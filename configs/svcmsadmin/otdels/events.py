# Полный доступ у логинов timonenkova и isavnin (легаси otdels).
async def permissions(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login in ('timonenkova', 'isavnin'):
    form.make_delete = 1
    form.read_only = 0
    form.not_create = 0
  else:
    form.make_delete = 0
    form.read_only = 1
    form.not_create = 1


events = {
  'permissions': permissions,
}
