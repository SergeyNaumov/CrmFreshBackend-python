# Полный доступ только у логина naumov (легаси admin_group.pl).
async def permissions(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login == 'naumov':
    form.make_delete = 1
    form.read_only = 0
    form.not_create = 0


events = {
  'permissions': permissions,
}
