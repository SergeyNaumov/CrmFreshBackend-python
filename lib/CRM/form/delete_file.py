import re
from lib.core import del_file_and_resizes, exists_arg
def delete_file(form,arg={}):
  # удаляет файл со всеми миниатюрами

  R=form.R
  name=R['name']
  field=None
  
  keep_str=''

  if name in form.fields_hash:
    field=form.fields_hash[name]
  else:
    return {'success':0,'errors':['name не указано или указано неверно']}

  value=form.values[name]
  
  if value:

      del_file_and_resizes(
        field=field,
        value=value
      )

      if exists_arg('keep_orig_filename_in_field',field):
        keep_str=f', {field["keep_orig_filename_in_field"]}=""'

      form.db.query(
        query=f'UPDATE {form.work_table} SET {name}="" {keep_str} WHERE {form.work_table_id}=%s',
        errors=form.errors,
        values=[form.id],
      )




  return {
    'success':form.success(),
    'errors':form.errors
  }
