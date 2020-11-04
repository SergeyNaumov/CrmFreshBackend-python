from lib.all_configs import read_config
from lib.core import exists_arg, random_filename

import re 
def form_update_or_insert(form):
    if form.read_only:
      form.errors.append('Вам запрещено сохранять изменения')
    else:
      if form.action=='update':
          form.run_event('before_update')
      if form.action=='insert':
          form.run_event('before_insert')
      if form.action in ['insert','update']:
          form.run_event('before_save')
      form.save()
      #print('ACTION:',form.action)
      if form.action=='update':
          form.run_event('after_update')

      if form.action=='insert':
          form.run_event('after_insert')

      if form.action in ['insert','update']:
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
    R=R,
    values=values,
    script='edit_form'
  )

  field=None
  if 'name' in R and R['name']:
    field=form.fields_hash[R['name']]

  #print("\nField:\n",field)
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
    form.check() # проверяем все поля в new_values
    return form_update_or_insert(form)
  
  elif form.action == 'delete_file':
    return form.DeleteFile()
  
  elif form.action == 'upload_file':
    return form.UploadFile()
    
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
