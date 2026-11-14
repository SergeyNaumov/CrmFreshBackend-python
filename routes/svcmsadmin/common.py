# Реализация переехала в нейтральный lib/authz.py (общие роуты — например,
# /password — тоже должны уметь проверять права без импорта тенант-пакета).
from lib.authz import has_permission, require_permission, manager  # noqa: F401


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
