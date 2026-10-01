# Редактирование статичных страниц доступно только svcomplex и alena
async def permissions_content_opt(form):
  login = form.request.state.manager.get('login')
  if login in ('svcomplex','alena'):
    form.read_only = 0
    form.make_delete = 1


events = {
  'permissions': [permissions_content_opt],
}
