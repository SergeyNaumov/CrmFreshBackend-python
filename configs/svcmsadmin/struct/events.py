# Убираем \r из тела конфига перед обновлением (легаси before_update)
async def before_update_struct(form):
  body = form.new_values.get('body')
  if body:
    form.new_values['body'] = body.replace('\r','')


events = {
  'before_update': [before_update_struct],
}
