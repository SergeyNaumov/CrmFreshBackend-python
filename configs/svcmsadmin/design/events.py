# Полный доступ у перечисленных логинов (легаси design).
async def permissions(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login in ('svcomplex', 'alena', 'zaitsev'):
    form.read_only = 0
    form.make_delete = 1


events = {
  'permissions': permissions,
}
