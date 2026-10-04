# Глобальный каркас фоновых задач.
#
# Очередь хранится в таблице crm_background (см. db/migrate_crm_background.py).
# Воркеры запускаются внутри процессов uvicorn (main.py:startup). Захват задачи
# атомарный (UPDATE ... WHERE status=0 ORDER BY id LIMIT 1), поэтому несколько
# процессов/воркеров не выполняют одну и ту же задачу дважды.
#
# Обработчики регистрируются из роутов: register_task('svcmsadmin','project_sitemap', fn).
# ctx: db, task_id, config, action, params, admin_id, project_id, progress().
import asyncio
import json
import os
import traceback
import uuid

from lib.core import gen_pas

# (config, action) -> async def handler(ctx)
TASKS = {}

_workers = []

STATUS_NEW = 0
STATUS_RUNNING = 1
STATUS_DONE = 2
STATUS_ERROR = 3
STATUS_CANCELED = 4


def register_task(config, action, handler):
  TASKS[(config, action)] = handler


def _db():
  from db import get_db
  return get_db()


def _conf():
  from config import config
  return config


def _bg_conf():
  return (_conf().get('background') or {})


async def enqueue(*, config, action, params=None, admin_id=None, project_id=None, errors=None):
  task_id = gen_pas(40)
  await _db().save(
    table='crm_background',
    data={
      'task_id': task_id,
      'config': config,
      'action': action,
      'params': json.dumps(params or {}, ensure_ascii=False),
      'admin_id': admin_id,
      'project_id': project_id,
      'status': STATUS_NEW,
      'progress': 0,
      'message': '',
    },
    errors=errors if errors is not None else [],
  )
  return task_id


async def set_progress(task_id, progress, message=''):
  await _db().query(
    query='UPDATE crm_background SET progress=%s, message=%s, updated=NOW(), heartbeat=NOW() WHERE task_id=%s',
    values=[max(0, min(100, int(progress))), message[:512], task_id],
    errors=[],
  )


async def get_task(task_id):
  rows = await _db().query(
    query='SELECT task_id, config, action, status, progress, message, result, error, '
          'registered, started, finished FROM crm_background WHERE task_id=%s',
    values=[task_id],
    errors=[],
  )
  return rows[0] if rows else None


async def list_tasks(limit=50, admin_id=None):
  where = ''
  values = []
  if admin_id:
    where = 'WHERE admin_id=%s'
    values.append(admin_id)
  values.append(int(limit))
  return await _db().query(
    query='SELECT task_id, config, action, status, progress, message, registered, finished '
          f'FROM crm_background {where} ORDER BY id DESC LIMIT %s',
    values=values,
    errors=[],
  )


async def _finish(task_id, status, result=None, error=''):
  await _db().query(
    query='UPDATE crm_background SET status=%s, progress=%s, result=%s, error=%s, '
          'finished=NOW(), updated=NOW(), heartbeat=NOW() WHERE task_id=%s',
    values=[
      status,
      100 if status == STATUS_DONE else 0,
      json.dumps(result, ensure_ascii=False) if result is not None else None,
      (error or '')[:512],
      task_id,
    ],
    errors=[],
  )


async def _heartbeat(task_id):
  while True:
    await asyncio.sleep(20)
    await _db().query(
      query='UPDATE crm_background SET heartbeat=NOW() WHERE task_id=%s',
      values=[task_id],
      errors=[],
    )


class Ctx:
  def __init__(self, db, row):
    self.db = db
    self.id = row[0]
    self.task_id = row[1]
    self.config = row[2]
    self.action = row[3]
    raw = row[4]
    self.admin_id = row[5]
    self.project_id = row[6]
    try:
      self.params = json.loads(raw) if raw else {}
    except (TypeError, ValueError):
      self.params = {}

  async def progress(self, percent, message=''):
    await set_progress(self.task_id, percent, message)


async def _claim(db, token):
  # Атомарный захват одной задачи. worker хранит уникальный токен захвата,
  # поэтому после UPDATE мы точно находим именно свою строку.
  async with db.pool.acquire() as conn:
    async with conn.cursor() as cur:
      await cur.execute(
        'UPDATE crm_background SET status=%s, worker=%s, started=NOW(), updated=NOW(), heartbeat=NOW() '
        'WHERE status=%s ORDER BY id LIMIT 1',
        (STATUS_RUNNING, token, STATUS_NEW),
      )
      if cur.rowcount == 0:
        return None
      await cur.execute(
        'SELECT id, task_id, config, action, params, admin_id, project_id '
        'FROM crm_background WHERE worker=%s AND status=%s LIMIT 1',
        (token, STATUS_RUNNING),
      )
      return await cur.fetchone()


async def _run(db, row):
  ctx = Ctx(db, row)
  handler = TASKS.get((ctx.config, ctx.action))
  if not handler:
    await _finish(ctx.task_id, STATUS_ERROR, error=f'Нет обработчика {ctx.config}/{ctx.action}')
    return
  hb = asyncio.create_task(_heartbeat(ctx.task_id))
  try:
    result = await handler(ctx)
    await _finish(ctx.task_id, STATUS_DONE, result=result)
  except Exception as e:
    await _finish(ctx.task_id, STATUS_ERROR, error=f'{e}\n{traceback.format_exc()[:400]}')
  finally:
    hb.cancel()


async def _recover():
  stale = int(_bg_conf().get('stale_minutes', 10))
  await _db().query(
    query='UPDATE crm_background SET status=%s, worker=%s '
          'WHERE status=%s AND (heartbeat IS NULL OR heartbeat < NOW() - INTERVAL %s MINUTE)',
    values=[STATUS_NEW, '', STATUS_RUNNING, stale],
    errors=[],
  )


async def _worker_loop(poll):
  token = f'{os.getpid()}:{uuid.uuid4().hex[:12]}'
  db = _db()
  while True:
    try:
      if db and db.pool:
        row = await _claim(db, token)
        if row:
          await _run(db, row)
          continue
    except Exception as e:
      print(f'background worker error: {e}')
    await asyncio.sleep(poll)


async def start_workers():
  bg = _bg_conf()
  if not bg.get('enabled'):
    return
  poll = float(bg.get('poll', 0.5))
  count = int(bg.get('workers', 2))
  try:
    await _recover()
  except Exception as e:
    print(f'background recover error: {e}')
  global _workers
  _workers = [asyncio.create_task(_worker_loop(poll)) for _ in range(count)]
  print(f'background workers started: {count}')


def stop_workers():
  for w in _workers:
    w.cancel()
