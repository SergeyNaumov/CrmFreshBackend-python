# Редактировать могут только svcomplex/alena (легаси good.pl)
async def permissions_good(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login in ('svcomplex', 'alena'):
    form.read_only = 0
    form.make_delete = 1


events = {
  'permissions': [permissions_good],
}
