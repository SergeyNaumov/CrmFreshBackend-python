import os
import re
import asyncio
import hashlib
import subprocess
from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel

from config import config as sysconfig
from lib.background import enqueue, register_task
from .common import manager, require_permission


router = APIRouter()


def _paths():
  return sysconfig.get('paths') or {}


# Экспорт проекта -- аналог легаси api/export.pm::export_test +
# api/scripts/copy_and_create: считаем md5-каталог, запускаем bash-скрипт,
# результат -- <exported_projects>/<exp_folder>/files.tar.gz.
async def run_project_export(ctx):
  pid = int(ctx.params.get('project_id') or 0)
  if not pid:
    raise ValueError('не указан project_id')

  info = await ctx.db.query(
    query='SELECT p.project_id, d.template_id, t.folder '
          'FROM project p '
          'JOIN domain d ON d.project_id=p.project_id '
          'JOIN template t ON t.template_id=d.template_id '
          'WHERE p.project_id=%s LIMIT 1',
    values=[pid],
    onerow=1,
    errors=[],
  )
  if not info:
    raise ValueError('не найдены проект/домен/шаблон')

  template_id = info['template_id']
  folder = info['folder']
  exp_folder = hashlib.md5(
    f"{pid}{template_id}{folder}{datetime.now()}".encode()
  ).hexdigest()

  exp_root = _paths().get('exported_projects', '/var/www/sv-cms/htdocs/exported_projects')
  script = _paths().get('export_script', '/var/www/sv-cms/htdocs/admin2/api/scripts/copy_and_create')

  await ctx.progress(10, 'Запуск copy_and_create')
  cmd = ['/bin/bash', script, '-p', str(pid), '-t', str(template_id), '-f', folder, '-F', exp_folder]
  res = await asyncio.to_thread(subprocess.run, cmd, capture_output=True, text=True)
  if res.returncode != 0:
    raise ValueError(f'copy_and_create: {(res.stderr or res.stdout or "")[-400:]}')

  file_path = os.path.join(exp_root, exp_folder, 'files.tar.gz')

  exist = await ctx.db.query(
    query='SELECT count(*) FROM exported_projects WHERE project_id=%s',
    values=[pid],
    onevalue=1,
    errors=[],
  )
  if not exist:
    await ctx.db.save(
      table='exported_projects',
      data={'project_id': pid, 'file': file_path},
      errors=[],
    )

  await ctx.progress(100, 'Готово')
  return {'file': file_path, 'exp_folder': exp_folder}


# Аналог легаси api/export.pm::drop_export: удаляем запись и каталог архива.
async def run_project_export_drop(ctx):
  pid = int(ctx.params.get('project_id') or 0)
  if not pid:
    raise ValueError('не указан project_id')

  row = await ctx.db.query(
    query='SELECT file FROM exported_projects WHERE project_id=%s LIMIT 1',
    values=[pid],
    onerow=1,
    errors=[],
  )
  await ctx.db.query(
    query='DELETE FROM exported_projects WHERE project_id=%s',
    values=[pid],
    errors=[],
  )
  if row and row.get('file'):
    m = re.match(r'^(.*)/files\.tar\.gz$', row['file'])
    target = m.group(1) if m else row['file']
    await asyncio.to_thread(subprocess.run, ['rm', '-rf', target])
  return {'deleted': pid}


register_task('svcmsadmin', 'project_export', run_project_export)
register_task('svcmsadmin', 'project_export_drop', run_project_export_drop)


class ExportStart(BaseModel):
  project_id: int


@router.get('/project/export/info')
async def project_export_info(request: Request, project_id: int):
  row = await request.state.engine.db_read.query(
    query='SELECT project_id, file, created FROM exported_projects WHERE project_id=%s LIMIT 1',
    values=[project_id],
    onerow=1,
    errors=[],
  )
  return {'success': True, 'errors': [], 'export': row}


@router.post('/project/export/start')
async def project_export_start(request: Request, r: ExportStart):
  await require_permission(request, 'admin_main')
  mgr = manager(request)
  task_id = await enqueue(
    config='svcmsadmin',
    action='project_export',
    params={'project_id': r.project_id},
    admin_id=mgr.get('id'),
    project_id=r.project_id,
  )
  return {'success': True, 'errors': [], 'task_id': task_id}


@router.post('/project/export/drop')
async def project_export_drop(request: Request, r: ExportStart):
  await require_permission(request, 'admin_main')
  mgr = manager(request)
  task_id = await enqueue(
    config='svcmsadmin',
    action='project_export_drop',
    params={'project_id': r.project_id},
    admin_id=mgr.get('id'),
    project_id=r.project_id,
  )
  return {'success': True, 'errors': [], 'task_id': task_id}
