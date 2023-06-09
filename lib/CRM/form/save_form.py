from lib.core import exists_arg, is_wt_field, from_datetime_get_date
#from routes.edit_form.multiconnect import save as multiconnect_save
from .multiconnect import save as multiconnect_save
def get_in_url(f,id):
  in_url=f['in_url'].replace('<%id%>',str(id))
  return in_url
  
def save_in_ext_url(form,f,value):
  in_url=get_in_url(f,form.id)
  if not in_url:
    return
  
  where=[f'in_url="{in_url}"']
  values=[]

  data={
    'in_url':in_url,
    'ext_url':value
  }

  if exists_arg('foreign_key',f) and  exists_arg('foreign_key_value',f):
        where.append(f'{f["foreign_key"]}={f["foreign_key_value"]}')
        
        data[f['foreign_key']]=f['foreign_key_value']
  
  where_str=' AND '.join(where)
  
  exists=form.db.get(
    table='in_ext_url',
    where=where_str,
    values=values,
    onerow=1
  )

  if exists and exists['ext_url']!=value and value:
    print('where_str:',where_str)
    print('values:',values)
    print('data:',data)
    form.db.save(
       table='in_ext_url',
       update=1,
       debug=1,
       where=where_str,
       #values=values,
       data=data
    )
  elif not(exists) and value:
    form.db.save(
        table='in_ext_url',
        debug=1,
        data=data,
    )


def save_form(form,arg):
  
  if len(form.errors): return
  save_hash={}
  print('NEW_VALUES:',form.new_values)
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
        
        if f['type'] in ['switch','checkbox','select_values','select_from_table','select'] and not v:
          v='0'

        if f['type'] in ['date','datetime'] :
          
          date_value=from_datetime_get_date(v)
          #print(f['name'],'(date_value): ',date_value)
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

        save_hash[name]=v
      

      # Если мы только создаём карточку -- пароль также разрешено сохранить
      if(f['type']=='password' and form.action=='insert'):
        if form.s.config['encrypt_method'] == 'mysql_sha2':
          save_hash[name]=form.db.query(
            query="select sha2(%s,256)",
            values=[v],
            onevalue=1
          )
  
  if form.success() and len(save_hash):
    # FOREIGN KEY
    # Для конфигов с foreign key
    if hasattr(form,'foreign_key') and form.foreign_key and hasattr(form,'foreign_key_value'):
      save_hash[form.foreign_key]=form.foreign_key_value

      
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
        #print('errors:',form.errors)

  for f in form.fields:
    name=f['name']
    if len(form.errors): break

    if exists_arg('read_only',f) or ( name not in form.new_values ):
      continue

    value=form.new_values[name]
    if f['type']=='multiconnect':
      print('!!NEW_VALUES:',value)
      if isinstance(value,list):
        multiconnect_save(form,f,value)
    elif f['type']=='in_ext_url':
        save_in_ext_url(form,f,value)



  #form.log.append('save_form не сделана')
