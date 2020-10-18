from lib.all_configs import read_config

def form_update_or_insert(form):
    



    
    if form.read_only:
      form.errors.append('Вам запрещено сохранять изменения')
    else:
      form.run_event(event='before_update')
      form.run_event(event='before_insert')
      form.run_event(event='before_save')
      form.save()
      form.run_event(event='after_update')
      form.run_event(event='after_insert')
      form.run_event(event='after_save')

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
    #print('NEW_VALUES: ',values)
    return form_update_or_insert(form)
  #elif from.action == 'delete_file':form.delete_file()
  #elif form.action == 'upload_file': form.upload_file()
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
