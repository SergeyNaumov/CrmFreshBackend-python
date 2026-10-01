# Редактирование компаний доступно только svcomplex и alena
async def permissions_project_1_comp(form):
  login = form.request.state.manager.get('login')
  if login in ('svcomplex','alena'):
    form.read_only = 0
    form.make_delete = 1


events = {
  'permissions': [permissions_project_1_comp],
}
