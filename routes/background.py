import asyncio

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect

from lib.background import get_task, list_tasks


router = APIRouter()

TERMINAL = (2, 3, 4)


@router.get('/status/{task_id}')
async def background_status(task_id: str, request: Request):
  task = await get_task(task_id)
  if not task:
    return {'success': False, 'errors': [f'Задача {task_id} не найдена']}
  return {'success': True, 'errors': [], 'task': task}


@router.get('/list')
async def background_list(request: Request, limit: int = 50, admin_id: int = 0):
  tasks = await list_tasks(limit=limit, admin_id=admin_id or None)
  return {'success': True, 'errors': [], 'tasks': tasks}


# WS-прогресс: сокет сам тейлит строку crm_background, поэтому работает
# при любом числе процессов-воркеров (задача могла выполниться в другом процессе).
@router.websocket('/ws/{task_id}')
async def background_ws(websocket: WebSocket, task_id: str):
  await websocket.accept()
  last = None
  try:
    while True:
      task = await get_task(task_id)
      if task is None:
        await websocket.send_json({'success': False, 'errors': [f'Задача {task_id} не найдена']})
        break
      payload = {
        'success': True,
        'task_id': task['task_id'],
        'status': task['status'],
        'progress': task['progress'],
        'message': task['message'],
        'result': task['result'],
        'error': task['error'],
      }
      if payload != last:
        last = payload
        await websocket.send_json(payload)
      if task['status'] in TERMINAL:
        break
      await asyncio.sleep(0.3)
  except WebSocketDisconnect:
    pass
  except Exception:
    pass
  finally:
    try:
      await websocket.close()
    except Exception:
      pass
