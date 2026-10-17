"""Инструмент «Перенос на другой домен» (админка svcmsadmin).

Данные конструктора привязаны к `domain_id` (домен = сайт), см.
`page_constructor/TABLES.md`. Инструмент переносит/копирует их на другой домен
(существующий или только что созданный):

* режим `copy` — источник продолжает работать, у приёмника появляется копия;
* режим `move` — строки переезжают (UPDATE), источник теряет настройки.

Работает и для конструкторных (template.type=6), и для обычных проектов:
у обычных конструкторных таблиц нет, переносятся hosting/DNS/РКН и, при желании,
создаётся отдельная копия шаблона с папкой.

Операция идёт фоном (копия папки шаблона может быть тяжёлой), с компенсацией:
транзакций в db-слое нет.
"""

import re
from typing import List, Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel

from lib.background import enqueue, register_task
from .common import manager, require_permission
from .domain_scope import (
  COMMON_PARTS, CONSTRUCTOR_PARTS, DOMAIN_THEME_TABLES,
  clone_template_for_domain, copy_domain_constructor, copy_domain_lists,
  copy_template_dir, delete_domain_leftovers, domain_counts, domain_profile,
  move_domain_constructor, next_free_port, table_columns,
)

router = APIRouter()

# Как в карточке домена (configs/svcmsadmin/domain).
DOMAIN_RE = re.compile(r'^[a-zA-Z0-9\-\.]+$')
SYNC_PARTS = tuple(CONSTRUCTOR_PARTS) + tuple(COMMON_PARTS)


class SyncIn(BaseModel):
  src_domain_id: int
  mode: str = 'copy'                  # copy | move
  dst_domain_id: Optional[int] = None  # существующий приёмник
  new_domain: Optional[str] = None     # либо создаём новый домен
  new_folder: Optional[str] = None     # папка шаблона для template_mode='clone'
  template_mode: str = 'inherit'       # inherit | clone (только не-DS)
  parts: Optional[List[str]] = None
  pages_mode: str = 'replace'          # replace | merge (страницы)
  delete_old: bool = False             # удалить источник (только при mode='move')
  port: Optional[int] = None           # порт нового DS-домена (иначе авто)


class SyncError(Exception):
  pass


async def _check(errors):
  if errors:
    raise SyncError(errors[-1])


def _clean_parts(parts):
  parts = [p for p in (parts or SYNC_PARTS) if p in SYNC_PARTS]
  return parts or list(SYNC_PARTS)


# ---------------------------------------------------------------------------
# Превью
# ---------------------------------------------------------------------------

@router.get('/domain/sync/preview')
async def domain_sync_preview(request: Request, src_domain_id: int, dst_domain_id: int = 0):
  """Что переедет и о чём предупредить — до выполнения."""
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  warnings = []
  src = await domain_profile(db, src_domain_id)
  if not src:
    return {'success': False, 'errors': ['Домен-источник не найден']}
  dst = await domain_profile(db, dst_domain_id) if dst_domain_id else None
  if dst and int(dst.get('project_id') or 0) != int(src.get('project_id') or 0):
    if src.get('is_constructor'):
      warnings.append('Приёмник принадлежит другому проекту: страницы/тема конструктора '
                      'ссылаются на сущности проекта-источника — переносить их нельзя')
  src_counts = await domain_counts(db, src_domain_id, src.get('project_id'))
  dst_counts = await domain_counts(db, dst_domain_id, dst.get('project_id')) if dst else {}
  if dst and not dst.get('is_constructor'):
    warnings.append('Приёмник — обычный шаблон (не конструктор): страницы/тема ему не нужны')
  if dst_counts.get('domain_page'):
    warnings.append('У приёмника уже есть страницы конструктора (%s) — при замене они будут перезаписаны'
                    % dst_counts['domain_page'])
  if src.get('is_constructor'):
    warnings.append('Конструктор привязан к домену: после копирования две версии будут '
                    'расходиться — дальше правьте только новый домен')
  else:
    warnings.append('У обычного проекта конструктор привязан к шаблонам: переносятся '
                    'hosting/DNS/РКН, страницы конструктора не участвуют')
  return {
    'success': True, 'errors': [], 'warnings': warnings,
    'src': src, 'dst': dst, 'src_counts': src_counts, 'dst_counts': dst_counts,
    'parts': list(SYNC_PARTS),
  }


# ---------------------------------------------------------------------------
# Постановка задачи
# ---------------------------------------------------------------------------

@router.post('/domain/sync/start')
async def domain_sync_start(request: Request, r: SyncIn):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_write
  mgr = manager(request)
  errors = []

  src = await domain_profile(db, r.src_domain_id)
  if not src:
    return {'success': False, 'errors': ['Домен-источник не найден']}
  if r.mode not in ('copy', 'move'):
    return {'success': False, 'errors': ['Неизвестный режим: %s' % r.mode]}
  if r.pages_mode not in ('replace', 'merge'):
    return {'success': False, 'errors': ['Неизвестный режим страниц: %s' % r.pages_mode]}
  if r.template_mode not in ('inherit', 'clone'):
    return {'success': False, 'errors': ['Неизвестный режим шаблона: %s' % r.template_mode]}

  new_domain = (r.new_domain or '').strip()
  if not new_domain and not r.dst_domain_id:
    return {'success': False, 'errors': ['Укажите новый домен или приёмник']}
  if new_domain:
    if not DOMAIN_RE.match(new_domain):
      return {'success': False, 'errors': ['Недопустимые символы в домене']}
    if len(new_domain) > 200:
      return {'success': False, 'errors': ['Домен длиннее 200 символов']}
    dup = await db.query(query='SELECT domain_id FROM domain WHERE domain=%s',
                         values=[new_domain], onerow=1, errors=errors)
    if errors:
      return {'success': False, 'errors': errors}
    if dup:
      return {'success': False, 'errors': ['Домен %s уже используется' % new_domain]}
    if r.port is not None and not (1 <= int(r.port) <= 65535):
      return {'success': False, 'errors': ['Порт должен быть в диапазоне 1..65535']}
  if r.delete_old and r.mode != 'move':
    return {'success': False, 'errors': ['Удалить источник можно только в режиме «перенести»']}

  task_id = await enqueue(
    config='svcmsadmin',
    action='domain_sync',
    params={
      'src_domain_id': r.src_domain_id,
      'mode': r.mode,
      'dst_domain_id': r.dst_domain_id,
      'new_domain': new_domain,
      'new_folder': (r.new_folder or '').strip() or new_domain,
      'template_mode': r.template_mode,
      'parts': _clean_parts(r.parts),
      'pages_mode': r.pages_mode,
      'delete_old': r.delete_old,
      'port': r.port,
    },
    admin_id=mgr.get('id'),
  )
  return {'success': True, 'errors': [], 'task_id': task_id}


# ---------------------------------------------------------------------------
# Фоновая задача
# ---------------------------------------------------------------------------

async def _create_domain(db, src, new_domain, port, errors):
  """Создаёт новый домен как копию источника (без SSL-полей и дат оплаты)."""
  server_type = int(src.get('server_type') or 3)
  data = {
    'domain': new_domain,
    'project_id': src.get('project_id'),
    'template_id': src.get('template_id'),
    'server_type': server_type,
    'dns_enabled': src.get('dns_enabled', 1),
    'our_domain': src.get('our_domain', 0),
    'not_cache_nginx': src.get('not_cache_nginx', 0),
    'is_adaptive': src.get('is_adaptive', 0),
    'not_crm_server': src.get('not_crm_server', 0),
    'user_id': src.get('user_id', 0),
    'dkim_enabled': src.get('dkim_enabled', 0),
    'need_clean_cache': 1,
    # SSL выдаётся заново: is_ssl/lets_encrypt_status/paid_till/ssl_domains — дефолты.
  }
  if server_type == 4:
    port = int(port) if port else await next_free_port(db)
    if not (1 <= port <= 65535):
      raise SyncError('не осталось свободных портов')
    data['port'] = port
  else:
    data['port'] = 0
  new_id = await db.save(table='domain', data=data, errors=errors)
  _check(errors)
  if not new_id:
    raise SyncError('не удалось создать домен %s' % new_domain)
  # MySQL в не-strict режиме усекает длинные строки — сверяем записанное.
  row = await db.query(query='SELECT domain FROM domain WHERE domain_id=%s',
                       values=[new_id], onerow=1, errors=errors)
  if not row or (row.get('domain') or '') != new_domain:
    raise SyncError('домен %s не сохранён (проверьте длину/формат)' % new_domain)
  return new_id


async def _revert(db, state, warnings):
  """Компенсация: возвращаем перенесённое и убираем созданное."""
  if state.get('moved'):
    try:
      await move_domain_constructor(db, state['dst_domain_id'], state['src_domain_id'],
                                    parts=state.get('parts'), errors=[])
    except Exception as e:
      warnings.append('откат переноса не удался: %s' % e)
  if state.get('created_domain'):
    await db.query(query='DELETE FROM domain WHERE domain_id=%s',
                   values=[state['dst_domain_id']], errors=[])
  if state.get('created_template'):
    await db.query(query='DELETE FROM template_const WHERE template_id=%s',
                   values=[state['created_template']], errors=[])
    await db.query(query='DELETE FROM url_run_code WHERE template_id=%s',
                   values=[state['created_template']], errors=[])
    await db.query(query='DELETE FROM url_rules WHERE template_id=%s',
                   values=[state['created_template']], errors=[])
    await db.query(query='DELETE FROM template WHERE template_id=%s',
                   values=[state['created_template']], errors=[])


async def run_domain_sync(ctx):
  p = ctx.params or {}
  db = ctx.db
  errors = []
  warnings = []
  src_id = int(p.get('src_domain_id') or 0)
  dst_id = int(p.get('dst_domain_id') or 0) or None
  new_domain = (p.get('new_domain') or '').strip()
  new_folder = (p.get('new_folder') or '').strip() or new_domain
  mode = p.get('mode') or 'copy'
  parts = _clean_parts(p.get('parts'))
  pages_mode = p.get('pages_mode') or 'replace'
  template_mode = p.get('template_mode') or 'inherit'
  delete_old = bool(p.get('delete_old'))
  state = {'src_domain_id': src_id, 'dst_domain_id': None, 'parts': parts,
           'created_domain': False, 'created_template': None, 'moved': False}

  try:
    await ctx.progress(5, 'Проверки')
    src = await domain_profile(db, src_id)
    if not src:
      raise SyncError('Домен-источник не найден')
    is_constructor = bool(src.get('is_constructor'))
    constructor_parts = [x for x in parts if x in CONSTRUCTOR_PARTS]
    if constructor_parts and not is_constructor:
      # У обычного проекта конструкторских данных нет — это не ошибка, просто пропустим.
      warnings.append('Обычный проект: части конструктора (%s) пропущены' % ', '.join(constructor_parts))
      parts = [x for x in parts if x not in CONSTRUCTOR_PARTS]
      state['parts'] = parts

    await ctx.progress(15, 'Определяем приёмник')
    if new_domain:
      dst_id = await _create_domain(db, src, new_domain, p.get('port'), errors)
      state['created_domain'] = True
      warnings.append('создан домен %s (#%s)' % (new_domain, dst_id))
    else:
      dst = await domain_profile(db, dst_id)
      if not dst:
        raise SyncError('Домен-приёмник не найден')
      if int(dst['domain_id']) == src_id:
        raise SyncError('Приёмник совпадает с источником')
      if constructor_parts and int(dst.get('project_id') or 0) != int(src.get('project_id') or 0):
        raise SyncError('Страницы/тема конструктора ссылаются на сущности своего проекта — '
                        'приёмник должен быть из того же проекта')
      if mode == 'move':
        dst_counts = await domain_counts(db, dst_id)
        busy = [t for t in ('domain_page', 'domain_constructor', 'domain_rkn')
                if dst_counts.get(t)]
        if busy:
          raise SyncError('У приёмника уже есть данные конструктора (%s). '
                          'Для переноса выберите пустой домен или используйте копирование'
                          % ', '.join(busy))
    state['dst_domain_id'] = dst_id

    if not is_constructor and template_mode == 'clone':
      await ctx.progress(35, 'Копируем шаблон')
      new_tid, src_folder = await clone_template_for_domain(
        db, src_id, dst_id, new_folder or str(new_domain or ''), errors)
      _check(errors)
      state['created_template'] = new_tid
      if new_tid:
        warnings.append('создан шаблон #%s (папка %s)' % (new_tid, new_folder))
        if src_folder:
          copied = await copy_template_dir(src_folder, new_folder, warnings)
          if copied:
            warnings.append('папка шаблона скопирована: %s' % copied)

    await ctx.progress(55, 'Копируем доменные данные')
    await copy_domain_lists(db, src_id, dst_id, parts=parts, replace=True, errors=errors)
    _check(errors)

    if constructor_parts:
      await ctx.progress(70, 'Конструктор')
      if mode == 'move' and state['created_domain']:
        # Перенос в только что созданный домен: страницы/тема/схемы/РКН переезжают.
        await move_domain_constructor(db, src_id, dst_id, parts=constructor_parts, errors=errors)
        state['moved'] = True
      else:
        await copy_domain_constructor(db, src_id, dst_id, parts=constructor_parts,
                                      pages_mode=pages_mode, errors=errors)
      _check(errors)

    if delete_old:
      await ctx.progress(88, 'Удаляем исходный домен')
      await delete_domain_leftovers(db, src_id, errors=errors)
      _check(errors)
      await db.query(query='DELETE FROM domain WHERE domain_id=%s', values=[src_id], errors=errors)
      _check(errors)

    await ctx.progress(100, 'Готово')
    dst_profile = await domain_profile(db, dst_id)
    counts = await domain_counts(db, dst_id, (dst_profile or {}).get('project_id'))
    return {
      'success': True, 'errors': [], 'warnings': warnings,
      'src_domain_id': src_id, 'dst_domain_id': dst_id,
      'dst_domain': (dst_profile or {}).get('domain'),
      'mode': mode, 'is_constructor': is_constructor,
      'template_id': (dst_profile or {}).get('template_id'),
      'port': (dst_profile or {}).get('port'),
      'parts': parts, 'pages_mode': pages_mode,
      'counts': counts,
    }

  except Exception as e:
    await _revert(db, state, warnings)
    message = str(e) or 'неизвестная ошибка'
    if warnings:
      message += ' | ' + '; '.join(str(x) for x in warnings[-3:])
    raise SyncError(message)


register_task('svcmsadmin', 'domain_sync', run_domain_sync)
