from fastapi import Request


def manager(request: Request):
  return getattr(request.state, 'manager', None) or {}


async def has_permission(request: Request, *pnames):
  """Проверка права админа по admin_permissions -> permissions.pname."""
  if not pnames:
    return True
  admin_id = manager(request).get('id')
  if not admin_id:
    return False
  rows = await request.state.engine.db_read.query(
    query='SELECT count(*) cnt FROM admin_permissions ap '
          'JOIN permissions p ON p.id = ap.permissions_id '
          'WHERE ap.admin_id=%s AND p.pname IN ({})'.format(
            ','.join(['%s'] * len(pnames))),
    values=[admin_id, *pnames],
    onevalue=1,
    errors=[],
  ) or 0
  return bool(rows)


async def require_permission(request: Request, *pnames):
  if not await has_permission(request, *pnames):
    raise PermissionError('Недостаточно прав для выполнения действия')


# Реквизиты для RKN-страниц (/soglasie, /securitypolicy, /yandex-agreement).
# Заводим запись domain_rkn каждому домену, построенному на конструкторе (DS);
# значения тянем из констант проекта (const).
RKN_CONST_MAP = {
  'orgname': ('legal_name', 'short_name', 'orgname'),
  'process_owner': ('director',),
  'inn': ('inn',),
  'ogrn': ('ogrn',),
  'ur_address': ('legal_address', 'address'),
  'address': ('fact_address', 'address'),
  'email': ('email_for_feedback', 'email'),
}


async def rkn_from_const(db, project_id):
  """Собирает реквизиты RKN из констант проекта (const)."""
  rows = await db.query(
    query='SELECT name, value FROM const WHERE project_id=%s',
    values=[project_id], errors=[],
  ) or []
  cd = {r['name']: (r['value'] or '') for r in rows}
  data = {}
  for field, keys in RKN_CONST_MAP.items():
    for k in keys:
      if cd.get(k):
        data[field] = cd[k]
        break
  return data


async def create_domain_rkn(db, domain_id, project_id=None, enable=1):
  """Заводит запись domain_rkn для домена (идемпотентно), реквизиты — из const."""
  if not domain_id:
    return
  exists = await db.query(
    query='SELECT count(*) FROM domain_rkn WHERE domain_id=%s',
    values=[domain_id], onevalue=1, errors=[],
  )
  if exists:
    return
  data = await rkn_from_const(db, project_id) if project_id else {}
  await db.query(
    query='INSERT INTO domain_rkn(domain_id, enable, orgname, process_owner, inn, '
          'ogrn, ur_address, address, email) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)',
    values=[
      domain_id, enable,
      data.get('orgname', ''), data.get('process_owner', ''), data.get('inn', ''),
      data.get('ogrn', ''), data.get('ur_address', ''), data.get('address', ''),
      data.get('email', ''),
    ],
    errors=[],
  )
