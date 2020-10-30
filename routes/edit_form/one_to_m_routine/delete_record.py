from .delete_file import delete_file

def delete_record(form,field,arg):
  form.run_event('before_delete')
  
  if form.success():
    for cf in field['fields']:

      if cf['type'] == 'file':
        delete_file(form,field,cf,arg['one_to_m_id'])

      if not form.success():
        break

  if form.success() and 0:
    form.db.query(
      query=f'DELETE FROM {field["table"]} WHERE {field["foreign_key"]}=%s and {field["table_id"]}=%s',
      values=[arg['id'],arg['one_to_m_id']],
      errors=form.errors
    )

  form.run_event('after_delete_code',{'field':field})

  return{
    'success':form.success(),
    'errors':form.errors
  }

