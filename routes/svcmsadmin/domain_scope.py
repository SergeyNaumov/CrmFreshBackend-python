"""Доменные данные конструктора/сайта: копирование и перенос между доменами.

Домен = сайт: тема, шапка/подвал, страницы конструктора, схемы темы и реквизиты
РКН привязаны к ``domain_id``, а не к ``project_id`` (см.
``page_constructor/TABLES.md``). У проекта может быть несколько доменов
(например, после переезда ``old.ru`` → ``new.ru``), поэтому перенос/копирование
этих данных — отдельная операция. Её используют и клонирование проекта, и
инструмент «Перенос на другой домен».

Здесь только данные БД + шаблон/файлы. Транзакций в db-слое нет, поэтому
вызывающая сторона отвечает за компенсацию (см. ``domain_sync.py``).
"""

import asyncio
import os
import shutil

from config import config as sysconfig


# Схемы темы: строки домена (domain_id > 0); строки с domain_id=0 — общие пресеты,
# их не копируем и не переносим.
DOMAIN_THEME_TABLES = (
  'domain_theme_color', 'domain_theme_style', 'domain_theme_layout', 'domain_theme_font',
)

# Таблицы, где ключ — domain_id (одна строка на домен): upsert.
DOMAIN_ROW_TABLES = ('domain_rkn', 'for_robots_id')

# Таблицы-«списки» с автоинкрементным id: копируются вставкой (replace — с
# предварительной очисткой приёмника).
DOMAIN_LIST_TABLES = (
  'project_hosting',
  'domain_dns_records_a', 'domain_dns_records_cname', 'domain_dns_records_mx',
  'domain_dns_records_ns', 'domain_dns_records_txt',
)

# Что переносится/копируется у конструктора (DS): ключи «частей» для UI.
CONSTRUCTOR_PARTS = ('pages', 'theme', 'schemes', 'rkn')
# Что копируется у любого домена (свойства конкретного домена).
COMMON_PARTS = ('hosting', 'dns', 'robots')


def _paths():
  return sysconfig.get('paths') or {}


async def table_columns(db, table):
  """Колонки таблицы (list) либо None, если таблицы нет."""
  rows = await db.query(query='SHOW COLUMNS FROM `%s`' % table, errors=[])
  if not rows:
    return None
  return [r.get('Field') for r in rows or []]


async def domain_profile(db, domain_id):
  """Данные домена + признак конструктора (template.type=6)."""
  rows = await db.query(
    query='SELECT d.domain_id, d.domain, d.project_id, d.template_id, d.server_type, '
          'd.port, d.not_cache_nginx, t.folder, t.header template_header, t.type template_type '
          'FROM domain d JOIN template t ON t.template_id=d.template_id WHERE d.domain_id=%s',
    values=[domain_id], onerow=1, errors=[],
  )
  if not rows:
    return None
  rows['is_constructor'] = str(rows.get('template_type')) == '6'
  return rows


async def domain_counts(db, domain_id, project_id=None):
  """Сколько строк «доменных» данных у домена (для превью/результата)."""
  counts = {}
  for table in DOMAIN_THEME_TABLES:
    c = await db.query(query='SELECT COUNT(*) c FROM `%s` WHERE domain_id=%%s' % table,
                       values=[domain_id], onevalue=1, errors=[])
    counts[table] = c or 0
  for table in ('domain_page', 'domain_constructor', 'domain_rkn', 'for_robots_id'):
    c = await db.query(query='SELECT COUNT(*) c FROM `%s` WHERE domain_id=%%s' % table,
                       values=[domain_id], onevalue=1, errors=[])
    counts[table] = c or 0
  for table in DOMAIN_LIST_TABLES:
    c = await db.query(query='SELECT COUNT(*) c FROM `%s` WHERE domain_id=%%s' % table,
                       values=[domain_id], onevalue=1, errors=[])
    counts[table] = c or 0
  if project_id:
    c = await db.query(query='SELECT COUNT(*) c FROM project_struct_public WHERE project_id=%s',
                       values=[project_id], onevalue=1, errors=[])
    counts['__struct_public'] = c or 0
  return counts


async def _copy_single_row_table(db, table, src_domain, dst_domain, replace, errors):
  """Копирует строку-на-домен (domain_rkn, for_robots_id) на новый домен."""
  cols = await table_columns(db, table)
  if not cols or 'domain_id' not in cols:
    return 0
  use_cols = [c for c in cols if c != 'domain_id']
  if replace:
    await db.query(query='DELETE FROM `%s` WHERE domain_id=%%s' % table,
                   values=[dst_domain], errors=errors)
  if not use_cols:
    return 0
  await db.query(
    query='INSERT INTO `%s`(domain_id,%s) SELECT %%s,%s FROM `%s` WHERE domain_id=%%s'
          % (table, ','.join('`%s`' % c for c in use_cols),
             ','.join('`%s`' % c for c in use_cols), table),
    values=[dst_domain, src_domain], errors=errors,
  )
  return 1


async def copy_domain_lists(db, src_domain, dst_domain, parts=None, replace=True, errors=None):
  """Копирует доменные «списки»: hosting и DNS-записи."""
  parts = parts or (COMMON_PARTS,)
  errors = errors if errors is not None else []
  result = {}
  for table in DOMAIN_LIST_TABLES:
    if table == 'project_hosting' and 'hosting' not in parts:
      continue
    if table.startswith('domain_dns_records_') and 'dns' not in parts:
      continue
    cols = await table_columns(db, table)
    if not cols or 'domain_id' not in cols:
      continue
    use_cols = [c for c in cols if c != 'domain_id' and c != 'id']
    if replace:
      await db.query(query='DELETE FROM `%s` WHERE domain_id=%%s' % table,
                     values=[dst_domain], errors=errors)
    if not use_cols:
      continue
    await db.query(
      query='INSERT INTO `%s`(domain_id,%s) SELECT %%s,%s FROM `%s` WHERE domain_id=%%s'
            % (table, ','.join('`%s`' % c for c in use_cols),
               ','.join('`%s`' % c for c in use_cols), table),
      values=[dst_domain, src_domain], errors=errors,
    )
    result[table] = True
  return result


async def copy_domain_constructor(db, src_domain, dst_domain, parts=None,
                                  pages_mode='replace', errors=None):
  """Копирует конструктор домена (страницы/тему/схемы/РКН) на другой домен.

  pages_mode: 'replace' — страницы приёмника заменить, 'merge' — только добавить
  отсутствующие по url.
  """
  parts = parts or CONSTRUCTOR_PARTS
  errors = errors if errors is not None else []
  result = {'pages': 0, 'theme': 0, 'schemes': 0, 'rkn': 0}

  if 'pages' in parts:
    pcols = await table_columns(db, 'domain_page')
    if pcols and 'domain_id' in pcols:
      if pages_mode != 'merge':
        await db.query(query='DELETE FROM domain_page WHERE domain_id=%s',
                       values=[dst_domain], errors=errors)
      ignore = ' IGNORE' if pages_mode == 'merge' else ''
      await db.query(
        query='INSERT%s INTO domain_page(domain_id,url,header,blocks) '
              'SELECT %%s,url,header,blocks FROM domain_page WHERE domain_id=%%s' % ignore,
        values=[dst_domain, src_domain], errors=errors,)
      c = await db.query(query='SELECT COUNT(*) c FROM domain_page WHERE domain_id=%s',
                         values=[dst_domain], onevalue=1, errors=[])
      result['pages'] = c or 0

  if 'theme' in parts:
    if 'domain_constructor' in (await _tables_present(db)):
      await db.query(query='DELETE FROM domain_constructor WHERE domain_id=%s',
                     values=[dst_domain], errors=errors)
      await db.query(
        query='INSERT INTO domain_constructor(domain_id,color,style,layout,font,'
              'color_css,style_css,layout_css,font_css,header_blocks,footer_blocks,base_set_id) '
              'SELECT %s,color,style,layout,font,color_css,style_css,layout_css,font_css,'
              'header_blocks,footer_blocks,base_set_id FROM domain_constructor WHERE domain_id=%s',
        values=[dst_domain, src_domain], errors=errors,)
      result['theme'] = 1

  if 'schemes' in parts:
    for table in DOMAIN_THEME_TABLES:
      cols = await table_columns(db, table)
      if not cols or 'domain_id' not in cols:
        continue
      use_cols = [c for c in cols if c != 'domain_id']
      await db.query(query='DELETE FROM `%s` WHERE domain_id=%%s' % table,
                     values=[dst_domain], errors=errors)
      await db.query(
        query='INSERT IGNORE INTO `%s`(domain_id,%s) SELECT %%s,%s FROM `%s` WHERE domain_id=%%s'
              % (table, ','.join('`%s`' % c for c in use_cols),
                 ','.join('`%s`' % c for c in use_cols), table),
        values=[dst_domain, src_domain], errors=errors,)
      c = await db.query(query='SELECT COUNT(*) c FROM `%s` WHERE domain_id=%%s' % table,
                         values=[dst_domain], onevalue=1, errors=[])
      result['schemes'] += c or 0

  if 'rkn' in parts:
    result['rkn'] = await _copy_single_row_table(db, 'domain_rkn', src_domain, dst_domain, True, errors)

  return result


async def _tables_present(db):
  rows = await db.query(
    query="SELECT table_name tn FROM information_schema.tables WHERE table_schema=DATABASE()",
    errors=[])
  return {(r.get('tn') or '') for r in rows or []}


async def move_domain_constructor(db, src_domain, dst_domain, parts=None, errors=None):
  """Переносит конструктор домена (UPDATE domain_id) на другой домен.

  Приёмник освобождается (его одноимённые строки удаляются), затем строки
  источника переезжают. Схемы темы переносятся только доменные (domain_id>0).
  """
  parts = parts or CONSTRUCTOR_PARTS
  errors = errors if errors is not None else []
  result = {'pages': 0, 'theme': 0, 'schemes': 0, 'rkn': 0}

  if 'pages' in parts:
    await db.query(query='DELETE FROM domain_page WHERE domain_id=%s', values=[dst_domain], errors=errors)
    await db.query(query='UPDATE domain_page SET domain_id=%s WHERE domain_id=%s',
                   values=[dst_domain, src_domain], errors=errors)
    result['pages'] = await db.query(query='SELECT COUNT(*) c FROM domain_page WHERE domain_id=%s',
                                     values=[dst_domain], onevalue=1, errors=[]) or 0

  if 'theme' in parts:
    await db.query(query='DELETE FROM domain_constructor WHERE domain_id=%s', values=[dst_domain], errors=errors)
    await db.query(query='UPDATE domain_constructor SET domain_id=%s WHERE domain_id=%s',
                   values=[dst_domain, src_domain], errors=errors)
    result['theme'] = 1

  if 'schemes' in parts:
    for table in DOMAIN_THEME_TABLES:
      # У приёмника своих схем быть не может с тем же header — чистим и переносим.
      await db.query(query='DELETE FROM `%s` WHERE domain_id=%%s' % table,
                     values=[dst_domain], errors=errors)
      await db.query(query='UPDATE `%s` SET domain_id=%%s WHERE domain_id=%%s' % table,
                     values=[dst_domain, src_domain], errors=errors)
      c = await db.query(query='SELECT COUNT(*) c FROM `%s` WHERE domain_id=%%s' % table,
                         values=[dst_domain], onevalue=1, errors=[])
      result['schemes'] += c or 0

  if 'rkn' in parts:
    await db.query(query='DELETE FROM domain_rkn WHERE domain_id=%s', values=[dst_domain], errors=errors)
    await db.query(query='UPDATE domain_rkn SET domain_id=%s WHERE domain_id=%s',
                   values=[dst_domain, src_domain], errors=errors)
    result['rkn'] = 1

  return result


async def delete_domain_leftovers(db, domain_id, errors=None):
  """Чистит доменные данные, у которых нет FK-каскада.

  Нужно при «переносе», если старый домен удаляется: domain_theme_* и
  for_robots_id не имеют FOREIGN KEY на domain, автоматически не исчезнут.
  """
  errors = errors if errors is not None else []
  for table in DOMAIN_THEME_TABLES + ('for_robots_id',):
    cols = await table_columns(db, table)
    if not cols or 'domain_id' not in cols:
      continue
    await db.query(query='DELETE FROM `%s` WHERE domain_id=%%s' % table,
                   values=[domain_id], errors=errors)


async def next_free_port(db):
  """Свободный порт = максимальный занятый (1..65535) + 1."""
  mx = await db.query(query='SELECT MAX(port) mx FROM domain WHERE port BETWEEN 1 AND 65535',
                      onevalue=1, errors=[])
  return int(mx or 0) + 1


async def clone_template_for_domain(db, src_domain_id, dst_domain_id, new_folder, errors=None):
  """Создаёт отдельный шаблон для нового домена (обычные, не-DS проекты).

  Копирует ``template`` (та же папка-источник не нужна, задаётся new_folder),
  ``template_const``, ``url_run_code`` (с подменой id проекта) и ``url_rules``.
  Возвращает (new_template_id, src_folder) либо (None, src_folder).
  """
  errors = errors if errors is not None else []
  src = await db.query(
    query='SELECT d.project_id, t.template_id, t.header, t.folder, t.type, t.options '
          'FROM domain d JOIN template t ON t.template_id=d.template_id WHERE d.domain_id=%s',
    values=[src_domain_id], onerow=1, errors=errors,
  )
  if not src:
    return None, None
  project_id = src.get('project_id')
  old_tid = src.get('template_id')
  new_tid = await db.save(
    table='template',
    data={
      'folder': new_folder,
      'type': src.get('type'),
      'header': src.get('header'),
      'options': src.get('options') or '',
    },
    errors=errors,
  )
  if not new_tid:
    return None, src.get('folder')
  await db.query(
    query='INSERT INTO template_const(template_id,sort,type,header,description) '
          'SELECT %s,sort,type,header,description FROM template_const WHERE template_id=%s',
    values=[new_tid, old_tid], errors=errors,)
  await db.query(
    query='INSERT INTO url_run_code(header,template_id,url_regexp,run_code,sort) '
          'SELECT header,%s,url_regexp,REPLACE(run_code,%s,%s),sort '
          'FROM url_run_code WHERE template_id=%s',
    values=[new_tid, old_tid, project_id, old_tid], errors=errors,)
  await db.query(
    query='INSERT INTO url_rules(template_id,url_regexp,template_name,header,sort) '
          'SELECT %s,url_regexp,template_name,header,sort FROM url_rules WHERE template_id=%s',
    values=[new_tid, old_tid], errors=errors,)
  await db.query(query='UPDATE domain SET template_id=%s WHERE domain_id=%s',
                 values=[new_tid, dst_domain_id], errors=errors)
  return new_tid, src.get('folder')


async def copy_template_dir(src_folder, new_folder, warnings=None):
  """Копирует папку шаблона на диске (paths.templates/<folder>)."""
  warnings = warnings if warnings is not None else []
  root = _paths().get('templates')
  if not root or not src_folder or not new_folder:
    return None
  src = os.path.join(root, src_folder)
  dst = os.path.join(root, new_folder)
  if not os.path.isdir(src):
    warnings.append('папка шаблона не найдена: %s' % src)
    return None
  try:
    await asyncio.to_thread(shutil.copytree, src, dst,
                            dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns('__pycache__'))
  except Exception as e:
    warnings.append('копирование шаблона %s: %s' % (src, e))
    return None
  return dst
