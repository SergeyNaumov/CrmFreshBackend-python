# -*- coding: utf-8 -*-
# Панель «API и интеграции» (svcms manager): управление ключом и настройками
# API управления контентом DS-сайта + статистика/журнал.
#
#   GET  /svcms/api/info            -- состояние: ключ(маска), scopes, лимиты, ping
#   POST /svcms/api/key/generate    -- новый ключ (отдаётся один раз)
#   POST /svcms/api/key/revoke      -- отозвать ключ (выключить API)
#   POST /svcms/api/settings        -- scopes / лимиты / список IP
#   GET  /svcms/api/stats?days=30   -- сводная статистика трафика API
#   GET  /svcms/api/log             -- журнал запросов
#   POST /svcms/api/log/clear       -- чистка журнала старше N дней
#   GET  /svcms/api/doc.html        -- самодостаточный HTML-файл документации
#
# Сам API живёт в движке сайта (sites/lib/api, /api/v1/...), логика настроек и
# статистики -- lib/svcmsmanager/ds_api.py, документация -- api_doc.py.

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from db import get_db
from lib.svcmsmanager import api_doc, ds_api

router = APIRouter()


def _project_id(request):
  project = getattr(request.state, 'project', None) or {}
  return int(project.get('project_id') or 0)


def _manager(request):
  return getattr(request.state, 'manager', None) or {}


def _fail(errors):
  return {'success': 0, 'errors': errors, 'data': {}}


def _ok(data=None):
  return {'success': 1, 'errors': [], 'data': data or {}}


@router.get('/api/info')
async def api_info(request: Request):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])

  db = get_db()
  host = _manager(request).get('host') or ''
  settings = await ds_api.get_settings(db, project_id)
  ping = await ds_api.ping_engine(host)
  today = await db.query(
    query='''SELECT COALESCE(SUM(requests),0) requests, COALESCE(SUM(errors),0) errors
             FROM ds_api_stat WHERE project_id=%s AND day=CURDATE()''',
    values=[project_id], onerow=1, errors=[],
  ) or {}

  return _ok({
    'project_id': project_id,
    'host': host,
    'base_url': ds_api.base_url(host),
    'settings': settings,
    'scopes': [{'code': c, 'title': ds_api.SCOPE_TITLES.get(c, c)} for c in ds_api.SCOPE_METHODS],
    'limits': {
      'batch_insert': 100,
      'select_limit': 500,
      'select_default': 50,
      'update_delete': 500,
      'tree_depth': 5,
      'file_mb': 15,
      'image_mp': 40,
    },
    'ping': ping,
    'today': {'requests': int(today.get('requests') or 0),
              'errors': int(today.get('errors') or 0)},
  })


class KeyGenerate(BaseModel):
  scopes: list = []


@router.post('/api/key/generate')
async def api_key_generate(request: Request, r: KeyGenerate):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])

  db = get_db()
  if r.scopes:
    await ds_api.save_settings(db, project_id, scopes=r.scopes)
  elif not (await ds_api.get_settings(db, project_id))['scopes']:
    # Первый ключ: по умолчанию полный доступ, чтобы интеграция заработала
    # сразу (при желании права сужаются отдельно).
    await ds_api.save_settings(db, project_id, scopes=list(ds_api.SCOPE_METHODS))
  key = await ds_api.create_key(db, project_id)
  settings = await ds_api.get_settings(db, project_id)
  return _ok({
    'key': key,           # показывается один раз
    'key_mask': settings['key_mask'],
    'settings': settings,
  })


@router.post('/api/key/revoke')
async def api_key_revoke(request: Request):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])
  db = get_db()
  await ds_api.revoke_key(db, project_id)
  return _ok({'settings': await ds_api.get_settings(db, project_id)})


class ApiSettings(BaseModel):
  scopes: list = None
  rate_limit: str = None
  rate_limit_day: str = None
  allow_ips: str = None


@router.post('/api/settings')
async def api_settings_save(request: Request, r: ApiSettings):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])
  db = get_db()
  await ds_api.save_settings(
    db, project_id,
    scopes=r.scopes,
    rate_limit=None if r.rate_limit is None else str(r.rate_limit).strip(),
    rate_limit_day=None if r.rate_limit_day is None else str(r.rate_limit_day).strip(),
    allow_ips=None if r.allow_ips is None else str(r.allow_ips).strip(),
  )
  return _ok({'settings': await ds_api.get_settings(db, project_id)})


@router.get('/api/stats')
async def api_stats(request: Request, days: int = 30):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])
  db = get_db()
  data = await ds_api.stats_summary(db, project_id, days)
  return _ok(data)


@router.get('/api/log')
async def api_log(request: Request, limit: int = 50, offset: int = 0,
                  operation: str = '', errors: int = 0):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])
  db = get_db()
  data = await ds_api.log_list(db, project_id, limit=limit, offset=offset,
                               operation=operation, errors_only=bool(errors))
  return _ok(data)


class LogClear(BaseModel):
  days: int = ds_api.LOG_KEEP_DAYS


@router.post('/api/log/clear')
async def api_log_clear(request: Request, r: LogClear = LogClear()):
  project_id = _project_id(request)
  if not project_id:
    return _fail(['проект не определён'])
  db = get_db()
  days = await ds_api.clear_log(db, project_id, r.days)
  return _ok({'kept_days': days})


@router.get('/api/doc.html', response_class=HTMLResponse)
async def api_doc_html(request: Request):
  # Документация не зависит от данных проекта -- доступна авторизованному
  # менеджеру по домену проекта.
  host = _manager(request).get('host') or ''
  return HTMLResponse(content=api_doc.doc_html(ds_api.base_url(host) or 'https://<домен>/api/v1'))
