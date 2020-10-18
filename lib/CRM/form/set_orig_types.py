def func_set_orig_types(form):
  for f in form.fields:
    type=f['type']
    if f['type'].startswith('filter_'):
      continue

    name=f['name']
    if form.action not in ['insert','update'] and type in ['select_from_table','select_values']:
      f['orig_type']=f['type']