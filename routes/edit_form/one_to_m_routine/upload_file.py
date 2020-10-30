from lib.core import get_child_field, exists_arg, get_ext, random_filename
from lib.get_1_to_m_data import get_1_to_m_data
import shutil,os

def upload_file(form,field,arg):
  child_field_name=arg['child_field_name']
  child_field=get_child_field(field,child_field_name)
  if not child_field:
    form.errors.append(f'не найдено поле {child_field_name} в {field["name"]} обратитесь к разработчику')
  

  if form.success():
    oldfile=form.db.query(
      query=f'SELECT {child_field["name"]} from {field["table"]} WHERE {field["foreign_key"]}=%s and {field["table_id"]}=%s',
      values=[form.id,arg["one_to_m_id"] ],
      onevalue=1,
      debug=1,
      errors=form.errors
    )
  
  if form.success() and oldfile:


    oldfile_arr=oldfile.split(':')
    if len(oldfile_arr)==2:
      oldfile=oldfile_arr[1]

    os.remove(child_field['filedir']+'/'+oldfile)

  # сохраняем файл
  if form.success():
    attach=arg['attach']
    orig_filename=attach.filename

    ext=get_ext(orig_filename)
    filename_without_ext=random_filename()
    filename=filename_without_ext+'.'+ext
    with open(child_field['filedir']+'/'+filename, "wb") as buffer:
       shutil.copyfileobj(attach.file, buffer)

    db_value=filename
    if exists_arg('keep_orig_filename',child_field):
      db_value+=";"+orig_filename

    form.db.save(
      table=field['table'],
      update=1,
      where=f'{field["foreign_key"]}={form.id} and {field["table_id"]}={arg["one_to_m_id"]}',
      data={
        child_field['name']: db_value
      }
    )


  get_1_to_m_data(form,field)
  return {
    'success':form.success(),
    'errors':form.errors,
    'values':exists_arg('value',field)
  }

