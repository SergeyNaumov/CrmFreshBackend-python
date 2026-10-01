# Проект в списке выводим ссылкой на карточку (легаси const.pl: filter_code).
async def project_id_filter_code(form, field, row):
  project_id = row.get('wt__project_id') or ''
  header = row.get('p__header') or ''
  if not project_id:
    return ''
  return f'<a href="/edit-form/project/{project_id}" target="_blank">{header}</a>'


events = {
  'project_id': {
    'filter_code': project_id_filter_code,
  },
}
