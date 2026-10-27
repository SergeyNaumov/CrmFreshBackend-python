# -*- coding: utf-8 -*-
"""API управления контентом DS-сайта: ключ, настройки, статистика.

Точка входа -- routes/svcms/api_keys.py (панель «API и интеграции»).
Сам API живёт в движке сайта (/api/v1/... на домене проекта, sites/lib/api),
а здесь -- управление его настройками в константах проекта и чтение статистики.

Настройки проекта (таблица const, префикс имени api_):
  api_key            -- сам ключ (24 hex-символа), хранится открытым текстом;
                        если ключа нет -- API для проекта выключено;
  api_key_created    -- дата/время создания ключа (для интерфейса);
  api_scopes         -- через запятую: select,insert,update,replace,delete,upload
                        (пусто = только select);
  api_rate_limit     -- "600/60" (запросов/секунд); движок по умолчанию берёт 600/60;
  api_rate_limit_day -- суточный лимит запросов (по умолчанию 20000);
  api_allow_ips      -- через запятую/пробел; пусто = любые IP.

Ключ наружу отдаётся один раз -- при создании; в интерфейсе и статистике
показывается только маска (9f4c…71d2). Смена настроек становится видимой
движку в пределах минуты (кеш настроек 60 с).
"""

import asyncio
import datetime
import secrets
import urllib.error
import urllib.request

# Методы API (совпадают с SCOPE_METHODS движка).
SCOPE_METHODS = ('select', 'insert', 'update', 'replace', 'delete', 'upload')
SCOPE_TITLES = {
  'select': 'Чтение (select)',
  'insert': 'Добавление (insert)',
  'update': 'Изменение (update)',
  'replace': 'Замена/upsert (replace)',
  'delete': 'Удаление (delete)',
  'upload': 'Загрузка файлов (upload)',
}

KEY_BYTES = 12          # 12 байт -> 24 hex-символа
LOG_KEEP_DAYS = 90      # срок хранения журнала по умолчанию


def generate_key():
  """Новый ключ доступа: 24 hex-символа (криптослучайные)."""
  return secrets.token_hex(KEY_BYTES)


def mask_key(key):
  """Маска ключа для интерфейса/логов: 9f4c…71d2."""
  k = str(key or '')
  if not k:
    return ''
  if len(k) <= 10:
    return k[:2] + '…'
  return f'{k[:4]}…{k[-4:]}'


def scopes_of(settings):
  raw = str((settings or {}).get('api_scopes') or '').strip()
  if not raw:
    return ['select']
  out = []
  for s in raw.replace(';', ',').split(','):
    s = s.strip().lower()
    if s and s in SCOPE_METHODS and s not in out:
      out.append(s)
  return out


def normalize_scopes(scopes):
  if isinstance(scopes, str):
    scopes = scopes.replace(';', ',').split(',')
  out = []
  for s in (scopes or []):
    s = str(s).strip().lower()
    if s in SCOPE_METHODS and s not in out:
      out.append(s)
  return out


async def get_settings(db, project_id):
  """Настройки API проекта (без самого ключа) + маска."""
  rows = await db.query(
    query='SELECT name, value FROM const WHERE project_id=%s AND name LIKE %s',
    values=[int(project_id), 'api\\_%'], errors=[],
  ) or []
  s = {r['name']: (r.get('value') or '') for r in rows}
  key = str(s.get('api_key') or '')
  return {
    'enabled': bool(key),
    'key_mask': mask_key(key),
    'created': s.get('api_key_created') or '',
    'scopes': scopes_of(s),
    'rate_limit': s.get('api_rate_limit') or '',
    'rate_limit_day': s.get('api_rate_limit_day') or '',
    'allow_ips': s.get('api_allow_ips') or '',
  }


async def set_const(db, project_id, name, value):
  """Upsert настройки в const (уникальный ключ name+project_id)."""
  await db.query(
    query='''INSERT INTO const (name, value, project_id, read_only)
             VALUES (%s, %s, %s, 0)
             ON DUPLICATE KEY UPDATE value=VALUES(value)''',
    values=[name, str(value), int(project_id)], errors=[],
  )


async def delete_const(db, project_id, name):
  await db.query(
    query='DELETE FROM const WHERE project_id=%s AND name=%s',
    values=[int(project_id), name], errors=[],
  )


async def save_settings(db, project_id, scopes=None, rate_limit=None,
                        rate_limit_day=None, allow_ips=None):
  """Сохранить настройки API (что передано -- то и пишем)."""
  if scopes is not None:
    await set_const(db, project_id, 'api_scopes', ','.join(normalize_scopes(scopes)))
  if rate_limit is not None:
    await set_const(db, project_id, 'api_rate_limit', str(rate_limit).strip())
  if rate_limit_day is not None:
    await set_const(db, project_id, 'api_rate_limit_day', str(rate_limit_day).strip())
  if allow_ips is not None:
    await set_const(db, project_id, 'api_allow_ips', str(allow_ips).strip())


async def create_key(db, project_id):
  """Сгенерировать новый ключ (старый перестаёт работать)."""
  key = generate_key()
  await set_const(db, project_id, 'api_key', key)
  await set_const(db, project_id, 'api_key_created',
                  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
  return key


async def revoke_key(db, project_id):
  """Отозвать ключ: API для проекта выключается (scopes/лимиты остаются)."""
  await delete_const(db, project_id, 'api_key')
  await delete_const(db, project_id, 'api_key_created')


def _int(v):
  try:
    return int(v or 0)
  except (TypeError, ValueError):
    return 0


def _num_row(row, day_keys=('day',)):
  out = dict(row or {})
  for k in ('requests', 'errors', 'rows_affected', 'bytes_in', 'bytes_out'):
    if k in out:
      out[k] = _int(out[k])
  for k in day_keys:
    if isinstance(out.get(k), (datetime.date, datetime.datetime)):
      out[k] = out[k].strftime('%Y-%m-%d')
  return out


async def stats_summary(db, project_id, days=30):
  """Сводка API: итоги, по дням, по методам, по сущностям, по ключам."""
  days = max(1, min(int(days or 30), 365))
  since = datetime.date.today() - datetime.timedelta(days=days - 1)
  pid = int(project_id)

  total = await db.query(
    query='''SELECT COALESCE(SUM(requests),0) requests,
                    COALESCE(SUM(errors),0) errors,
                    COALESCE(SUM(rows_affected),0) rows_affected,
                    COALESCE(SUM(bytes_in),0) bytes_in,
                    COALESCE(SUM(bytes_out),0) bytes_out,
                    MIN(day) first_day, MAX(day) last_day
             FROM ds_api_stat WHERE project_id=%s''',
    values=[pid], onerow=1, errors=[],
  ) or {}

  by_day = await db.query(
    query='''SELECT day, SUM(requests) requests, SUM(errors) errors,
                    SUM(rows_affected) rows_affected,
                    SUM(bytes_in) bytes_in, SUM(bytes_out) bytes_out
             FROM ds_api_stat WHERE project_id=%s AND day>=%s
             GROUP BY day ORDER BY day DESC''',
    values=[pid, since], errors=[],
  ) or []

  by_operation = await db.query(
    query='''SELECT operation, SUM(requests) requests, SUM(errors) errors,
                    SUM(rows_affected) rows_affected
             FROM ds_api_stat WHERE project_id=%s AND day>=%s
             GROUP BY operation ORDER BY requests DESC''',
    values=[pid, since], errors=[],
  ) or []

  by_entity = await db.query(
    query='''SELECT entity, SUM(requests) requests, SUM(errors) errors
             FROM ds_api_stat
             WHERE project_id=%s AND day>=%s AND entity<>''
             GROUP BY entity ORDER BY requests DESC LIMIT 50''',
    values=[pid, since], errors=[],
  ) or []

  by_key = await db.query(
    query='''SELECT key_mask, SUM(requests) requests, SUM(errors) errors,
                    MAX(last_ip) last_ip
             FROM ds_api_stat WHERE project_id=%s AND day>=%s
             GROUP BY key_mask ORDER BY requests DESC''',
    values=[pid, since], errors=[],
  ) or []

  return {
    'days': days,
    'total': _num_row(total),
    'by_day': [_num_row(r) for r in by_day],
    'by_operation': [_num_row(r) for r in by_operation],
    'by_entity': [_num_row(r) for r in by_entity],
    'by_key': [_num_row(r) for r in by_key],
  }


async def log_list(db, project_id, limit=50, offset=0, operation='', errors_only=False):
  """Журнал запросов (свежие сверху) + общее количество."""
  limit = max(1, min(int(limit or 50), 500))
  offset = max(0, int(offset or 0))
  where, values = ['project_id=%s'], [int(project_id)]
  if operation:
    where.append('operation=%s')
    values.append(str(operation))
  if errors_only:
    where.append('ok=0')
  wsql = ' AND '.join(where)

  total = await db.query(query=f'SELECT COUNT(*) FROM ds_api_log WHERE {wsql}',
                         values=values, onevalue=1, errors=[])
  # LIMIT/OFFSET -- уже приведённые к int числа, в тексте запроса
  rows = await db.query(
    query=f'''SELECT id, registered, ip, key_mask, operation, entity, ok,
                     error_code, error_message, ms, rows_affected,
                     bytes_in, bytes_out
              FROM ds_api_log WHERE {wsql}
              ORDER BY id DESC LIMIT {limit} OFFSET {offset}''',
    values=values, errors=[],
  ) or []
  out = []
  for r in rows:
    r = dict(r)
    if isinstance(r.get('registered'), (datetime.date, datetime.datetime)):
      r['registered'] = r['registered'].strftime('%Y-%m-%d %H:%M:%S')
    out.append(r)
  return {'total': _int(total), 'rows': out}


async def clear_log(db, project_id, days=LOG_KEEP_DAYS):
  """Удалить из журнала записи старше N дней."""
  days = max(1, int(days or LOG_KEEP_DAYS))
  cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
  await db.query(
    query='DELETE FROM ds_api_log WHERE project_id=%s AND registered<%s',
    values=[int(project_id), cutoff], errors=[],
  )
  return days


def _ping_sync(host, timeout=4):
  """Синхронный ping движка (запускается в отдельном потоке)."""
  url = f'https://{host}/api/v1/ping'
  req = urllib.request.Request(url, method='GET', headers={'Accept': 'application/json'})
  try:
    with urllib.request.urlopen(req, timeout=timeout) as resp:
      body = resp.read(2000).decode('utf-8', 'replace')
      return {'ok': 200 <= resp.status < 300, 'status': resp.status, 'url': url, 'body': body}
  except urllib.error.HTTPError as e:
    try:
      body = e.read(1000).decode('utf-8', 'replace')
    except Exception:
      body = ''
    return {'ok': False, 'status': e.code, 'url': url, 'body': body}
  except Exception as e:
    return {'ok': False, 'status': 0, 'url': url, 'body': '', 'error': str(e)}


async def ping_engine(host):
  """Проверить, отвечает ли API движка на домене проекта."""
  if not host:
    return {'ok': False, 'status': 0, 'url': '', 'body': '', 'error': 'не определён домен'}
  return await asyncio.to_thread(_ping_sync, host)


def base_url(host):
  return f'https://{host}/api/v1' if host else ''
