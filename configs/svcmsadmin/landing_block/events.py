# Блок можно сохранить с привязкой к шаблону из URL (легаси after_save)
async def before_insert_landing_block(form):
  if not form.new_values.get('template_id'):
    template_id = form.param('template_id')
    if template_id:
      form.new_values['template_id'] = template_id


# Редактирование блока доступно naumov и svetlanakrash (легаси permissions)
async def permissions_landing_block(form):
  login = form.request.state.manager.get('login')
  if login in ('naumov','svetlanakrash'):
    form.read_only = 0


events = {
  'permissions': [permissions_landing_block],
  'before_insert': [before_insert_landing_block],
}
