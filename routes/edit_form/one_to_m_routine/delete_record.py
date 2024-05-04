from .delete_file import delete_file

async def delete_record(form,field,arg):
  await form.run_event('before_delete')
  #print('success:',form.success())
  if form.success():
    for cf in field['fields']:

      if cf['type'] == 'file':
        await delete_file(form,field,cf,arg['one_to_m_id'])

      if not form.success():
        break

  if form.success() and 1:
    await form.db.query(
      query=f'DELETE FROM {field["table"]} WHERE {field["foreign_key"]}=%s and {field["table_id"]}=%s',
      values=[arg['id'],arg['one_to_m_id']],
      errors=form.errors
    )

  await form.run_event('after_delete_code',{'field':field})

  return{
    'success':form.success(),
    'errors':form.errors
  }

