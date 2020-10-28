def func_set_orig_types(form):
  for f in form.fields:
    if not 'type' in f:
      print('Отсутствует type: ',f)
    type=f['type']
    if f['type'].startswith('filter_'):
      continue

    name=f['name']
    if type in ['select_from_table','select_values']:
      f['orig_type']=f['type']
      if form.script=='edit_form':
        f['type']='select'