import asyncio
import json
import os
import random
import shutil
import string
from typing import List, Optional

from fastapi import APIRouter, Request
from pydantic import BaseModel

from config import config as sysconfig
from lib.background import enqueue, register_task
from lib.password import hash_password
from .common import manager, require_permission, create_domain_rkn
from .domain_scope import copy_domain_constructor
from .project_clone import COLS as CLONE_COLS

router = APIRouter()

BASE_PAGES = os.path.join(os.path.dirname(__file__), 'page_constructor', 'base_pages.json')
THEME_AXES = ('color', 'style', 'layout', 'font')
THEME_DEFAULTS = {'color': 'digitalstrateg', 'style': 'soft', 'layout': 'standard', 'font': 'inter'}
BLOCKS_EMPTY = '{"schema": "svcms.page_blocks", "version": 2, "blocks": []}'


class CreateError(Exception):
  pass


def _paths():
  return sysconfig.get('paths') or {}


def _source_project_id(override=None):
  if override:
    return int(override)
  return int((sysconfig.get('fast_create') or {}).get('source_project_id') or 0)


def _check(errors):
  if errors:
    msg = errors[-1]
    errors.clear()
    raise CreateError(msg)


def _gen_password(n=8):
  return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def _first(row):
  return list(row.values())[0] if row else None


def _load_base_pages():
  with open(BASE_PAGES, 'r', encoding='utf-8') as f:
    return json.load(f)


def _blocks_doc(value):
  """Приводит blocks страницы к формату v2 (как template_pages_base / base-pages)."""
  if value is None or value == '':
    return BLOCKS_EMPTY
  if isinstance(value, (dict, list)):
    data = value
  else:
    data = json.loads(value)
  if isinstance(data, list):
    data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': data}
  elif isinstance(data, dict) and 'blocks' not in data:
    data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': []}
  return json.dumps(data, ensure_ascii=False)


async def _table_columns(db, table):
  rows = await db.query(query='SHOW COLUMNS FROM `%s`' % table, errors=[])
  return {r.get('Field') for r in (rows or [])}


async def _next_free_port(db):
  """Свободный порт = максимальный занятый (в допустимом диапазоне TCP) + 1."""
  row = await db.query(
    query='SELECT MAX(port) mx FROM domain WHERE port BETWEEN 1 AND 65535',
    onerow=1,
    errors=[],
  )
  port = int((row or {}).get('mx') or 0) + 1
  if port > 65535:
    raise CreateError('не осталось свободных портов')
  return port


async def _theme_from_source(db, source_project_id, errors):
  theme = dict(THEME_DEFAULTS)
  if not source_project_id:
    return theme
  row = await db.query(
    query='SELECT dc.color, dc.style, dc.layout, dc.font FROM domain d '
          'JOIN domain_constructor dc ON dc.domain_id=d.domain_id '
          'WHERE d.project_id=%s LIMIT 1',
    values=[source_project_id],
    onerow=1,
    errors=errors,
  )
  _check(errors)
  if row:
    for axis in THEME_AXES:
      if row.get(axis):
        theme[axis] = row[axis]
  return theme


async def _ensure_constructor_default(db, domain_id, source_project_id, errors):
  """Тема из проекта-эталона + шапка/подвал из base_pages.json."""
  theme = await _theme_from_source(db, source_project_id, errors)
  base = _load_base_pages()
  header_blocks = json.dumps(base.get('header'), ensure_ascii=False) if base.get('header') else None
  footer_blocks = json.dumps(base.get('footer'), ensure_ascii=False) if base.get('footer') else None
  await db.query(
    query='INSERT INTO domain_constructor(domain_id, color, style, layout, font, header_blocks, footer_blocks) '
          'VALUES(%s,%s,%s,%s,%s,%s,%s) '
          'ON DUPLICATE KEY UPDATE color=VALUES(color), style=VALUES(style), layout=VALUES(layout), '
          'font=VALUES(font), header_blocks=VALUES(header_blocks), footer_blocks=VALUES(footer_blocks)',
    values=[domain_id, theme['color'], theme['style'], theme['layout'], theme['font'], header_blocks, footer_blocks],
    errors=errors,
  )
  _check(errors)


async def _apply_base_pages(db, domain_id, errors):
  """Страницы из базового набора (base_pages_set / template_pages_base)."""
  base_set = await db.query(
    query='SELECT id FROM base_pages_set ORDER BY is_default DESC, sort, id LIMIT 1',
    onerow=1,
    errors=errors,
  )
  _check(errors)
  set_id = (base_set or {}).get('id')
  if not set_id:
    return 0
  pages = await db.query(
    query='SELECT url, header, blocks FROM template_pages_base WHERE set_id=%s ORDER BY sort, url',
    values=[set_id],
    errors=errors,
  )
  _check(errors)
  count = 0
  for page in (pages or []):
    url = (page.get('url') or '').strip()
    if not url:
      continue
    await db.query(
      query='INSERT INTO domain_page(domain_id, url, header, blocks) VALUES(%s,%s,%s,%s)',
      values=[domain_id, url, page.get('header') or '', _blocks_doc(page.get('blocks'))],
      errors=errors,
    )
    _check(errors)
    count += 1
  await db.query(
    query='INSERT INTO domain_constructor(domain_id, base_set_id) VALUES(%s,%s) '
          'ON DUPLICATE KEY UPDATE base_set_id=VALUES(base_set_id)',
    values=[domain_id, set_id],
    errors=errors,
  )
  _check(errors)
  return count


async def _copy_constructor(db, src_domain_id, dst_domain_id, errors):
  """Копирует тему/шапку/подвал домена-источника. True — если строка была.

  Само копирование — в общем слое `domain_scope` (его же использует инструмент
  «Перенос на другой домен»).
  """
  if not (src_domain_id and dst_domain_id):
    return False
  has = await db.query(
    query='SELECT domain_id FROM domain_constructor WHERE domain_id=%s',
    values=[src_domain_id],
    onerow=1,
    errors=errors,
  )
  _check(errors)
  if not has:
    return False
  # Тема + доменные схемы темы (без них /theme.css соберётся без своей оси —
  # например, style=armit у demo1 лежит в domain_theme_style с domain_id домена).
  await copy_domain_constructor(db, src_domain_id, dst_domain_id,
                                parts=('theme', 'schemes'), errors=errors)
  _check(errors)
  return True


async def _copy_pages_from_domain(db, src_domain_id, dst_domain_id, errors):
  rows = await db.query(
    query='SELECT url, header, blocks FROM domain_page WHERE domain_id=%s ORDER BY id',
    values=[src_domain_id],
    errors=errors,
  )
  _check(errors)
  count = 0
  for page in (rows or []):
    url = (page.get('url') or '').strip()
    if not url:
      continue
    await db.query(
      query='INSERT INTO domain_page(domain_id, url, header, blocks) VALUES(%s,%s,%s,%s)',
      values=[dst_domain_id, url, page.get('header') or '', _blocks_doc(page.get('blocks'))],
      errors=errors,
    )
    _check(errors)
    count += 1
  return count


async def _copy_rkn(db, src_domain_id, dst_domain_id, errors):
  await copy_domain_constructor(db, src_domain_id, dst_domain_id, parts=('rkn',), errors=errors)
  _check(errors)


# Клонирование данных ds-конструктора: порядок по зависимостям + перепривязка id.
# Для каждой таблицы перечислены колонки-ссылки на id другой ds-таблицы; если
# значение равно самой таблице -- это self-ссылка (parent_id), её правим вторым
# проходом. Порядок списка -- топологический (родители раньше детей).
DS_CLONE_RULES = [
  ('ds_brands', {}),
  ('ds_params', {}),
  ('ds_catalog', {'parent_id': 'ds_catalog'}),
  ('ds_bottom_menu', {'parent_id': 'ds_bottom_menu'}),
  ('ds_service', {'parent_id': 'ds_service'}),
  ('ds_top_menu', {'parent_id': 'ds_top_menu'}),
  ('ds_zakaz', {}),
  ('ds_good', {'rubricator_id': 'ds_catalog', 'brand': 'ds_brands'}),
  ('ds_good_galery', {'good_id': 'ds_good'}),
  ('ds_params_catalog', {'param_id': 'ds_params', 'catalog_id': 'ds_catalog'}),
  ('ds_params_good', {'param_id': 'ds_params', 'good_id': 'ds_good'}),
  ('ds_zakaz_good', {'zakaz_id': 'ds_zakaz', 'good_id': 'ds_good'}),
  ('ds_advantages', {}),
  ('ds_article', {}),
  ('ds_certificates', {}),
  ('ds_clients', {}),
  ('ds_doc', {}),
  ('ds_employee', {}),
  ('ds_filials', {}),
  ('ds_form_submit', {}),
  ('ds_galery', {}),
  ('ds_news', {}),
  ('ds_reviews', {}),
  ('ds_slider', {}),
  ('ds_text', {}),
  ('ds_video', {}),
]


async def _ds_table_columns(db, table):
  """Колонки ds-таблицы: [{name, auto, null}] либо None, если таблицы нет."""
  rows = await db.query(query='SHOW COLUMNS FROM `%s`' % table, errors=[])
  if not rows:
    return None
  return [{
    'name': r.get('Field'),
    'auto': 'auto_increment' in (r.get('Extra') or '').lower(),
    'null': (r.get('Null') or '').upper() == 'YES',
  } for r in rows or []]


def _ds_link_value(old, mapped, nullable):
  """Новое значение ссылки: id из карты, иначе NULL (если можно) или 0."""
  if old in (None, '', 0):
    return None if nullable else 0
  if old in mapped:
    return mapped[old]
  return None if nullable else 0


async def _copy_ds_tables(db, source_project_id, project_id, warnings):
  """Клонирует данные ds-конструктора с перепривязкой id (по зависимостям)."""
  if not source_project_id:
    warnings.append('ds-данные: не задан проект-источник')
    return
  id_map = {}
  for table, refs in DS_CLONE_RULES:
    cols = await _ds_table_columns(db, table)
    if not cols:
      continue
    names = [c['name'] for c in cols]
    if 'id' not in names:
      continue
    meta = {c['name']: c for c in cols}
    has_project = 'project_id' in names

    if has_project:
      rows = await db.query(
        query='SELECT * FROM `%s` WHERE project_id=%%s' % table,
        values=[source_project_id],
        errors=[],
      )
    else:
      # Таблицы без project_id (ds_zakaz_good): берём строки, ссылающиеся на уже
      # скопированных родителей.
      flt = None
      for col, ref in refs.items():
        if id_map.get(ref):
          flt = (col, list(id_map[ref].keys()))
          break
      if not flt:
        continue
      col, old_ids = flt
      rows = await db.query(
        query='SELECT * FROM `%s` WHERE `%s` IN (%s)' % (table, col, ','.join(str(i) for i in old_ids)),
        errors=[],
      )

    id_map.setdefault(table, {})
    self_rows = []
    warned = False
    for row in rows or []:
      old_id = row.get('id')
      data = {c['name']: row.get(c['name']) for c in cols if not c['auto']}
      if has_project:
        data['project_id'] = project_id
      for col, ref in refs.items():
        old = row.get(col)
        if ref == table:
          # self-ссылка: вставляем заглушку, поправим вторым проходом.
          self_rows.append((old_id, col, old))
          data[col] = None if meta[col]['null'] else 0
        else:
          data[col] = _ds_link_value(old, id_map.get(ref, {}), meta[col]['null'])
      errs = []
      new_id = await db.save(table=table, data=data, errors=errs)
      if not new_id or errs:
        if not warned:
          warnings.append('%s: %s' % (table, (errs or ['не удалось вставить'])[-1]))
          warned = True
        continue
      id_map[table][old_id] = new_id

    # Второй проход: родительские ссылки внутри той же таблицы.
    for old_id, col, old_parent in self_rows:
      new_id = id_map[table].get(old_id)
      if not new_id:
        continue
      new_parent = id_map[table].get(old_parent) if old_parent else None
      await db.query(
        query='UPDATE `%s` SET `%s`=%%s WHERE id=%%s' % (table, col),
        values=[new_parent, new_id],
        errors=[],
      )
  # id_map (таблица → {старый id: новый id}) нужен для перепривязки ЧПУ.
  return id_map


# Префикс технического url → структура (совпадает с движком:
# lib/dsengine/page.py EXT_URL_PREFIXES и lib/seo_files.py _URL_OPTIONS).
CHPU_PREFIX_TABLE = {
  '/news/': 'ds_news',
  '/article/': 'ds_article',
  '/service/': 'ds_service',
  '/catalog/': 'ds_catalog',
  '/good/': 'ds_good',
}


async def _copy_chpu(db, source_project_id, project_id, id_map, warnings):
  """Переносит ЧПУ (in_ext_url) с перепривязкой id на новый проект.

  in_url имеет вид '/catalog/<id>' (технический url), ext_url — slug. Id внутри
  in_url указывает на строку структуры, которая при клонировании получила новый
  id, поэтому подставляем его из id_map. Без этого ссылки идут как '/catalog/1213'.
  """
  if not source_project_id or not id_map:
    return 0
  rows = await db.query(
    query='SELECT in_url, ext_url FROM in_ext_url WHERE project_id=%s',
    values=[source_project_id],
    errors=[],
  )
  copied = 0
  skipped = set()
  for row in rows or []:
    in_url = str(row.get('in_url') or '')
    ext_url = row.get('ext_url')
    if not (in_url and ext_url):
      continue
    prefix, _, tail = in_url.rpartition('/')
    prefix += '/'
    table = CHPU_PREFIX_TABLE.get(prefix)
    if not table:
      skipped.add(prefix)
      continue
    new_id = None
    if tail.isdigit():
      new_id = (id_map.get(table) or {}).get(int(tail))
    if not new_id:
      continue
    errs = []
    await db.query(
      query='INSERT IGNORE INTO in_ext_url(project_id, in_url, ext_url) VALUES(%s,%s,%s)',
      values=[project_id, '%s%s' % (prefix, new_id), ext_url],
      errors=errs,
    )
    if errs:
      warnings.append('ЧПУ %s: %s' % (in_url, errs[-1]))
      continue
    copied += 1
  for p in sorted(skipped):
    warnings.append('ЧПУ: неизвестный префикс %s' % p)
  return copied


async def _copy_promo(db, source_project_id, project_id, warnings):
  """Копирует SEO-тексты страниц (promo)."""
  cols = await _table_columns(db, 'promo')
  if not cols or 'project_id' not in cols:
    return 0
  use_cols = [c for c in ('promo_title', 'promo_description', 'promo_keywords', 'promo_body',
                          'url', 'project_id', 'add_tags', 'h1') if c in cols]
  select_cols = ['%s' if c == 'project_id' else '`%s`' % c for c in use_cols]
  table_errors = []
  await db.query(
    query='INSERT INTO promo(%s) SELECT %s FROM promo WHERE project_id=%%s'
          % (','.join('`%s`' % c for c in use_cols), ','.join(select_cols)),
    values=[project_id, source_project_id],
    errors=table_errors,
  )
  if table_errors:
    warnings.append('promo: %s' % table_errors[-1])
    return 0
  return 1


async def _copy_common_tables(db, source_project_id, project_id, warnings):
  """Копирует данные общих сущностей проекта (news, article, good, ...)."""
  for table, col_list in CLONE_COLS.items():
    cols = await _table_columns(db, table)
    if not cols or 'project_id' not in cols:
      continue
    use_cols = [c.strip() for c in col_list.split(',') if c.strip() in cols]
    if 'project_id' not in use_cols:
      use_cols.append('project_id')
    select_cols = [str(project_id) if c == 'project_id' else '`%s`' % c for c in use_cols]
    table_errors = []
    await db.query(
      query='INSERT INTO `%s`(%s) SELECT %s FROM `%s` WHERE project_id=%%s'
            % (table, ','.join('`%s`' % c for c in use_cols), ','.join(select_cols), table),
      values=[source_project_id],
      errors=table_errors,
    )
    if table_errors:
      warnings.append('%s: %s' % (table, table_errors[-1]))

  content_cols = await _table_columns(db, 'content')
  if content_cols and 'project_id' in content_cols:
    await db.query(
      query='INSERT INTO content(header,body,url,project_id) '
            'SELECT header,body,url,%s FROM content WHERE project_id=%s',
      values=[project_id, source_project_id],
      errors=[],
    )


async def _copy_struct_tables(db, source_project_id, project_id, warnings):
  """Копирует уникальные структуры struct_<pid>_<name> под новый project_id."""
  rows = await db.query(
    query='SHOW TABLES LIKE %s',
    values=['struct\\_%s\\_%%' % source_project_id],
    errors=[],
  ) or []
  created = []
  for row in rows:
    old_table = _first(row)
    if not old_table:
      continue
    new_table = old_table.replace('struct_%s' % source_project_id, 'struct_%s' % project_id)
    table_errors = []
    await db.query(query='CREATE TABLE `%s` LIKE `%s`' % (new_table, old_table), errors=table_errors)
    await db.query(query='INSERT INTO `%s` SELECT * FROM `%s`' % (new_table, old_table), errors=table_errors)
    cols = await _table_columns(db, new_table)
    if 'project_id' in cols:
      await db.query(
        query='UPDATE `%s` SET project_id=%%s WHERE project_id=%%s' % new_table,
        values=[project_id, source_project_id],
        errors=table_errors,
      )
    if table_errors:
      warnings.append('%s: %s' % (new_table, table_errors[-1]))
    else:
      created.append(new_table)
  return created


def _copy_pairs(source_project_id, project_id, new_folder, src_folder):
  """Пары каталогов источник→назначение для копирования файлов проекта."""
  paths = _paths()
  pairs = []
  engine_root = paths.get('engine_root')
  if engine_root:
    pairs.append((
      os.path.join(engine_root, 'files', 'project_%s' % source_project_id),
      os.path.join(engine_root, 'files', 'project_%s' % project_id),
    ))
    pairs.append((
      os.path.join(engine_root, 'projects', 'project_%s' % source_project_id),
      os.path.join(engine_root, 'projects', 'project_%s' % project_id),
    ))
  conf_root = paths.get('conf_projects')
  if conf_root:
    pairs.append((
      os.path.join(conf_root, 'project_%s' % source_project_id),
      os.path.join(conf_root, 'project_%s' % project_id),
    ))
  templates_root = paths.get('templates')
  if templates_root and src_folder and new_folder:
    pairs.append((
      os.path.join(templates_root, src_folder),
      os.path.join(templates_root, new_folder),
    ))
  files_root = paths.get('files')
  if files_root:
    pairs.append((
      os.path.join(files_root, 'project_%s' % source_project_id),
      os.path.join(files_root, 'project_%s' % project_id),
    ))
  return pairs


async def _copy_files(pairs, warnings):
  copied = []
  for src, dst in pairs:
    if not src or not os.path.isdir(src):
      continue
    try:
      await asyncio.to_thread(
        shutil.copytree, src, dst,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('__pycache__'),
      )
      copied.append(dst)
    except Exception as e:
      warnings.append('файлы %s: %s' % (src, e))
  return copied


async def _make_dirs(project_id, folder, warnings):
  """Пустые каталоги проекта -- для проекта «с чистого листа»."""
  paths = _paths()
  dirs = []
  engine_root = paths.get('engine_root')
  if engine_root:
    dirs.append(os.path.join(engine_root, 'files', 'project_%s' % project_id))
    dirs.append(os.path.join(engine_root, 'projects', 'project_%s' % project_id))
  for key in ('conf_projects', 'files'):
    root = paths.get(key)
    if root:
      dirs.append(os.path.join(root, 'project_%s' % project_id))
  created = []
  for d in dirs:
    try:
      await asyncio.to_thread(os.makedirs, d, exist_ok=True)
      created.append(d)
    except Exception as e:
      warnings.append('каталог %s: %s' % (d, e))
  return created


async def _ensure_template_dir(folder, warnings):
  """Папка шаблона (paths.templates/<folder>) должна существовать для template.folder."""
  root = _paths().get('templates')
  if not root or not folder:
    return None
  path = os.path.join(root, folder)
  try:
    await asyncio.to_thread(os.makedirs, path, exist_ok=True)
    return path
  except Exception as e:
    warnings.append('каталог шаблона %s: %s' % (path, e))
    return None


async def _rollback(db, created):
  errors = []
  domain_id = created.get('domain_id')
  project_id = created.get('project_id')
  manager_id = created.get('manager_id')
  template_id = created.get('template_id')

  if domain_id:
    await db.query(query='DELETE FROM domain WHERE domain_id=%s', values=[domain_id], errors=errors)
  if template_id:
    await db.query(query='DELETE FROM template WHERE template_id=%s', values=[template_id], errors=errors)
  if project_id:
    await db.query(query='DELETE FROM manager_project_access WHERE project_id=%s', values=[project_id], errors=errors)
    await db.query(query='DELETE FROM const WHERE project_id=%s', values=[project_id], errors=errors)
    await db.query(query='DELETE FROM project_struct_public WHERE project_id=%s', values=[project_id], errors=errors)
    await db.query(query='DELETE FROM admin_project WHERE project_id=%s', values=[project_id], errors=errors)
  if manager_id:
    await db.query(query='DELETE FROM manager WHERE manager_id=%s', values=[manager_id], errors=errors)
  if project_id:
    await db.query(query='DELETE FROM project WHERE project_id=%s', values=[project_id], errors=errors)
  for table in (created.get('struct_tables') or []):
    await db.query(query='DROP TABLE IF EXISTS `%s`' % table, errors=errors)
  for path in (created.get('dirs') or []):
    try:
      if os.path.isdir(path):
        await asyncio.to_thread(shutil.rmtree, path)
    except Exception:
      pass
  return errors


# ---------------------------------------------------------------------------
# Эндпоинты подготовки формы
# ---------------------------------------------------------------------------

@router.get('/project/create/init')
async def project_create_init(request: Request):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  errors = []
  source_project_id = _source_project_id()

  source_domain = None
  if source_project_id:
    source_domain = await db.query(
      query='SELECT d.domain_id, d.domain, d.template_id, d.project_id, p.header, t.type '
            'FROM domain d '
            'JOIN project p ON p.project_id=d.project_id '
            'JOIN template t ON t.template_id=d.template_id '
            'WHERE d.project_id=%s ORDER BY (t.type=6) DESC, d.domain_id LIMIT 1',
      values=[source_project_id],
      onerow=1,
      errors=errors,
    )

  ds_options = await db.query(
    query='SELECT id, header, name, sort, is_menu, parent_id, note FROM ds_options ORDER BY sort, id',
    errors=errors,
  )

  source_option_ids = []
  if source_project_id:
    rows = await db.query(
      query='SELECT option_id FROM ds_options_project WHERE project_id=%s ORDER BY option_id',
      values=[source_project_id],
      errors=errors,
    )
    source_option_ids = [int(r['option_id']) for r in (rows or [])]

  return {
    'success': not errors,
    'errors': errors,
    'source_project_id': source_project_id,
    'source_domain': source_domain,
    'source_option_ids': source_option_ids,
    'ds_options': ds_options or [],
  }


@router.get('/project/create/templates')
async def project_create_templates(request: Request):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  errors = []
  templates = await db.query(
    query='SELECT template_id, header, folder, type FROM template WHERE type=6 ORDER BY header',
    errors=errors,
  ) or []
  return {
    'success': not errors,
    'errors': errors,
    'templates': templates,
    'source_project_id': _source_project_id(),
  }


@router.get('/project/create/domains')
async def project_create_domains(request: Request, term: str = '', constructor: int = 0):
  """Autocomplete доменов: {v: domain_id, d: 'domain — Проект (#id)', type, project_id, template_id}."""
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  errors = []
  where = []
  values = []
  if term:
    where.append('(d.domain LIKE %s OR p.header LIKE %s)')
    values.extend(['%' + term + '%', '%' + term + '%'])
  if constructor:
    where.append('t.type=6')
  query = (
    "SELECT d.domain_id v, CONCAT(d.domain, ' — ', p.header, ' (#', p.project_id, ')') d, "
    "d.template_id, d.project_id, t.type "
    "FROM domain d "
    "JOIN project p ON p.project_id=d.project_id "
    "JOIN template t ON t.template_id=d.template_id"
  )
  if where:
    query += ' WHERE ' + ' AND '.join(where)
  query += ' ORDER BY d.domain LIMIT 20'
  rows = await db.query(query=query, values=values, errors=errors) or []
  return {'success': not errors, 'errors': errors, 'list': rows}


@router.get('/project/create/options')
async def project_create_options(request: Request, project_id: int):
  """Опции конструктора (ds_options_project) выбранного проекта."""
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  errors = []
  rows = await db.query(
    query='SELECT option_id FROM ds_options_project WHERE project_id=%s ORDER BY option_id',
    values=[project_id],
    errors=errors,
  )
  return {
    'success': not errors,
    'errors': errors,
    'option_ids': [int(r['option_id']) for r in (rows or [])],
  }


@router.get('/project/create/next-port')
async def project_create_next_port(request: Request):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  return {'success': True, 'errors': [], 'port': await _next_free_port(db)}


@router.get('/project/create/check-domain')
async def project_create_check_domain(request: Request, domain: str = ''):
  """Проверка занятости домена до создания проекта."""
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  domain = (domain or '').strip()
  if not domain:
    return {'success': True, 'errors': [], 'exists': False}
  row = await db.query(
    query='SELECT d.domain_id, d.project_id, p.header FROM domain d '
          'LEFT JOIN project p ON p.project_id=d.project_id WHERE d.domain=%s',
    values=[domain],
    onerow=1,
    errors=[],
  )
  if row:
    return {
      'success': True, 'errors': [], 'exists': True,
      'domain_id': row.get('domain_id'),
      'project_id': row.get('project_id'),
      'project_header': row.get('header'),
    }
  return {'success': True, 'errors': [], 'exists': False}


# ---------------------------------------------------------------------------
# Постановка задачи
# ---------------------------------------------------------------------------

class CreateIn(BaseModel):
  mode: str = 'new'                    # new | base
  header: str
  domain: str
  source_domain_id: Optional[int] = None
  server_type: int = 3                 # 3 PSGI + utf8, 4 Python + Fastapi
  port: Optional[int] = None
  create_manager: bool = False
  login: Optional[str] = None
  password: Optional[str] = None
  # None -- не выбирали (взять как у источника), [] -- явно ни одной.
  ds_option_ids: Optional[List[int]] = None
  # Новый проект на базе конструктора страниц (DS).
  ds_mode: bool = False
  copy_data: bool = False
  demo: bool = False


@router.post('/project/create/start')
async def project_create_start(request: Request, r: CreateIn):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_write
  mgr = manager(request)
  errors = []

  header = (r.header or '').strip()
  domain = (r.domain or '').strip()
  if not header:
    return {'success': False, 'errors': ['Укажите название проекта']}
  if not domain:
    return {'success': False, 'errors': ['Укажите домен']}
  if len(domain) > 200:
    return {'success': False, 'errors': ['Домен длиннее 200 символов']}
  if r.mode not in ('new', 'base'):
    return {'success': False, 'errors': ['Неизвестный режим создания']}
  if r.server_type not in (3, 4):
    return {'success': False, 'errors': ['Недопустимый тип размещения']}
  if r.port is not None and not (1 <= int(r.port) <= 65535):
    return {'success': False, 'errors': ['Порт должен быть в диапазоне 1..65535']}
  # Домен-образец обязателен только при клонировании.
  if r.mode == 'base' and not r.source_domain_id:
    return {'success': False, 'errors': ['Выберите домен-образец']}

  if r.source_domain_id:
    src = await db.query(
      query='SELECT domain_id FROM domain WHERE domain_id=%s',
      values=[r.source_domain_id],
      onerow=1,
      errors=errors,
    )
    if errors:
      return {'success': False, 'errors': errors}
    if not src:
      return {'success': False, 'errors': ['Домен-образец не найден']}

  dup_domain = await db.query(
    query='SELECT domain_id FROM domain WHERE domain=%s',
    values=[domain],
    onerow=1,
    errors=errors,
  )
  if errors:
    return {'success': False, 'errors': errors}
  if dup_domain:
    return {'success': False, 'errors': ['Домен %s уже используется' % domain]}

  login = (r.login or '').strip()
  if r.create_manager:
    if not login:
      return {'success': False, 'errors': ['Укажите логин менеджера']}
    dup_login = await db.query(
      query='SELECT manager_id FROM manager WHERE login=%s',
      values=[login],
      onerow=1,
      errors=errors,
    )
    if errors:
      return {'success': False, 'errors': errors}
    if dup_login:
      return {'success': False, 'errors': ['Менеджер с логином %s уже существует' % login]}

  task_id = await enqueue(
    config='svcmsadmin',
    action='project_create',
    params={
      'mode': r.mode,
      'header': header,
      'domain': domain,
      'source_domain_id': r.source_domain_id,
      'server_type': r.server_type,
      'port': r.port,
      'create_manager': r.create_manager,
      'login': login,
      'password': r.password or '',
      'ds_option_ids': None if r.ds_option_ids is None else [int(x) for x in r.ds_option_ids],
      'ds_mode': r.ds_mode,
      'copy_data': r.copy_data,
      'demo': r.demo,
    },
    admin_id=mgr.get('id'),
  )
  return {'success': True, 'errors': [], 'task_id': task_id}


# ---------------------------------------------------------------------------
# Фоновая задача
# ---------------------------------------------------------------------------

async def run_project_create(ctx):
  p = ctx.params or {}
  db = ctx.db
  errors = []
  warnings = []

  mode = (p.get('mode') or 'new')
  header = (p.get('header') or '').strip()
  domain = (p.get('domain') or '').strip()
  source_domain_id = int(p.get('source_domain_id') or 0)
  server_type = int(p.get('server_type') or 3)
  port = p.get('port')
  create_manager = bool(p.get('create_manager'))
  login = (p.get('login') or '').strip()
  password = p.get('password') or ''
  ds_option_ids = p.get('ds_option_ids')
  if ds_option_ids is not None:
    ds_option_ids = [int(x) for x in ds_option_ids]
  ds_mode = bool(p.get('ds_mode')) and mode == 'new'
  copy_data = bool(p.get('copy_data'))
  demo = bool(p.get('demo'))

  await ctx.progress(3, 'Проверки')

  src = None
  if source_domain_id:
    src = await db.query(
      query='SELECT d.domain_id, d.domain, d.template_id, p.project_id, p.header project_header, '
            'p.options project_options, p.city, t.type tpl_type, t.options template_options, t.folder src_folder '
            'FROM domain d '
            'JOIN project p ON p.project_id=d.project_id '
            'JOIN template t ON t.template_id=d.template_id '
            'WHERE d.domain_id=%s',
      values=[source_domain_id],
      onerow=1,
      errors=errors,
    )
    _check(errors)
    if not src:
      raise CreateError('Домен-образец не найден')

  # В «новом» проекте домен-источник используется только как источник наполнения
  # конструктора; в остальных случаях он игнорируется.
  if mode == 'new' and not ds_mode:
    src = None

  src_pid = int(src['project_id']) if src else 0
  src_template_id = src['template_id'] if src else 0
  tpl_type = int(src['tpl_type'] or 0) if src else 0
  is_constructor = ds_mode or (tpl_type == 6)
  # Источник констант/структур/темы/опций: выбранный домен или проект-эталон.
  etalon_pid = _source_project_id()
  data_pid = src_pid or etalon_pid

  dup_domain = await db.query(
    query='SELECT domain_id FROM domain WHERE domain=%s',
    values=[domain],
    onerow=1,
    errors=errors,
  )
  _check(errors)
  if dup_domain:
    raise CreateError('Домен %s уже используется' % domain)

  if create_manager and login:
    dup_login = await db.query(
      query='SELECT manager_id FROM manager WHERE login=%s',
      values=[login],
      onerow=1,
      errors=errors,
    )
    _check(errors)
    if dup_login:
      raise CreateError('Менеджер с логином %s уже существует' % login)

  if create_manager and not password:
    password = _gen_password()

  if server_type == 4:
    port = int(port) if port else await _next_free_port(db)
    if not (1 <= port <= 65535):
      raise CreateError('недопустимый порт %s (нужно 1..65535)' % port)
  else:
    port = None

  created = {
    'project_id': None, 'domain_id': None, 'manager_id': None,
    'template_id': None, 'dirs': [], 'struct_tables': [],
  }
  pages_count = 0
  project_id = None

  try:
    await ctx.progress(12, 'Создаём проект')
    project_data = {'header': header, 'options': '', 'city': 0}
    if mode == 'base':
      project_data['options'] = src.get('project_options') or ''
      project_data['city'] = src.get('city') or 0
    project_id = await db.save(table='project', data=project_data, errors=errors)
    _check(errors)
    created['project_id'] = project_id

    await db.save(
      table='admin_project',
      data={'project_id': project_id, 'admin_id': ctx.admin_id or 0, 'type': 0},
      errors=errors,
    )
    _check(errors)

    await ctx.progress(22, 'Создаём шаблон и домен')
    # Клон DS-проекта переиспользует ОБЩИЙ шаблон конструктора: у него одна папка
    # бандла на всех (2026/ds-constructor), собственной папки быть не должно.
    clone_ds = (mode == 'base' and tpl_type == 6)
    if (mode == 'base' and not clone_ds) or (not src and not ds_mode):
      # Свой шаблон: клонирование (type источника) или «чистый лист» (обычный, type=1).
      new_template_id = await db.save(
        table='template',
        data={
          'folder': domain,
          'type': tpl_type if mode == 'base' else 1,
          'header': header,
          'options': (src.get('template_options') or '') if (mode == 'base' and src) else '',
        },
        errors=errors,
      )
      _check(errors)
      created['template_id'] = new_template_id
      # template.folder должен указывать на существующую папку
      # (локально sources.templates может отсутствовать — копирование пропустится).
      tmpl_dir = await _ensure_template_dir(domain, warnings)
      if tmpl_dir:
        created['dirs'].append(tmpl_dir)
    elif not src and ds_mode:
      # Новый DS-проект без источника: берём существующий шаблон конструктора.
      ds_tpl = await db.query(
        query='SELECT template_id FROM template WHERE type=6 ORDER BY template_id DESC LIMIT 1',
        onerow=1,
        errors=errors,
      )
      _check(errors)
      if not ds_tpl:
        raise CreateError('не найден шаблон конструктора (type=6)')
      new_template_id = ds_tpl['template_id']
    else:
      new_template_id = src_template_id

    domain_id = await db.save(
      table='domain',
      data={
        'domain': domain,
        'project_id': project_id,
        'template_id': new_template_id,
        'server_type': server_type,
        'not_cache_nginx': 1,
        'port': port,
      },
      errors=errors,
    )
    _check(errors)
    if not domain_id:
      raise CreateError('не удалось создать домен %s' % domain)
    created['domain_id'] = domain_id
    # MySQL в не-strict режиме усекает слишком длинные строки -- сверяем записанное,
    # иначе проект получит обрезанный домен (и rollback не удалит строку).
    drow = await db.query(
      query='SELECT domain FROM domain WHERE domain_id=%s',
      values=[domain_id],
      onerow=1,
      errors=errors,
    )
    _check(errors)
    if not drow or (drow.get('domain') or '') != domain:
      raise CreateError('домен %s не сохранён (проверьте длину/формат)' % domain)

    await ctx.progress(32, 'Константы и связи')
    if mode == 'base':
      # Клонирование: константы со значениями + стандартные структуры образца.
      await db.query(
        query='INSERT INTO const(name,value,project_id) '
              'SELECT name,value,%s FROM const WHERE project_id=%s',
        values=[project_id, data_pid],
        errors=errors,
      )
      _check(errors)
      await db.query(
        query='INSERT INTO project_struct_public(project_id,struct_public_id) '
              'SELECT %s,struct_public_id FROM project_struct_public WHERE project_id=%s',
        values=[project_id, data_pid],
        errors=errors,
      )
      _check(errors)
    elif is_constructor:
      # Новый проект-конструктор: набор констант DS (имена из источника/эталона,
      # значения пустые) + стандартные структуры.
      names = await db.query(
        query='SELECT name FROM const WHERE project_id=%s GROUP BY name',
        values=[data_pid],
        errors=errors,
      )
      _check(errors)
      if not names:
        warnings.append('константы не созданы: у источника нет const')
      for row in (names or []):
        name = (row.get('name') or '').strip()
        if not name:
          continue
        await db.query(
          query='INSERT INTO const(name, value, project_id) VALUES(%s,%s,%s)',
          values=[name, '', project_id],
          errors=errors,
        )
        _check(errors)
      await db.query(
        query='INSERT INTO project_struct_public(project_id,struct_public_id) '
              'SELECT %s,struct_public_id FROM project_struct_public WHERE project_id=%s',
        values=[project_id, data_pid],
        errors=errors,
      )
      _check(errors)
    # Обычный проект (не конструктор): константы не создаём.

    # Конфиги шаблона -- только когда создаём свою запись template (обычный клон).
    if mode == 'base' and not clone_ds:
      await db.query(
        query='INSERT INTO template_const(template_id,header,sort,type,description) '
              'SELECT %s,header,sort,type,description FROM template_const WHERE template_id=%s',
        values=[new_template_id, src_template_id],
        errors=errors,
      )
      _check(errors)
      await db.query(
        query='INSERT INTO url_run_code(header,template_id,url_regexp,run_code,sort) '
              'SELECT header,%s,url_regexp,REPLACE(run_code,%s,%s),sort FROM url_run_code WHERE template_id=%s',
        values=[new_template_id, src_pid, project_id, src_template_id],
        errors=errors,
      )
      _check(errors)
      await db.query(
        query='INSERT INTO url_rules(template_id,url_regexp,template_name,header,sort) '
              'SELECT %s,url_regexp,template_name,header,sort FROM url_rules WHERE template_id=%s',
        values=[new_template_id, src_template_id],
        errors=errors,
      )
      _check(errors)

    await ctx.progress(44, 'Создаём менеджера')
    if create_manager:
      manager_id = await db.save(
        table='manager',
        data={
          'login': login,
          'password': hash_password(password, sysconfig.get('encrypt_method')),
          'project_id': project_id,
        },
        errors=errors,
      )
      _check(errors)
      created['manager_id'] = manager_id
      await db.query(
        query='INSERT INTO manager_project_access(manager_id, project_id) VALUES(%s,%s)',
        values=[manager_id, project_id],
        errors=errors,
      )
      _check(errors)

    pages_src_domain = None
    if is_constructor:
      await ctx.progress(54, 'Опции конструктора')
      option_ids = ds_option_ids
      if option_ids is None:
        # Не выбирали -- берём набор опций источника (или эталона).
        rows = await db.query(
          query='SELECT option_id FROM ds_options_project WHERE project_id=%s ORDER BY option_id',
          values=[data_pid],
          errors=errors,
        )
        _check(errors)
        option_ids = [int(r['option_id']) for r in (rows or [])]
      for oid in option_ids:
        await db.query(
          query='INSERT IGNORE INTO ds_options_project(project_id,option_id) VALUES(%s,%s)',
          values=[project_id, oid],
          errors=errors,
        )
        _check(errors)

      # Страницы и тему копируем из источника (клон или DS-наполнение), если он задан.
      if src:
        pages_src_domain = int(src['domain_id'])

      await ctx.progress(64, 'Тема, шапка и подвал')
      if pages_src_domain:
        copied = await _copy_constructor(db, pages_src_domain, domain_id, errors)
        _check(errors)
        if not copied:
          await _ensure_constructor_default(db, domain_id, data_pid, errors)
        await _copy_rkn(db, pages_src_domain, domain_id, errors)
      else:
        await _ensure_constructor_default(db, domain_id, data_pid, errors)
      # Гарантируем запись domain_rkn (обязательные /soglasie и т.п.).
      await create_domain_rkn(db, domain_id, project_id)

      await ctx.progress(76, 'Страницы')
      if pages_src_domain:
        pages_count = await _copy_pages_from_domain(db, pages_src_domain, domain_id, errors)
      else:
        pages_count = await _apply_base_pages(db, domain_id, errors)
      _check(errors)

      if demo and mode == 'new':
        # Демо-контент — только для нового проекта (в клоне данные идут через copy_data,
        # иначе ds_* скопировались бы дважды).
        id_map = await _copy_ds_tables(db, data_pid, project_id, warnings)
        await _copy_chpu(db, data_pid, project_id, id_map, warnings)
        await _copy_promo(db, data_pid, project_id, warnings)
        created['dirs'] = await _copy_files(
          _copy_pairs(data_pid, project_id, None, None), warnings)

    if mode == 'base' and copy_data:
      await ctx.progress(86, 'Копируем данные проекта')
      await _copy_common_tables(db, src_pid, project_id, warnings)
      created['struct_tables'] = await _copy_struct_tables(db, src_pid, project_id, warnings)
      id_map = await _copy_ds_tables(db, src_pid, project_id, warnings)
      await _copy_chpu(db, src_pid, project_id, id_map, warnings)
      await _copy_promo(db, src_pid, project_id, warnings)
      await ctx.progress(92, 'Копируем файлы')
      created['dirs'] = await _copy_files(
        _copy_pairs(src_pid, project_id, None if clone_ds else domain, src.get('src_folder')), warnings)

    if mode == 'new':
      # Новый проект: гарантируем существование каталогов проекта (файлы не копируем).
      await ctx.progress(90, 'Создаём каталоги')
      created['dirs'] = (created.get('dirs') or []) + await _make_dirs(project_id, domain, warnings)

  except Exception as e:
    rollback_errors = await _rollback(db, created)
    message = str(e) or 'неизвестная ошибка'
    if rollback_errors:
      message += ' | откат неполный: %s' % '; '.join(str(x) for x in rollback_errors)
    raise CreateError(message)

  await ctx.progress(100, 'Готово')
  return {
    'success': True,
    'errors': [],
    'warnings': warnings,
    'mode': mode,
    'header': header,
    'domain': domain,
    'project_id': project_id,
    'domain_id': domain_id,
    'template_id': new_template_id,
    'is_constructor': is_constructor,
    'login': login,
    'password': password,
    'port': port,
    'server_type': server_type,
    'pages': pages_count,
    'source_project_id': src_pid,
  }


register_task('svcmsadmin', 'project_create', run_project_create)
