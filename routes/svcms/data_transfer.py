# Инструмент «Импорт / экспорт данных проекта» (svcms manager).
#
# Архив с данными таблиц DS-проекта + файлами project_<id>:
#   GET  /svcms/data/tables          -- таблицы и счётчики (для чекбоксов)
#   POST /svcms/data/export/start    -- фоновая задача project_export
#   POST /svcms/data/import/preview  -- загрузка архива + dry-run план
#   POST /svcms/data/import/start    -- фоновая задача project_import
#
# Логика -- lib/svcmsmanager/ds_data_export.py / ds_data_import.py,
# реестр таблиц -- lib/svcmsmanager/ds_data_transfer.py.
# Прогресс -- /background/status/{task_id} и WS /background/ws/{task_id}.

import os
import re
import time
import uuid

from fastapi import APIRouter, File, Request, UploadFile
from pydantic import BaseModel

from db import get_db
from lib.background import enqueue
from lib.svcmsmanager.ds_data_transfer import (
  EXPORT_PREFIX, IMPORT_PREFIX, TMP_DIR, TABLES, is_service, project_dir,
  sorted_tables, table_title,
)
# регистрирует фоновые задачи project_export / project_import
from lib.svcmsmanager import ds_data_export, ds_data_import  # noqa: F401


router = APIRouter()

# лимит загружаемого архива (запас на проекты с фото ~130МБ)
MAX_UPLOAD = 600 * 1024 * 1024


def _project_id(request):
  project = getattr(request.state, 'project', None) or {}
  return int(project.get('project_id') or 0)


def _manager(request):
  return getattr(request.state, 'manager', None) or {}


def _cleanup_tmp():
  # подчищаем архивы в files/tmp по TTL: загруженные для импорта -- через
  # сутки, готовые архивы экспорта -- через неделю. Вызывается при старте
  # экспорта и при загрузке архива (системного cron для files/tmp нет).
  if not os.path.isdir(TMP_DIR):
    return
  ttl = {
    IMPORT_PREFIX: 24 * 3600,
    EXPORT_PREFIX: 7 * 24 * 3600,
  }
  now = time.time()
  for name in os.listdir(TMP_DIR):
    if not name.endswith('.zip'):
      continue
    for prefix, seconds in ttl.items():
      if name.startswith(prefix):
        path = os.path.join(TMP_DIR, name)
        try:
          if os.path.getmtime(path) < now - seconds:
            os.remove(path)
        except OSError:
          pass
        break


class ExportStart(BaseModel):
  tables: list = []
  # Флаг «включить ключ»: по умолчанию api_*-настройки в архив не попадают
  include_api: bool = False


@router.get('/data/tables')
async def data_tables(request: Request):
  project_id = _project_id(request)
  if not project_id:
    return {'success': 0, 'errors': ['проект не определён']}

  db = get_db()
  out = []
  for name in sorted_tables(None):
    meta = TABLES[name]
    where = meta.get('where_tpl') or 'project_id=%s'
    if meta.get('exclude_tpl'):
      where += ' AND (' + meta['exclude_tpl'] + ')'
    rows = await db.query(query=f'SELECT COUNT(*) c FROM `{name}` WHERE {where}',
                          values=[project_id], onerow=1, errors=[])
    out.append({
      'table': name,
      'title': table_title(name),
      'rows': int((rows or {}).get('c') or 0),
      'natural_key': meta.get('natural_key'),
      'service': bool(is_service(name)),
    })
  return {'success': 1, 'errors': [], 'project_id': project_id, 'tables': out}


@router.post('/data/export/start')
async def data_export_start(request: Request, r: ExportStart):
  project_id = _project_id(request)
  if not project_id:
    return {'success': 0, 'errors': ['проект не определён']}

  tables = sorted_tables(r.tables)
  if not tables:
    return {'success': 0, 'errors': ['не выбраны таблицы']}

  _cleanup_tmp()
  manager = _manager(request)
  task_id = await enqueue(
    config='svcmsmanager',
    action='project_export',
    params={'project_id': project_id, 'tables': tables, 'domain': manager.get('host'),
            'include_api': bool(r.include_api)},
    admin_id=manager.get('id'),
    project_id=project_id,
  )
  return {'success': 1, 'errors': [], 'task_id': task_id}


@router.post('/data/import/preview')
async def data_import_preview(request: Request, file: UploadFile = File(...)):
  project_id = _project_id(request)
  if not project_id:
    return {'success': 0, 'errors': ['проект не определён']}
  if not (file.filename or '').lower().endswith('.zip'):
    return {'success': 0, 'errors': ['ожидается файл .zip']}

  os.makedirs(TMP_DIR, exist_ok=True)
  _cleanup_tmp()
  import_id = uuid.uuid4().hex[:20]
  path = os.path.join(TMP_DIR, IMPORT_PREFIX + import_id + '.zip')

  size = 0
  try:
    with open(path, 'wb') as out:
      while True:
        chunk = await file.read(1 << 20)
        if not chunk:
          break
        size += len(chunk)
        if size > MAX_UPLOAD:
          raise ValueError('архив слишком большой')
        out.write(chunk)
  except ValueError as e:
    try:
      os.remove(path)
    except OSError:
      pass
    return {'success': 0, 'errors': [str(e)]}
  except Exception:
    try:
      os.remove(path)
    except OSError:
      pass
    return {'success': 0, 'errors': ['не удалось сохранить архив']}

  plan = await ds_data_import.build_plan(get_db(), project_id, path)
  if not plan.get('success'):
    try:
      os.remove(path)
    except OSError:
      pass
    return plan
  plan['import_id'] = import_id
  plan['project_id'] = project_id
  return plan


class ImportStart(BaseModel):
  import_id: str
  mode: str = 'replace'
  # Флаг «включить ключ»: переносить api_*-настройки из архива
  include_api: bool = False


@router.post('/data/import/start')
async def data_import_start(request: Request, r: ImportStart):
  project_id = _project_id(request)
  if not project_id:
    return {'success': 0, 'errors': ['проект не определён']}
  if r.mode not in ('replace', 'merge'):
    return {'success': 0, 'errors': ['неизвестный режим: ' + r.mode]}
  if not re.match(r'^[a-zA-Z0-9_\-]+$', r.import_id):
    return {'success': 0, 'errors': ['некорректный идентификатор архива']}
  if not os.path.isfile(os.path.join(TMP_DIR, IMPORT_PREFIX + r.import_id + '.zip')):
    return {'success': 0, 'errors': ['архив не найден, загрузите заново']}

  manager = _manager(request)
  task_id = await enqueue(
    config='svcmsmanager',
    action='project_import',
    params={
      'project_id': project_id,
      'import_id': r.import_id,
      'mode': r.mode,
      'domain': manager.get('host'),
      'include_api': bool(r.include_api),
    },
    admin_id=manager.get('id'),
    project_id=project_id,
  )
  return {'success': 1, 'errors': [], 'task_id': task_id}
