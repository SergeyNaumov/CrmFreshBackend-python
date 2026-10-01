# Значения по умолчанию из GET-параметров (легаси url_generator: value=>param(...))
async def project_id_before_code(form, field):
  project_id = form.request.query_params.get('project_id')
  if project_id:
    field['value'] = project_id


async def struct_id_before_code(form, field):
  struct_id = form.request.query_params.get('struct_id')
  if struct_id:
    field['value'] = struct_id


events = {
  'project_id': {
    'before_code': project_id_before_code,
  },
  'struct_id': {
    'before_code': struct_id_before_code,
  },
}
