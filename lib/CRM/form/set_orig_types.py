def func_set_orig_types(form):
  for f in form.fields:
    if 'type' in f:
      T=f['type']
    else:
      form.errors.append(f"не указан type у поля {f['description']} ({f['name']}) ")
      f['type']=''
      continue
    #if f['type'].startswith('filter_'):
    #  continue
    #if f['type'] in ['text','textarea']


    #name=f['name']
    # if T in ('1_to_1_text'):
    #   f['orig_type']=f['type']
    #   f['type']='text'
    # elif T in ('1_to_1_textarea'):
    #   f['orig_type']=f['type']
    #   f['type']='textarea'
    # elif T in ('1_to_1_wysiwyg'):
    #   f['orig_type']='1_to_1_wysiwyg'
    #   f['type']='wysiwyg'

    if T in ('filter_extend_select_from_table','filter_extend_select_values','select_from_table','select_values'):
      f['orig_type']=f['type']
      if form.script=='edit_form':
        f['type']='select'