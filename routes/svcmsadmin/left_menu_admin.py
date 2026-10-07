from fastapi import Request


# Левое меню админ-панели из admin_menu_new с учётом прав.
# Права: admin_permissions (права админа) + admin_menu_permissions
# (связь пункта меню с правом, denied=0 -- давать доступ, denied=1 -- запрещать).
# Логика повторяет routes/core_routes.py:leftmenu (там manager_*), но для админки.
async def left_menu_admin(request: Request):
  s = request.state.engine
  errors = []
  manager = request.state.manager or {}
  admin_id = manager.get('id')

  permissions = await s.db.query(
    query='SELECT permissions_id FROM admin_permissions WHERE admin_id=%s',
    values=[admin_id],
    massive=1,
    errors=errors,
  ) or []
  perm_ids = [str(p) for p in permissions]
  perm_str = ','.join(perm_ids) if perm_ids else '0'

  rows = await s.db.query(
    query="""
      SELECT
        amn.id, amn.header, amn.type, amn.value, amn.params,
        amn.icon, amn.parent_id, amn.sort, amn.open,
        group_concat(concat(amp.permission_id,':',amp.denied) SEPARATOR ';') perm
      FROM
        admin_menu_new amn
        LEFT JOIN admin_menu_permissions amp ON amp.menu_id=amn.id
      WHERE
        amn.enabled=1
        AND (
          amp.id IS NULL
          OR (amp.denied=0 AND amp.permission_id IN (""" + perm_str + """))
          OR (amp.denied=1 AND amp.permission_id NOT IN (""" + perm_str + """))
        )
      GROUP BY amn.id
      ORDER BY amn.sort, amn.id
    """,
    errors=errors,
    tree_use=1,
  )

  # если таблицы ещё нет -- не роняем страницу
  if rows is None:
    rows = []

  def normalize(items):
    for item in items:
      item.pop('perm', None)
      item.pop('parent_id', None)
      if not item.get('type'):
        item['type'] = 'vue'
      if item.get('value') is None:
        item['value'] = ''
      if item.get('icon') is None:
        item['icon'] = ''
      item.setdefault('child', [])
      if item['child']:
        normalize(item['child'])
    return items

  roots = normalize(rows)

  admin = await s.db.query(
    query='select admin_id id, login, email from admin where admin_id=%s',
    values=[admin_id],
    onerow=1,
    errors=errors,
  )

  return {
    'left_menu': roots,
    'manager': admin or manager,
    'errors': errors,
    'success': not len(errors),
  }
