# На создании шаблон подставляется из URL и становится доступным для правки
async def template_id_before_code(form, field):
  if form.action in ('insert','new'):
    field['read_only'] = False
  if form.action == 'new':
    template_id = form.param('template_id')
    if template_id:
      field['value'] = template_id


events = {
  'template_id': {
    'before_code': template_id_before_code,
  },
}
