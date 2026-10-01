# Легаси pxls.before_update: убираем символы \r из тела конфига
async def before_update_pxls(form):
  body = form.new_values.get('body')
  if isinstance(body, str):
    form.new_values['body'] = body.replace('\r', '')


events = {
  'before_update': [before_update_pxls],
}
