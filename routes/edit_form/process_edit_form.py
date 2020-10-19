from lib.all_configs import read_config
from lib.core import exists_arg, random_filename, get_ext
from lib.save_base64_file import save_base64_file
import re 
def form_update_or_insert(form):
    if form.read_only:
      form.errors.append('Вам запрещено сохранять изменения')
    else:
      form.run_event('before_update')
      form.run_event('before_insert')
      form.run_event('before_save')
      form.save()
      form.run_event('after_update')
      form.run_event('after_insert')
      form.run_event('after_save')

    return {
      'success':form.success(),
      'errors':form.errors,
      'log':form.log,
      'id':form.id
    }

def process_edit_form(**arg):
  action=arg['action']
  config=arg['config']
  R=arg['R']
  #print('GET_VALUES -1 ',action)
  values=[]
  if 'values' in R:
    values=R['values']
  if 'id' not in arg: arg['id']=''
  form=read_config(
    action=action,
    config=config,
    id=arg['id'],
    values=values,
    script='edit_form'
  )
  if len(form.errors): return form

  if form.not_create and form.action in ['insert','new']:
    form.read_only=1

  if form.action == 'insert' and form.not_create:
    form.errors.append('Вам запрещено создавать новые записи')

  form.set_orig_types()
  form.run_event('permissions')
  form.get_values()

  if form.action in ['update','insert']:
    form.new_values=values
    return form_update_or_insert(form)
  #elif from.action == 'delete_file':form.delete_file()
  
  elif form.action == 'upload_file':
    name=exists_arg('name',R)
    if not name:
      form.errors.append('не указано name')
    
    value=exists_arg('value',R)
    if not value:
      form.errors.append('не указано value')

    orig_name=exists_arg('orig_name',value)
    if not orig_name:
      form.errors.append('не указано orig_name')
    else:
      ext = get_ext(orig_name)
      if not ext: 
        form.errors.append(f'не удалось определить расщирение. orig_name: {orig_name}')


    src=exists_arg('src',value)
    if not src:
      form.errors.append('нет value.src')

    
    if not form.success():
        return {'success':0,'errors':errors}

    filename_for_out=filename_without_ext+'.'+ext

    if value:
      orig_name=value['orig_name']
      filename_without_ext=random_filename()
      crops=None
      if 'crops' in value: crops=value['crops']
      
      b64=b64_split(src)



      if b64 and not len(form.errors):
        form.errors=save_base64_file(
          form=form,
          src=b64['rez'],
          field=field,
          orig_name=orig_name,
          filename=filename_without_ext+'.'+ext
        )
      # crops...
      # value['src']
    #return form.upload_file()
  else:
    if form.action in ['new','edit']:
      if len(form.errors): form.read_only=1
    form.edit_form_process_fields()
    return {
      'title':form.title,
      'success':form.success(),
      'errors':form.errors,
      'fields':form.fields,
      'id':form.id,
      'log':form.log,
      'read_only':form.read_only,
      'width':form.width,
      'cols':form.cols,
      'config':form.config
    }
