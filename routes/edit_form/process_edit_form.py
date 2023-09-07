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
      if form.action in ('insert','update'):
          form.run_event('before_save')
      
      if not len(form.errors):
        form.save()
      
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
  
  if len(form.errors): return {'success':False,'errors':form.errors}

  need_fields=[]
  
  for f in form.fields:
    if not('orig_type' in f) or not re.search(r'^filter_extend_',f['orig_type']):
      need_fields.append(f)

  form.fields=need_fields
  


  
  #print("\nField:\n",field)
  #if len(form.errors): return form
  
  if form.not_create and form.action in ['insert','new']:
    form.read_only=1
  
  if form.action == 'insert' and form.not_create:
    form.errors.append('Вам запрещено создавать новые записи')
  
  #form.set_orig_types() # уже есть в all_configs.read_config
  
  # Перенёс в .lib.all_configs.read_form
  #form.run_event('permissions')
  
  #form.get_values()
  #form.run_all_before_code()
  
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
    #form.pre(form.fields[0]['value'])
    return {
      'action':form.action,
      'title':form.title,
      'success':form.success(),
      'errors':form.errors,
      'fields':form.fields,
      'id':form.id,
      'log':form.log,
      'read_only':form.read_only,
      'wide_form':(hasattr(form, 'wide_form') and form.wide_form),
      'cols':form.cols,
      'tabs':form.tabs,
      'config':form.config,
      'javascript':exists_arg('edit_form',form.javascript),
      'redirect':(hasattr(form, 'redirect') and form.redirect),
    }
