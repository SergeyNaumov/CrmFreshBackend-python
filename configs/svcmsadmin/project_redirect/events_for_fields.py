# Значение project_id по умолчанию из GET-параметра (легаси project_redirect)
async def project_id_before_code(form, field):
  project_id = form.request.query_params.get('project_id')
  if project_id:
    field['value'] = project_id


# Домен выводим ссылкой (легаси project_redirect, filter_code)
async def domain_filter_code(form, field, row):
  value = row.get('domain__domain') or row.get('wt__domain') or ''
  if not value:
    return ''
  return f'<a href="http://{value}" target="_blank">{value}</a>'


events = {
  'project_id': {
    'before_code': project_id_before_code,
  },
  'domain': {
    'filter_code': domain_filter_code,
  },
}
