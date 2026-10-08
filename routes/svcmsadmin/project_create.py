import asyncio
import json
import os
import random
import shutil
import string

from fastapi import APIRouter, Request
from pydantic import BaseModel

from config import config as sysconfig
from lib.password import hash_password
from .common import manager, require_permission, create_domain_rkn


router = APIRouter()

BASE_PAGES = os.path.join(os.path.dirname(__file__), 'page_constructor', 'base_pages.json')
THEME_AXES = ('color', 'style', 'layout', 'font')
THEME_DEFAULTS = {'color': 'digitalstrateg', 'style': 'soft', 'layout': 'standard', 'font': 'inter'}
BLOCKS_EMPTY = '{"schema": "svcms.page_blocks", "version": 2, "blocks": []}'


class CreateError(Exception):
  pass


def _paths():
  return sysconfig.get('paths') or {}


def _source_project_id(override=None):
  if override:
    return int(override)
  return int((sysconfig.get('fast_create') or {}).get('source_project_id') or 0)


def _check(errors):
  if errors:
    msg = errors[-1]
    errors.clear()
    raise CreateError(msg)


def _gen_password(n=8):
  return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def _load_base_pages():
  with open(BASE_PAGES, 'r', encoding='utf-8') as f:
    return json.load(f)


def _blocks_doc(value):
  """Приводит blocks страницы к формату v2 (как template_pages_base / base-pages)."""
  if value is None or value == '':
    return BLOCKS_EMPTY
  if isinstance(value, (dict, list)):
    data = value
  else:
    data = json.loads(value)
  if isinstance(data, list):
    data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': data}
  elif isinstance(data, dict) and 'blocks' not in data:
    data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': []}
  return json.dumps(data, ensure_ascii=False)


async def _theme_from_source(db, source_project_id, errors):
  theme = dict(THEME_DEFAULTS)
  if not source_project_id:
    return theme
  row = await db.query(
    query='SELECT dc.color, dc.style, dc.layout, dc.font FROM domain d '
          'JOIN domain_constructor dc ON dc.domain_id=d.domain_id '
          'WHERE d.project_id=%s LIMIT 1',
    values=[source_project_id],
    onerow=1,
    errors=errors,
  )
  _check(errors)
  if row:
    for axis in THEME_AXES:
      if row.get(axis):
        theme[axis] = row[axis]
  return theme


async def _copy_demo(db, source_project_id, project_id, warnings):
  """Копирует демо-контент ds_* из проекта-эталона (по колонке project_id)."""
  if not source_project_id:
    warnings.append('демо-контент: не задан проект-эталон')
    return
  errors = []
  tables = await db.query(
    query="SELECT table_name FROM information_schema.columns "
          "WHERE table_schema=DATABASE() AND column_name='project_id' AND table_name LIKE %s",
    values=['ds\\_%'],
    errors=errors,
  )
  _check(errors)
  for row in (tables or []):
    table = (row.get('table_name') or row.get('TABLE_NAME') or '').strip()
    if not table:
      continue
    cols = await db.query(
      query='SELECT column_name, extra FROM information_schema.columns '
            'WHERE table_schema=DATABASE() AND table_name=%s ORDER BY ordinal_position',
      values=[table],
      errors=errors,
    )
    _check(errors)
    names = []
    for c in (cols or []):
      name = c.get('column_name') or c.get('COLUMN_NAME') or ''
      extra = c.get('extra') or c.get('EXTRA') or ''
      if name and 'auto_increment' not in extra.lower():
        names.append(name)
    if not names or 'project_id' not in names:
      continue
    insert_cols = ', '.join('`%s`' % n for n in names)
    select_cols = ', '.join(str(project_id) if n == 'project_id' else '`%s`' % n for n in names)
    table_errors = []
    await db.query(
      query='INSERT INTO `%s` (%s) SELECT %s FROM `%s` WHERE project_id=%%s'
            % (table, insert_cols, select_cols, table),
      values=[source_project_id],
      errors=table_errors,
    )
    if table_errors:
      warnings.append('%s: %s' % (table, table_errors[-1]))


async def _copy_demo_files(project_id, source_project_id):
  """Копирует файлы и python-модуль проекта из эталона (по чекбоксу «демо»)."""
  paths = _paths()
  engine_root = paths.get('engine_root')
  conf_root = paths.get('conf_projects')
  pairs = []
  if engine_root:
    pairs.append((
      os.path.join(engine_root, 'files', 'project_%s' % source_project_id),
      os.path.join(engine_root, 'files', 'project_%s' % project_id),
    ))
    pairs.append((
      os.path.join(engine_root, 'projects', 'project_%s' % source_project_id),
      os.path.join(engine_root, 'projects', 'project_%s' % project_id),
    ))
  if conf_root:
    pairs.append((
      os.path.join(conf_root, 'project_%s' % source_project_id),
      os.path.join(conf_root, 'project_%s' % project_id),
    ))
  copied = []
  for src, dst in pairs:
    if not os.path.isdir(src):
      continue
    await asyncio.to_thread(
      shutil.copytree, src, dst,
      dirs_exist_ok=True,
      ignore=shutil.ignore_patterns('__pycache__'),
    )
    copied.append(dst)
  return copied


async def _rollback(db, created):
  errors = []
  project_id = created.get('project_id')
  domain_id = created.get('domain_id')
  manager_id = created.get('manager_id')
  if domain_id:
    await db.query(query='DELETE FROM domain WHERE domain_id=%s', values=[domain_id], errors=errors)
  if project_id:
    await db.query(query='DELETE FROM manager_project_access WHERE project_id=%s', values=[project_id], errors=errors)
    await db.query(query='DELETE FROM const WHERE project_id=%s', values=[project_id], errors=errors)
    await db.query(query='DELETE FROM admin_project WHERE project_id=%s', values=[project_id], errors=errors)
  if manager_id:
    await db.query(query='DELETE FROM manager WHERE manager_id=%s', values=[manager_id], errors=errors)
  if project_id:
    await db.query(query='DELETE FROM project WHERE project_id=%s', values=[project_id], errors=errors)
  for path in (created.get('dirs') or []):
    try:
      if os.path.isdir(path):
        await asyncio.to_thread(shutil.rmtree, path)
    except Exception:
      pass
  return errors


@router.get('/project/create/templates')
async def project_create_templates(request: Request):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_read
  errors = []
  templates = await db.query(
    query='SELECT template_id, header, folder, type FROM template WHERE type=6 ORDER BY header',
    errors=errors,
  ) or []
  return {
    'success': not errors,
    'errors': errors,
    'templates': templates,
    'source_project_id': _source_project_id(),
  }


class CreateIn(BaseModel):
  header: str
  domain: str
  template_id: int
  create_manager: bool = False
  login: str | None = None
  password: str | None = None
  demo: bool = False
  source_project_id: int | None = None


@router.post('/project/create/start')
async def project_create_start(request: Request, r: CreateIn):
  await require_permission(request, 'admin_main')
  db = request.state.engine.db_write
  mgr = manager(request)
  errors = []

  header = (r.header or '').strip()
  domain = (r.domain or '').strip()
  if not header:
    return {'success': False, 'errors': ['Укажите название проекта']}
  if not domain:
    return {'success': False, 'errors': ['Укажите домен']}

  tpl = await db.query(
    query='SELECT template_id, header, folder FROM template WHERE template_id=%s AND type=6',
    values=[r.template_id],
    onerow=1,
    errors=errors,
  )
  if errors:
    return {'success': False, 'errors': errors}
  if not tpl:
    return {'success': False, 'errors': ['Шаблон-конструктор (type=6) не найден']}

  dup_domain = await db.query(
    query='SELECT domain_id FROM domain WHERE domain=%s',
    values=[domain],
    onerow=1,
    errors=errors,
  )
  if errors:
    return {'success': False, 'errors': errors}
  if dup_domain:
    return {'success': False, 'errors': ['Домен %s уже используется' % domain]}

  login = ''
  password = ''
  if r.create_manager:
    login = (r.login or '').strip()
    password = (r.password or '').strip()
    if not login:
      return {'success': False, 'errors': ['Укажите логин менеджера']}
    if not password:
      password = _gen_password()
    dup_login = await db.query(
      query='SELECT manager_id FROM manager WHERE login=%s',
      values=[login],
      onerow=1,
      errors=errors,
    )
    if errors:
      return {'success': False, 'errors': errors}
    if dup_login:
      return {'success': False, 'errors': ['Менеджер с логином %s уже существует' % login]}

  source_project_id = _source_project_id(r.source_project_id)
  created = {'project_id': None, 'domain_id': None, 'manager_id': None, 'dirs': []}
  warnings = []
  pages_count = 0

  try:
    project_id = await db.save(table='project', data={'header': header, 'options': '', 'city': 0}, errors=errors)
    _check(errors)
    created['project_id'] = project_id

    await db.save(
      table='admin_project',
      data={'project_id': project_id, 'admin_id': (mgr or {}).get('id') or 0, 'type': 0},
      errors=errors,
    )
    _check(errors)

    await db.save(
      table='domain',
      data={
        'domain': domain,
        'project_id': project_id,
        'template_id': r.template_id,
        'server_type': 4,
        'not_cache_nginx': 1,
      },
      errors=errors,
    )
    _check(errors)
    drow = await db.query(
      query='SELECT domain_id FROM domain WHERE domain=%s',
      values=[domain],
      onerow=1,
      errors=errors,
    )
    _check(errors)
    domain_id = drow['domain_id']
    created['domain_id'] = domain_id

    # Константы: имена из проекта-эталона, значения пустые.
    if source_project_id:
      names = await db.query(
        query='SELECT name FROM const WHERE project_id=%s GROUP BY name',
        values=[source_project_id],
        errors=errors,
      )
      _check(errors)
      for row in (names or []):
        name = (row.get('name') or '').strip()
        if not name:
          continue
        await db.query(
          query='INSERT INTO const(name, value, project_id) VALUES(%s,%s,%s)',
          values=[name, '', project_id],
          errors=errors,
        )
        _check(errors)
    else:
      warnings.append('константы не созданы: не задан проект-эталон')

    if r.create_manager:
      manager_id = await db.save(
        table='manager',
        data={
          'login': login,
          'password': hash_password(password, sysconfig.get('encrypt_method')),
          'project_id': project_id,
        },
        errors=errors,
      )
      _check(errors)
      created['manager_id'] = manager_id
      await db.query(
        query='INSERT INTO manager_project_access(manager_id, project_id) VALUES(%s,%s)',
        values=[manager_id, project_id],
        errors=errors,
      )
      _check(errors)

    # Конструктор: тема (из эталона) + базовые страницы (template_pages_base).
    theme = await _theme_from_source(db, source_project_id, errors)
    base = _load_base_pages()
    header_blocks = json.dumps(base.get('header'), ensure_ascii=False) if base.get('header') else None
    footer_blocks = json.dumps(base.get('footer'), ensure_ascii=False) if base.get('footer') else None
    await db.query(
      query='INSERT INTO domain_constructor(domain_id, color, style, layout, font, header_blocks, footer_blocks) '
            'VALUES(%s,%s,%s,%s,%s,%s,%s)',
      values=[domain_id, theme['color'], theme['style'], theme['layout'], theme['font'], header_blocks, footer_blocks],
      errors=errors,
    )
    _check(errors)
    # RKN-страницы: заводим запись domain_rkn (обязательные /soglasie и т.п.).
    await create_domain_rkn(db, domain_id, project_id)
    base_set = await db.query(
      query='SELECT id FROM base_pages_set ORDER BY is_default DESC, sort, id LIMIT 1',
      onerow=1,
      errors=errors,
    )
    _check(errors)
    base_set_id = (base_set or {}).get('id')
    pages = await db.query(
      query='SELECT url, header, blocks FROM template_pages_base WHERE set_id=%s ORDER BY sort, url',
      values=[base_set_id],
      errors=errors,
    ) if base_set_id else []
    _check(errors)
    for page in (pages or []):
      url = (page.get('url') or '').strip()
      if not url:
        continue
      await db.query(
        query='INSERT INTO domain_page(domain_id, url, header, blocks) VALUES(%s,%s,%s,%s)',
        values=[domain_id, url, page.get('header') or '', _blocks_doc(page.get('blocks'))],
        errors=errors,
      )
      _check(errors)
      pages_count += 1

    if r.demo:
      await _copy_demo(db, source_project_id, project_id, warnings)
      created['dirs'] = await _copy_demo_files(project_id, source_project_id)

  except Exception as e:
    rollback_errors = await _rollback(db, created)
    return {
      'success': False,
      'errors': ['Ошибка создания проекта: %s' % e],
      'rolled_back': not rollback_errors,
      'rollback_errors': rollback_errors,
    }

  return {
    'success': True,
    'errors': [],
    'warnings': warnings,
    'project_id': project_id,
    'domain_id': domain_id,
    'template_id': r.template_id,
    'template_folder': tpl.get('folder'),
    'login': login,
    'password': password,
    'pages': pages_count,
    'demo': r.demo,
    'source_project_id': source_project_id,
  }
