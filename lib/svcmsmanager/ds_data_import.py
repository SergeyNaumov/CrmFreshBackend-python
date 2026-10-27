# Импорт данных DS-проекта из переносимого архива (svcms manager).
#
# Архив собирает ds_data_export.py: manifest.json + data/<table>.json + files/.
# project_id в данных нет -- берётся целевой проект (по хосту запроса).
# Исходные id строк не вставляются: в другом проекте AUTO_INCREMENT другой,
# поэтому ссылки (refs) ремапятся по карте src_id -> новый id.
#
# Режимы:
#   replace -- очистить строки выбранных таблиц проекта и вставить из архива;
#   merge   -- вставить/обновить без удаления, поиск существующих строк -- по
#              «натуральному» ключу таблицы (natural_key), иначе вставка.
# Файлы в обоих режимах накладываются поверх: новые копируются, совпадающие
# пропускаются; в merge отличающиеся существующие не перезаписываются
# (в stats.files.conflicts), в replace -- перезаписываются.
#
# Весь импорт -- одна транзакция; файлы переносятся в проект только после
# COMMIT, при ошибке -- откат БД и удаление временных файлов.
#
# Фоновая задача: register_task('svcmsmanager','project_import', run_import).

import datetime
import hashlib
import json
import os
import re
import zipfile

from lib.background import register_task
from lib.svcmsmanager.ds_data_transfer import (
  API_CONST_EXCLUDE, FORMAT, FORMAT_VERSION, IMPORT_PREFIX, TMP_DIR, TABLES,
  is_service, project_dir, sorted_tables, table_pk, table_title,
)

CHUNK = 1 << 20


def _member_ok(name):
  # Защита от zip-slip: без абсолютных путей и выходов наружу
  if not name or name.startswith(('/', '\\')) or re.match(r'^[A-Za-z]:', name):
    return False
  return '..' not in re.split(r'[/\\]', name)


def read_archive(zip_path):
  # -> (manifest, data, files, errors). data: {table: {columns, rows}}
  errors = []
  if not os.path.isfile(zip_path):
    return None, {}, [], ['архив не найден']
  try:
    zf = zipfile.ZipFile(zip_path)
  except (zipfile.BadZipFile, OSError) as e:
    return None, {}, [], [f'не удалось открыть архив: {e}']

  with zf:
    names = zf.namelist()
    bad = [n for n in names if not _member_ok(n)]
    if bad:
      return None, {}, [], [f'недопустимый путь в архиве: {bad[0]}']

    try:
      manifest = json.loads(zf.read('manifest.json').decode('utf-8'))
    except Exception:
      return None, {}, [], ['архив повреждён: нет manifest.json']

    if manifest.get('format') != FORMAT:
      return None, {}, [], [f'неизвестный формат архива: {manifest.get("format")}']
    try:
      version = int(manifest.get('format_version') or 0)
    except (TypeError, ValueError):
      version = 0
    if not (1 <= version <= FORMAT_VERSION):
      return None, {}, [], [f'неподдерживаемая версия формата: {version}']

    data = {}
    for n in names:
      if n.startswith('data/') and n.endswith('.json'):
        try:
          body = json.loads(zf.read(n).decode('utf-8'))
        except Exception:
          errors.append(f'не удалось прочитать {n}')
          continue
        table = body.get('table') or n[5:-5]
        data[table] = {
          'columns': [c for c in (body.get('columns') or []) if c != 'id'],
          'rows': body.get('rows') or [],
        }
    if not data:
      errors.append('в архиве нет данных (нет data/*.json)')

    files = [i for i in zf.infolist() if i.filename.startswith('files/') and not i.is_dir()]

  return manifest, data, files, errors


async def _columns(cur, table):
  # -> {колонка: {'type':..., 'notnull':...}}; типы нужны для дат и значений по умолчанию
  await cur.execute(f'SHOW COLUMNS FROM `{table}`')
  out = {}
  for row in await cur.fetchall():
    name, typ = row[0], (row[1] or '').lower()
    out[name] = {'type': typ, 'notnull': str(row[2]).upper() == 'NO'}
  return out


def _is_date_type(typ):
  return typ.startswith(('date', 'datetime', 'timestamp'))


def _is_numeric_type(typ):
  return typ.startswith(('int', 'tiny', 'small', 'medium', 'bigint', 'decimal', 'float', 'double'))


def _to_date(value, typ):
  if not isinstance(value, str) or not value:
    return value
  try:
    if typ.startswith('date') and not typ.startswith('datetime'):
      return datetime.date.fromisoformat(value[:10])
    return datetime.datetime.fromisoformat(value)
  except ValueError:
    return None


def _topo_order(rows, pk, parent_col):
  # Родители (parent_col is NULL/0/неизвестен) вставляются раньше детей --
  # иначе FK не пропустит ребёнка. Циклы в данных выкидываем как есть.
  by_id = {}
  for r in rows:
    v = r.get(pk)
    if v is not None and v not in by_id:
      by_id[v] = r
  emitted = set()
  out = []
  pending = list(rows)
  while pending:
    rest = []
    progress = False
    for r in pending:
      p = r.get(parent_col)
      if not p or p not in by_id or p in emitted:
        out.append(r)
        if r.get(pk) is not None:
          emitted.add(r.get(pk))
        progress = True
      else:
        rest.append(r)
    if not progress:
      out.extend(rest)
      break
    pending = rest
  return out


async def build_plan(db, project_id, zip_path):
  # Dry-run: что произойдёт при импорте. Ничего не пишет.
  manifest, data, files, errors = read_archive(zip_path)
  if errors:
    return {'success': 0, 'errors': errors}

  src_pid = int(manifest.get('source_project_id') or 0)
  warnings = []
  unknown = [t for t in data if t not in TABLES]
  for t in unknown:
    warnings.append(f'таблица {t} не поддерживается и будет пропущена')

  # ссылки на таблицы, которых нет в архиве
  selected = set(data) & set(TABLES)
  for t in sorted(selected):
    for col, ref in (TABLES[t].get('refs') or {}).items():
      if ref not in selected and ref != t:
        warnings.append(f'{t}.{col} ссылается на {ref}, которого нет в архиве '
                        '-- значения будут сброшены')

  tables = []
  conn = await db.pool.acquire()
  try:
    async with conn.cursor() as cur:
      for name in sorted_tables(data):
        meta = TABLES[name]
        cols = await _columns(cur, name)
        if not cols:
          warnings.append(f'таблица {name} отсутствует в базе -- будет пропущена')
          continue
        where = meta.get('where_tpl') or 'project_id=%s'
        await cur.execute(f'SELECT COUNT(*) FROM `{name}` WHERE {where}', (project_id,))
        row = await cur.fetchone()
        nk = meta.get('natural_key')
        tables.append({
          'table': name,
          'title': table_title(name),
          'rows_archive': len(data[name]['rows']),
          'rows_project': row[0] if row else 0,
          'natural_key': nk,
          'service': is_service(name),
          'has_project_col': meta.get('project_col', 'project_id') == 'project_id',
        })
  finally:
    conn.close()

  # статистика файлов (по размеру; md5 считается уже при импорте)
  target = project_dir(project_id)
  target_sizes = {}
  if os.path.isdir(target):
    for dirpath, _dirs, names in os.walk(target):
      for n in names:
        full = os.path.join(dirpath, n)
        try:
          target_sizes[os.path.relpath(full, target).replace(os.sep, '/')] = os.path.getsize(full)
        except OSError:
          pass
  files_missing = files_differs = 0
  for info in files:
    rel = info.filename[len('files/'):]
    if rel not in target_sizes:
      files_missing += 1
    elif target_sizes[rel] != info.file_size:
      files_differs += 1

  return {
    'success': 1,
    'errors': [],
    'manifest': {
      'format_version': manifest.get('format_version'),
      'created': manifest.get('created'),
      'source_project_id': src_pid,
    },
    'tables': tables,
    'files': {
      'count': len(files),
      'bytes': sum(i.file_size for i in files),
      'missing': files_missing,
      'differs': files_differs,
    },
    'warnings': warnings,
  }


class _Stats:
  def __init__(self):
    self.tables = {}
    self.warnings = []
    self.files = None

  def table(self, name):
    return self.tables.setdefault(name, {'inserted': 0, 'updated': 0, 'skipped': 0})

  def warn(self, msg):
    if len(self.warnings) < 100:
      self.warnings.append(msg)


async def _resolve_ref(cur, ref_table, src_id, id_maps, pid, stats):
  # src_id (из архива) -> id в целевом проекте. Цепочка: карта вставленных
  # строк -> натуральный ключ источника в целевой БД -> прямое совпадение id.
  if src_id in (None, '', 0):
    return None
  m = id_maps.setdefault(ref_table, {})
  if src_id in m:
    return m[src_id]

  meta = TABLES.get(ref_table) or {}
  nk = meta.get('natural_key')
  if nk:
    # ключ источника может состоять из ссылок -- ремапим их в значения цели
    src_row = (id_maps.get('_rows_' + ref_table) or {}).get(src_id)
    if src_row:
      key = []
      for col in nk:
        v = src_row.get(col)
        ref = (meta.get('refs') or {}).get(col)
        if ref and v:
          v = await _resolve_ref(cur, ref, v, id_maps, pid, stats)
        key.append(v)
      if all(k not in (None, '', 0) for k in key):
        pk = table_pk(ref_table)
        await cur.execute(
          f'SELECT `{pk}` FROM `{ref_table}` WHERE ' +
          ' AND '.join(f'`{c}`=%s' for c in nk) +
          (f' AND project_id={int(pid)}' if meta.get('project_col', 'project_id') == 'project_id' else ''),
          tuple(key),
        )
        row = await cur.fetchone()
        if row:
          m[src_id] = row[0]
          return row[0]

  if meta.get('project_col', 'project_id') == 'project_id':
    # прямое совпадение id -- возможно, строки того же проекта
    await cur.execute(
      f'SELECT `{table_pk(ref_table)}` FROM `{ref_table}` WHERE id=%s AND project_id=%s',
      (src_id, pid),
    )
    row = await cur.fetchone()
    if row:
      m[src_id] = row[0]
      stats.warn(f'{ref_table}: строка {src_id} не найдена в архиве, '
                 f'использовано совпадение id в проекте')
      return row[0]

  stats.warn(f'{ref_table}: ссылка на строку {src_id} не разрешена -- значение сброшено')
  m[src_id] = None
  return None


async def _insert_table(cur, table, body, pid, src_pid, mode, id_maps, stats, include_api=False):
  meta = TABLES[table]
  pk = table_pk(table)
  cols_types = await _columns(cur, table)
  if not cols_types:
    stats.warn(f'таблица {table} отсутствует в базе -- пропущена')
    return

  has_project_col = meta.get('project_col', 'project_id') == 'project_id'
  columns = [c for c in body['columns'] if c in cols_types and c != pk]
  if has_project_col:
    columns.append('project_id')
  if not columns:
    return

  rows = body['rows']
  # api_*-настройки (ключ доступа) переносим только по явному флагу
  if table == 'const' and not include_api:
    rows = [r for r in rows if not str(r.get('name') or '').lower().startswith('api_')]
  rows_by_id = {r.get(pk): r for r in rows if r.get(pk) is not None}
  id_maps['_rows_' + table] = rows_by_id

  parent_col = meta.get('parent_col')
  if parent_col and parent_col in columns:
    rows = _topo_order(rows, pk, parent_col)

  natural_key = [c for c in (meta.get('natural_key') or []) if c in columns]

  ins_sql = (f'INSERT INTO `{table}` (' +
             ', '.join(f'`{c}`' for c in columns) +
             ') VALUES (' + ', '.join(['%s'] * len(columns)) + ')')
  upd_cols = [c for c in columns if c not in natural_key]
  upd_sql = (f'UPDATE `{table}` SET ' + ', '.join(f'`{c}`=%s' for c in upd_cols) +
             f' WHERE `{pk}`=%s') if upd_cols else None

  st = stats.table(table)
  m = id_maps.setdefault(table, {})

  for r in rows:
    src_id = r.get(pk)
    vals = {}
    for c in columns:
      if c == 'project_id':
        vals[c] = pid
        continue
      v = r.get(c)
      col = cols_types.get(c) or {}
      ref = (meta.get('refs') or {}).get(c)
      if ref and v is not None:
        v = await _resolve_ref(cur, ref, v, id_maps, pid, stats)
      if isinstance(v, str) and v:
        # пути /files/project_<src>/ в текстах -> целевой проект
        v = v.replace(f'/files/project_{src_pid}/', f'/files/project_{pid}/')
        if _is_date_type(col.get('type', '')):
          v = _to_date(v, col['type'])
      if v is None and r.get(c) is not None and col.get('notnull'):
        # неразрешённая ссылка в NOT NULL колонке: значение по умолчанию
        v = 0 if _is_numeric_type(col.get('type', '')) else ''
      vals[c] = v

    # В merge ищем существующую строку по натуральному ключу, но только если он
    # полностью заполнен; иначе строка вставляется (иначе потерялись бы данные,
    # например ds_good без artikul).
    dst_id = None
    key = None
    if mode == 'merge' and natural_key:
      key = tuple(vals.get(c) for c in natural_key)
      if not all(k not in (None, '', 0) for k in key):
        key = None
    if key is not None:
      where = ' AND '.join(f'`{c}`=%s' for c in natural_key)
      if has_project_col:
        where += ' AND project_id=%s'
        params = tuple(list(key) + [pid])
      else:
        params = tuple(key)
      await cur.execute(f'SELECT `{pk}` FROM `{table}` WHERE {where} LIMIT 1', params)
      row = await cur.fetchone()
      if row:
        dst_id = row[0]
        if upd_sql:
          await cur.execute(upd_sql, [vals[c] for c in upd_cols] + [dst_id])
        st['updated'] += 1

    if dst_id is None:
      await cur.execute(ins_sql, [vals[c] for c in columns])
      dst_id = cur.lastrowid
      st['inserted'] += 1

    if src_id is not None:
      m[src_id] = dst_id

  id_maps.pop('_rows_' + table, None)


async def _copy_files(zip_path, members, pid, mode, import_id, stats):
  # Файлы распаковываются в файлы-времянки рядом с целью и подменяются только
  # после успешного сравнения; в merge отличающиеся существующие не трогаем.
  target_root = project_dir(pid)
  os.makedirs(target_root, exist_ok=True)
  tmp_suffix = f'.ds_import_{import_id}'
  tmp_files = []
  result = {'copied': 0, 'overwritten': 0, 'skipped_same': 0, 'conflicts': 0, 'bytes': 0}
  try:
    with zipfile.ZipFile(zip_path) as zf:
      for info in members:
        rel = info.filename[len('files/'):]
        dest = os.path.join(target_root, rel)
        os.makedirs(os.path.dirname(dest) or target_root, exist_ok=True)
        tmp = dest + tmp_suffix
        tmp_files.append(tmp)
        h_in = hashlib.md5()
        with zf.open(info) as src, open(tmp, 'wb') as out:
          while True:
            chunk = src.read(CHUNK)
            if not chunk:
              break
            h_in.update(chunk)
            out.write(chunk)
        result['bytes'] += info.file_size

        if not os.path.exists(dest):
          os.replace(tmp, dest)
          tmp_files.remove(tmp)
          result['copied'] += 1
          continue

        h_ex = hashlib.md5()
        with open(dest, 'rb') as f:
          while True:
            chunk = f.read(CHUNK)
            if not chunk:
              break
            h_ex.update(chunk)

        if h_in.digest() == h_ex.digest():
          os.remove(tmp)
          tmp_files.remove(tmp)
          result['skipped_same'] += 1
        elif mode == 'replace':
          os.replace(tmp, dest)
          tmp_files.remove(tmp)
          result['overwritten'] += 1
        else:
          # merge: существующий файл с другим содержимым оставляем как есть,
          # чтобы не испортить чужой контент проекта
          os.remove(tmp)
          tmp_files.remove(tmp)
          result['conflicts'] += 1
  except Exception:
    for t in tmp_files:
      try:
        os.remove(t)
      except OSError:
        pass
    raise
  return result


async def run_import(ctx):
  pid = int(ctx.params.get('project_id') or 0)
  mode = ctx.params.get('mode') or 'replace'
  import_id = str(ctx.params.get('import_id') or '')
  if not pid:
    raise ValueError('не определён проект')
  if mode not in ('replace', 'merge'):
    raise ValueError(f'неизвестный режим импорта: {mode}')
  if not re.match(r'^[a-zA-Z0-9_\-]+$', import_id):
    raise ValueError('некорректный идентификатор архива')

  zip_path = os.path.join(TMP_DIR, IMPORT_PREFIX + import_id + '.zip')
  manifest, data, files, errors = read_archive(zip_path)
  if errors:
    raise ValueError('; '.join(errors))

  src_pid = int(manifest.get('source_project_id') or 0)
  tables = [t for t in sorted_tables(data) if t in TABLES]
  include_api = bool(ctx.params.get('include_api'))
  stats = _Stats()
  id_maps = {}
  db = ctx.db

  # ---- транзакция: очистка (replace) + вставка
  conn = await db.pool.acquire()
  try:
    await conn.autocommit(False)
    async with conn.cursor() as cur:
      if mode == 'replace':
        for i, table in enumerate(reversed(tables)):
          await ctx.progress(int(5 * i / max(1, len(tables))), f'Очищаем {table}')
          meta = TABLES[table]
          if meta.get('where_tpl'):
            # ds_zakaz_good чистится каскадом от ds_zakaz; иначе -- по подзапросу
            if 'ds_zakaz' in tables:
              continue
            await cur.execute(f'DELETE FROM `{table}` WHERE {meta["where_tpl"]}', (pid,))
          else:
            where = 'project_id=%s'
            # Ключ API не должен пропасть при импорте чужого архива
            if table == 'const' and not include_api:
              where += f' AND ({API_CONST_EXCLUDE})'
            await cur.execute(f'DELETE FROM `{table}` WHERE {where}', (pid,))

      for i, table in enumerate(tables):
        await ctx.progress(5 + int(70 * i / max(1, len(tables))), f'Импортируем {table}')
        await _insert_table(cur, table, data[table], pid, src_pid, mode, id_maps, stats,
                            include_api=include_api)

    await conn.commit()
  except Exception:
    try:
      await conn.rollback()
    except Exception:
      pass
    raise
  finally:
    conn.close()

  # ---- файлы: только после COMMIT (при ошибке -- откат БД, файлы не тронуты)
  if files:
    await ctx.progress(80, 'Копируем файлы')
    stats.files = await _copy_files(zip_path, files, pid, mode, import_id, stats)

  # ---- сброс кэша клиентского сайта
  domain = ctx.params.get('domain') or ''
  if domain:
    try:
      from lib.svcmsmanager.cache_pages import clear_cache_for_domain
      clear_cache_for_domain(domain)
    except Exception as e:
      stats.warn(f'не удалось сбросить кэш: {e}')

  await ctx.progress(100, 'Готово')
  return {
    'mode': mode,
    'source_project_id': src_pid,
    'project_id': pid,
    'tables': stats.tables,
    'files': stats.files,
    'warnings': stats.warnings,
  }


register_task('svcmsmanager', 'project_import', run_import)
