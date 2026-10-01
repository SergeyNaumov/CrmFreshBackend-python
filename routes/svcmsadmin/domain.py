from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

from .common import require_permission


router = APIRouter()

LETS_ENCRYPT_ADDR = '178.57.220.192'


# Легаси domain.pl action=lets_enctypt1: пересоздать A-записи домена
# (domain и www.domain) и увеличить dns_serial.
@router.get('/domain/{domain_id}/lets-encrypt-a')
async def domain_lets_encrypt_a(request: Request, domain_id: int):
  try:
    await require_permission(request, 'admin_main')
  except PermissionError as e:
    return {'success': False, 'errors': [str(e)]}

  db = request.state.engine.db_write
  row = await db.query(
    query='SELECT domain FROM domain WHERE domain_id=%s',
    values=[domain_id],
    onerow=1,
    errors=[],
  )
  if not row or not row.get('domain'):
    return {'success': False, 'errors': ['домен не найден']}

  domain = row['domain']
  await db.query(
    query='DELETE FROM domain_dns_records_a WHERE domain_id=%s',
    values=[domain_id],
    errors=[],
  )
  await db.query(
    query='INSERT INTO domain_dns_records_a(domain_id,sort,name,value) VALUES(%s,1,%s,%s)',
    values=[domain_id, domain, LETS_ENCRYPT_ADDR],
    errors=[],
  )
  await db.query(
    query='INSERT INTO domain_dns_records_a(domain_id,sort,name,value) VALUES(%s,2,%s,%s)',
    values=[domain_id, 'www.' + domain, LETS_ENCRYPT_ADDR],
    errors=[],
  )
  await db.query(
    query='UPDATE domain SET dns_serial=dns_serial+1 WHERE domain_id=%s',
    values=[domain_id],
    errors=[],
  )
  return RedirectResponse(url=f'/edit_form/domain/{domain_id}', status_code=303)
