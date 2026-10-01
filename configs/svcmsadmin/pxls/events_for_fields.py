# Легаси pxls.before_code: в селекте проекта показываем "id - header"
async def project_id_before_code(form, field):
  if form.script in ('admin_table', 'edit_form'):
    field['header_field'] = 'concat(project_id," - ",header)'


# Легаси pxls.filter_code для проекта
async def project_id_filter_code(form, field, row):
  project_id = row.get('wt__project_id') or ''
  header = row.get('p__header') or ''
  return f'{project_id} - {header}'


# Легаси pxls.filter_code для домена: выводим ссылкой
async def domain_filter_code(form, field, row):
  value = row.get('d__domain') or row.get('wt__domain') or ''
  if not value:
    return ''
  return f'<a href="http://{value}" target="_blank">{value}</a>'


events = {
  'project_id': {
    'before_code': project_id_before_code,
    'filter_code': project_id_filter_code,
  },
  'domain': {
    'filter_code': domain_filter_code,
  },
}
