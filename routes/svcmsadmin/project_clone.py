import os
import shutil
import asyncio

from fastapi import APIRouter, Request
from pydantic import BaseModel

from config import config as sysconfig
from lib.background import enqueue, register_task
from .common import manager, require_permission


router = APIRouter()

# Наборы колонок для стандартных сущностей (легаси clone_project.pl, %colz).
COLS = {
  'good': 'header,body,project_id,rubricator_id,price,specpredl,enabled,anons,photo,artikul,price2',
  'rubricator': 'header,path,parent_id,sort,project_id,anons,body,photo,enabled,specpredl',
  'news': 'header,anons,body,project_id,photo,enabled,registered,specpredl',
  'article': 'header,anons,body,project_id,registered,photo,enabled',
  'galery': 'header,body,project_id,sort,photo,anons,enabled',
  'portfolio': 'header,path,parent_id,sort,project_id,anons,body,photo,enabled,specpredl',
  'review': 'header,anons,body,project_id,registered,photo,enabled,sort',
  'service': 'header,anons,body,project_id,photo,enabled,specpredl,sort',
  'service_rubricator': 'header,path,parent_id,sort,project_id,anons,body,photo,enabled',
  'top_menu_tree': 'header,path,parent_id,sort,project_id,url,description',
  'left_menu_tree': 'header,path,parent_id,sort,project_id,url',
}


def _paths():
  return sysconfig.get('paths') or {}


def _first(row):
  return list(row.values())[0] if row else None


async def _table_columns(db, table):
  rows = await db.query(query=f'SHOW COLUMNS FROM `{table}`', errors=[])
  return {r['Field'] for r in (rows or [])}


# Клонирование проекта -- перенос легаси clone_project.pl на новый каркас.
async def run_project_clone(ctx):
  p = ctx.params or {}
  pid = int(p.get('project_id') or 0)
  new_domain = (p.get('domain') or '').strip()
  new_folder = (p.get('folder') or '').strip()
  login = (p.get('login') or '').strip()
  password = p.get('password') or ''
  if not pid or not new_domain or not new_folder:
    raise ValueError('нужны project_id, domain и folder')

  paths = _paths()
  templates_path = paths.get('templates', '/var/www/sv-cms/htdocs/templates')
  files_path = paths.get('files', './files')

  src = await ctx.db.query(
    query='SELECT p.header project_header, p.options project_options, p.city, '
          'd.template_id, t.header template_header, t.folder, t.type, t.options template_options '
          'FROM project p '
          'JOIN domain d ON d.project_id=p.project_id '
          'JOIN template t ON t.template_id=d.template_id '
          'WHERE p.project_id=%s LIMIT 1',
    values=[pid],
    onerow=1,
    errors=[],
  )
  if not src:
    raise ValueError('проект/шаблон не найдены')

  old_folder = src['folder']
  old_tid = src['template_id']

  await ctx.progress(5, 'Проверки')
  if os.path.isdir(os.path.join(templates_path, new_folder)):
    raise ValueError(f'папка {new_folder} уже существует')
  exist_domain = await ctx.db.query(
    query='SELECT count(*) FROM domain WHERE domain=%s', values=[new_domain], onevalue=1, errors=[])
  if exist_domain:
    raise ValueError('данный домен уже используется')
  if login:
    exist_login = await ctx.db.query(
      query='SELECT count(*) FROM manager WHERE login=%s', values=[login], onevalue=1, errors=[])
    if exist_login:
      raise ValueError(f'менеджер с логином {login} уже существует')

  await ctx.progress(15, 'Создаём проект')
  new_pid = await ctx.db.save(
    table='project',
    data={
      'header': f"{src['project_header']} ( clone - {pid} )",
      'options': src['project_options'],
      'city': src['city'],
    },
    errors=[],
  )

  await ctx.progress(25, 'Создаём шаблон и домен')
  new_tid = await ctx.db.save(
    table='template',
    data={
      'folder': new_folder,
      'type': src['type'],
      'header': f"{src['template_header']} ( clone - {pid} )",
      'options': src['template_options'],
    },
    errors=[],
  )
  await ctx.db.save(
    table='domain',
    data={'domain': new_domain, 'template_id': new_tid, 'project_id': new_pid},
    errors=[],
  )

  if login:
    await ctx.progress(35, 'Создаём менеджера')
    if not password:
      import random
      import string
      password = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))
    manager_id = await ctx.db.save(
      table='manager',
      data={'login': login, 'password': password, 'project_id': new_pid},
      errors=[],
    )
    await ctx.db.query(
      query='UPDATE manager SET password=encrypt(password) WHERE manager_id=%s',
      values=[manager_id],
      errors=[],
    )
    await ctx.db.query(
      query='INSERT INTO manager_project_access(manager_id, project_id) VALUES(%s, %s)',
      values=[manager_id, new_pid],
      errors=[],
    )

  await ctx.progress(45, 'Копируем константы и связи')
  await ctx.db.query(
    query='INSERT INTO template_const(template_id,header,sort,type,description) '
          f'SELECT {new_tid},header,sort,type,description FROM template_const WHERE template_id=%s',
    values=[old_tid], errors=[])
  await ctx.db.query(
    query='INSERT INTO const(name,value,project_id) '
          f'SELECT name,value,{new_pid} FROM const WHERE project_id=%s',
    values=[pid], errors=[])
  await ctx.db.query(
    query='INSERT INTO project_struct_public(project_id,struct_public_id) '
          f'SELECT {new_pid},struct_public_id FROM project_struct_public WHERE project_id=%s',
    values=[pid], errors=[])
  await ctx.db.query(
    query='INSERT INTO struct(project_id,header,table_name,body,admin_script,enabled) '
          f"SELECT {new_pid},header,replace(table_name,{pid},{new_pid}),"
          f"replace(body,{pid},{new_pid}),admin_script,enabled FROM struct WHERE project_id=%s",
    values=[pid], errors=[])
  await ctx.db.query(
    query='INSERT INTO url_run_code(header,template_id,url_regexp,run_code,sort) '
          f"SELECT header,{new_tid},url_regexp,replace(run_code,{pid},{new_pid}),sort "
          'FROM url_run_code WHERE template_id=%s',
    values=[old_tid], errors=[])
  await ctx.db.query(
    query='INSERT INTO url_rules(template_id,url_regexp,template_name,header,sort) '
          f'SELECT {new_tid},url_regexp,template_name,header,sort FROM url_rules WHERE template_id=%s',
    values=[old_tid], errors=[])

  await ctx.progress(60, 'Копируем уникальные структуры')
  struct_tables = await ctx.db.query(query=f"SHOW TABLES LIKE 'struct\\_{pid}\\_%'", errors=[])
  for row in (struct_tables or []):
    old_table = _first(row)
    new_table = old_table.replace(f'struct_{pid}', f'struct_{new_pid}')
    await ctx.db.query(query=f'CREATE TABLE `{new_table}` LIKE `{old_table}`', errors=[])
    await ctx.db.query(query=f'INSERT INTO `{new_table}` SELECT * FROM `{old_table}`', errors=[])
    cols = await _table_columns(ctx.db, new_table)
    if 'project_id' in cols:
      await ctx.db.query(
        query=f'UPDATE `{new_table}` SET project_id=%s WHERE project_id=%s',
        values=[new_pid, pid], errors=[])

  await ctx.progress(75, 'Копируем стандартные сущности')
  for table, col_list in COLS.items():
    cols = await _table_columns(ctx.db, table)
    if not cols or 'project_id' not in cols:
      continue
    use_cols = [c.strip() for c in col_list.split(',') if c.strip() in cols]
    select_cols = [str(new_pid) if c == 'project_id' else f'`{c}`' for c in use_cols]
    await ctx.db.query(
      query=f"INSERT INTO `{table}`({','.join('`' + c + '`' for c in use_cols)}) "
            f"SELECT {','.join(select_cols)} FROM `{table}` WHERE project_id=%s",
      values=[pid], errors=[])

  content_cols = await _table_columns(ctx.db, 'content')
  if content_cols and 'project_id' in content_cols:
    await ctx.db.query(
      query='INSERT INTO content(header,body,url,project_id) '
            f'SELECT header,body,url,{new_pid} FROM content WHERE project_id=%s',
      values=[pid], errors=[])

  await ctx.progress(85, 'Копируем файлы и шаблон')
  if os.path.isdir(os.path.join(templates_path, old_folder)):
    await asyncio.to_thread(
      shutil.copytree,
      os.path.join(templates_path, old_folder),
      os.path.join(templates_path, new_folder),
      dirs_exist_ok=True,
    )
  src_files = os.path.join(files_path, f'project_{pid}')
  dst_files = os.path.join(files_path, f'project_{new_pid}')
  os.makedirs(dst_files, exist_ok=True)
  if os.path.isdir(src_files):
    await asyncio.to_thread(shutil.copytree, src_files, dst_files, dirs_exist_ok=True)

  await ctx.progress(100, 'Готово')
  return {
    'project_id': new_pid,
    'template_id': new_tid,
    'domain': new_domain,
    'login': login,
    'password': password,
  }


register_task('svcmsadmin', 'project_clone', run_project_clone)


class CloneStart(BaseModel):
  project_id: int
  domain: str
  folder: str
  login: str | None = None
  password: str | None = None


@router.post('/project/clone/start')
async def project_clone_start(request: Request, r: CloneStart):
  await require_permission(request, 'admin_main')
  mgr = manager(request)
  task_id = await enqueue(
    config='svcmsadmin',
    action='project_clone',
    params={
      'project_id': r.project_id,
      'domain': r.domain,
      'folder': r.folder,
      'login': r.login or '',
      'password': r.password or '',
    },
    admin_id=mgr.get('id'),
    project_id=r.project_id,
  )
  return {'success': True, 'errors': [], 'task_id': task_id}
