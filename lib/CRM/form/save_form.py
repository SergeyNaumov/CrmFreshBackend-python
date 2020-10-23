from lib.core import exists_arg, is_wt_field, from_datetime_get_date
from .multiconnect_save import multiconnect_save
def save_form(form,arg):
  if len(form.errors): return
  save_hash={}
  
  for f in form.fields:
     
      if exists_arg('read_only',f) or exists_arg('not_process',f):
        continue
      name=f['name']
     

      if name not in form.new_values:
        continue

      
      v=None
      if name in form.new_values:
        v=form.new_values[name]

      
      if is_wt_field(f):
        if f['type'] in ['switch','checkbox','select_values','select_from_table'] and not v:
          v='0'

        if f['type'] in ['date','datetime'] :
          
          date_value=from_datetime_get_date(v)

          if date_value:
            v=date_value
            
          else:
            empty_value=exists_arg('empty_value',f) or ''
            if form.engine == 'mysql-strong' or empty_value=='null':
              v='func:(NULL)'
            else:
              v='0000-00-00'
          
        if f['type']=='time' and not v:
          v='00:00:00'
          
        #if type in ['select_from_table','select_values'] a:
        #  continue
        #if v != None:
        
        save_hash[name]=v
  
  if len(save_hash):
    if form.id:
        where=f'{form.work_table_id}={form.id}'
        if form.work_table_foreign_key and form.work_table_foreign_key_value:
            where=where + f' AND {form.work_table_foreign_key}={form.work_table_foreign_key_value}'
        
        
        form.db.save(
          table=form.work_table,
          where=where,
          update=1,
          data=save_hash,
          errors=form.errors,
          debug=form.explain,
          log=form.log
        )
    else:
        if form.work_table_foreign_key and form.work_table_foreign_key_value:
            save_hash[form.work_table_foreign_key]=form.work_table_foreign_key_value
        
        form.id = form.db.save(
          table=form.work_table,
          data=save_hash,
          errors=form.errors,
          debug=form.explain,
          log=form.log
        )
        print('errors:',form.errors)

  for f in form.fields:
    name=f['name']
    if len(form.errors): break

    if exists_arg('read_only',f) or ( name not in form.new_values ):
      continue

    value=form.new_values[name]
    if f['type']=='multiconnect':
      if isinstance(value,list) and len(list):
        multiconnect_save(form,field)
    elif f['type']=='in_ext_url':
        save_in_ext_url(form,field,value)



  #form.log.append('save_form не сделана')