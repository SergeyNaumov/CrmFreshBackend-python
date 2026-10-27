# Экспорт данных DS-проекта в переносимый архив (svcms manager).
#
# Формат архива (FORMAT/FORMAT_VERSION -- ds_data_transfer.py):
#   manifest.json          -- версия формата, источник, счётчики
#   data/<table>.json      -- {"table":..., "columns":[...], "rows":[...]}
#   files/<путь>           -- содержимое files/project_<id> БЕЗ сегмента project_<id>
#
# project_id в строки данных не пишется: на импорте целевой проект известен
# по хосту. Исходный id строк сохраняется -- по нему при импорте ремапятся
# ссылки (rubricator_id, good_id, parent_id ...), т.к. AUTO_INCREMENT в другом
# проекте другой.
#
# Фоновая задача: register_task('svcmsmanager','project_export', run_export).

import datetime
import decimal
import json
import os
import zipfile

from lib.background import register_task
from lib.svcmsmanager.ds_data_transfer import (
  EXPORT_PREFIX, FORMAT, FORMAT_VERSION, TMP_DIR, TABLES, project_dir,
  sorted_tables, table_pk,
)


# datetime/date/Decimal -> строка (json не сериализует эти типы)
def _json_default(obj):
  if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
    return obj.isoformat(sep=' ') if isinstance(obj, datetime.datetime) else obj.isoformat()
  if isinstance(obj, decimal.Decimal):
    return float(obj)
  return str(obj)


async def _table_columns(db, table):
  rows = await db.query(query=f'SHOW COLUMNS FROM `{table}`', errors=[])
  return [r['Field'] for r in (rows or [])]


async def collect_rows(db, project_id, table, meta, include_api=False):
  # Колонка project_id в выгрузку не попадает (см. шапку файла)
  columns = await _table_columns(db, table)
  columns = [c for c in columns if not (meta.get('project_col', 'project_id') == 'project_id' and c == 'project_id')]
  where = meta.get('where_tpl') or 'project_id=%s'
  # Служебные api_*-настройки (ключ доступа) в архив по умолчанию не пишем
  if meta.get('exclude_tpl') and not include_api:
    where += ' AND (' + meta['exclude_tpl'] + ')'
  rows = await db.query(
    query=f'SELECT * FROM `{table}` WHERE {where} ORDER BY {table_pk(table)}',
    values=[project_id],
    errors=[],
  )
  # убираем project_id из строк, остальное оставляем как есть
  clean = []
  for r in (rows or []):
    clean.append({k: v for k, v in r.items() if k in columns})
  return columns, clean


def _walk_files(root):
  # (arcname, fullpath, size) -- обход files/project_<id>
  out = []
  if not os.path.isdir(root):
    return out
  for dirpath, _dirs, names in os.walk(root):
    for name in names:
      full = os.path.join(dirpath, name)
      rel = os.path.relpath(full, root)
      try:
        size = os.path.getsize(full)
      except OSError:
        continue
      out.append((f'files/{rel}'.replace(os.sep, '/'), full, size))
  return out


async def build_archive(db, project_id, tables, zip_name, progress=None, include_api=False):
  # Собирает архив; возвращает статистику. progress -- async (percent, message)
  tables = sorted_tables(tables)
  if not tables:
    raise ValueError('не выбраны таблицы для экспорта')

  zip_path = os.path.join(TMP_DIR, zip_name)
  os.makedirs(TMP_DIR, exist_ok=True)

  stats = {'tables': {}, 'files': 0, 'bytes': 0}
  manifest = {
    'format': FORMAT,
    'format_version': FORMAT_VERSION,
    'created': datetime.datetime.now().isoformat(sep=' ', timespec='seconds'),
    'source_project_id': project_id,
    'tables': {},
  }

  with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for i, table in enumerate(tables):
      meta = TABLES[table]
      if progress:
        await progress(int(10 + 60 * i / len(tables)), f'Выгружаем {table}')
      columns, rows = await collect_rows(db, project_id, table, meta, include_api=include_api)
      body = {'table': table, 'columns': columns, 'rows': rows}
      zf.writestr(f'data/{table}.json', json.dumps(body, ensure_ascii=False, default=_json_default))
      manifest['tables'][table] = {'rows': len(rows)}
      stats['tables'][table] = len(rows)

    if progress:
      await progress(80, 'Упаковываем файлы')
    files = _walk_files(project_dir(project_id))
    for arcname, full, size in files:
      zf.write(full, arcname)
    manifest['files'] = {'count': len(files), 'bytes': sum(s for _a, _f, s in files)}
    stats['files'] = len(files)
    stats['bytes'] = manifest['files']['bytes']

    zf.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=1))

  if progress:
    await progress(100, 'Готово')
  stats['file'] = zip_name
  stats['url'] = f'/download_tmp/{zip_name}'
  stats['source_project_id'] = project_id
  return stats


async def run_export(ctx):
  project_id = int(ctx.params.get('project_id') or 0)
  if not project_id:
    raise ValueError('не определён проект')
  tables = ctx.params.get('tables') or []
  include_api = bool(ctx.params.get('include_api'))
  stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
  zip_name = f'{EXPORT_PREFIX}{project_id}_{stamp}.zip'
  return await build_archive(ctx.db, project_id, tables, zip_name,
                             progress=ctx.progress, include_api=include_api)


register_task('svcmsmanager', 'project_export', run_export)
