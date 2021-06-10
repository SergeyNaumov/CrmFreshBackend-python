def func_set_orig_types(form):
  for f in form.fields:
    if not 'type' in f:
      print('Отсутствует type: ',f)
    T=f['type']
    #if f['type'].startswith('filter_'):
    #  continue
    #if f['type'] in ['text','textarea']


    #name=f['name']
    if T in ['filter_extend_select_from_table','filter_extend_select_values','select_from_table','select_values']:
      f['orig_type']=f['type']
      if form.script=='edit_form':
        f['type']='select'