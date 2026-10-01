import os
import re

from fastapi import APIRouter, Request
from pydantic import BaseModel

from lib.background import enqueue, register_task
from .common import manager, require_permission


router = APIRouter()

# Эталонные структуры относятся к проектам менеджера (struct_<pid>_<name>),
# поэтому лежат в конфигах менеджера, а не админки.
TEMPLATES_DIR = os.path.join(os.getcwd(), 'configs', 'svcmsmanager', 'struct_templates')

HEADERS = {
  'news': 'Новости',
  'article': 'Статьи',
  'rubricator': 'Рубрикатор',
  'good': 'Товары',
  'review': 'Отзывы',
  'galery': 'Галерея',
  'service': 'Услуги',
}


def _templates():
  items = []
  if os.path.isdir(TEMPLATES_DIR):
    for name in sorted(os.listdir(TEMPLATES_DIR)):
      d = os.path.join(TEMPLATES_DIR, name)
      if os.path.isfile(os.path.join(d, '__init__.py')) and os.path.isfile(os.path.join(d, 'schema.sql')):
        items.append({'name': name, 'header': HEADERS.get(name, name)})
  return items


# Создание уникальной структуры проекта по эталону из struct_templates.
# Аналог легаси create_struct.pl: таблица по schema.sql + запись в struct
# (body -- исходник нового формата, который грузит lib/all_configs.py).
async def run_project_struct(ctx):
  pid = int(ctx.params.get('project_id') or 0)
  name = ctx.params.get('structname') or ''
  if not pid or not name:
    raise ValueError('не указаны project_id/structname')

  tpl_dir = os.path.join(TEMPLATES_DIR, name)
  init_file = os.path.join(tpl_dir, '__init__.py')
  schema_file = os.path.join(tpl_dir, 'schema.sql')
  if not (os.path.isfile(init_file) and os.path.isfile(schema_file)):
    raise ValueError(f'эталон структуры {name} не найден')

  table_name = f'struct_{pid}_{name}'
  table_id = f'{table_name}_id'
  header = HEADERS.get(name, name)

  def repl(s):
    return (s
            .replace('[%project_id%]', str(pid))
            .replace('[%table_name%]', table_name)
            .replace('[%table_id%]', table_id)
            .replace('[%header%]', header.replace("'", "\\'")))

  with open(init_file, encoding='utf-8') as f:
    form_src = repl(f.read())
  with open(schema_file, encoding='utf-8') as f:
    schema_sql = repl(f.read())

  compile(form_src, f'<struct {table_name}>', 'exec')

  exist = await ctx.db.query(
    query='SELECT count(*) FROM struct WHERE project_id=%s AND table_name=%s',
    values=[pid, table_name],
    onevalue=1,
    errors=[],
  )
  if exist:
    raise ValueError(f'структура {table_name} уже существует')

  await ctx.progress(15, 'Создаём таблицу')
  for stmt in schema_sql.split(';'):
    stmt = stmt.strip()
    if stmt:
      await ctx.db.query(query=stmt, errors=[])

  await ctx.progress(60, 'Создаём каталог файлов')
  os.makedirs(os.path.join(os.getcwd(), 'files', f'project_{pid}', name), exist_ok=True)

  await ctx.progress(80, 'Регистрируем структуру')
  struct_id = await ctx.db.save(
    table='struct',
    data={
      'project_id': pid,
      'enabled': 1,
      'header': header,
      'table_name': table_name,
      'body': form_src,
      'admin_script': 'admin_table.pl',
    },
    errors=[],
  )

  await ctx.progress(100, 'Готово')
  return {'struct_id': struct_id, 'table_name': table_name, 'header': header}


register_task('svcmsadmin', 'project_struct', run_project_struct)


@router.get('/project/struct/templates')
async def struct_templates(request: Request):
  return {'success': True, 'errors': [], 'templates': _templates()}


class StructStart(BaseModel):
  project_id: int
  structname: str
  resize: list[dict] | None = None


@router.post('/project/struct/start')
async def project_struct_start(request: Request, r: StructStart):
  await require_permission(request, 'admin_main')
  mgr = manager(request)
  task_id = await enqueue(
    config='svcmsadmin',
    action='project_struct',
    params={
      'project_id': r.project_id,
      'structname': r.structname,
      'resize': r.resize or [],
    },
    admin_id=mgr.get('id'),
    project_id=r.project_id,
  )
  return {'success': True, 'errors': [], 'task_id': task_id}
