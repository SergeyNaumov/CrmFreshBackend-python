# Проект подставляем из URL (легаси before_code у project_id)
async def project_id_before_code(form, field):
  project_id = form.param('project_id')
  if project_id and str(project_id).isdigit():
    field['value'] = project_id


events = {
  'project_id': {
    'before_code': project_id_before_code,
  },
}
