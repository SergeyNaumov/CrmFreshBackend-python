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
