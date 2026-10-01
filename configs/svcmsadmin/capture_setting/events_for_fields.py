# Легаси capture_setting.pl: на редактировании шаблон только для чтения
# и выводится составным заголовком; при создании подставляем template_id из запроса.
async def template_id_before_code(form, field):
  if form.action in ('edit', 'update'):
    field['read_only'] = True
    field['header_field'] = 'concat(template_id," - ",header)'
  if form.action == 'new':
    template_id = form.R.get('template_id')
    if template_id:
      field['value'] = template_id


events = {
  'template_id': {
    'before_code': template_id_before_code,
  },
}
