# Редактировать могут только svcomplex/alena (легаси template_group_promoblock)
async def permissions_template_group_promoblock(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if login in ('svcomplex', 'alena'):
    form.read_only = 0
    form.make_delete = 1


events = {
  'permissions': [permissions_template_group_promoblock],
}
