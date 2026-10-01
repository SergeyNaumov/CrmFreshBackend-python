# Полный доступ только у логина naumov (легаси admin_menu.pl).
async def permissions(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login == 'naumov':
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
