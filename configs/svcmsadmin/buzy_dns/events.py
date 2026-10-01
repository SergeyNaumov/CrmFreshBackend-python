# Полный доступ только у логинов maxtest и naumov (легаси buzy_dns).
async def permissions(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login in ('maxtest', 'naumov'):
    form.make_delete = 1
    form.read_only = 0
    form.not_create = 0


events = {
  'permissions': permissions,
}
