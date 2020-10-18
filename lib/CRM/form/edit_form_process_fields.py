def edit_form_process_fields(form):
  for f in form.edit_form_fields:
    if f['type']=='password':
      if 'enctypt_method' in f: del( f['enctypt_method'])
      if 'method_send' in f:
        for m in f['method_send']:
          del m['code']
    elif f['type']=='file' and 'value' in f and f['value']:
      v=f['value']
      print('дописать edit_form_process_fields (process_edit_form_fields)')
