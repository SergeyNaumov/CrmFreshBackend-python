from lib.core import exists_arg, is_wt_field, from_datetime_get_date
#from routes.edit_form.multiconnect import save as multiconnect_save
from .multiconnect import save as multiconnect_save
def update_1_to_1(form):
  if not(form.id):
    # выходим, если нет form.id
    return

  tables_1_to_1={}
  for f in form.fields:

      if f.get('read_only'):
        continue

      #print('f:',f)
      if f['name'] in form.new_values and f['type'].startswith('1_to_1_'):
        subtype=f['type'].replace('1_to_1_','')

        if subtype in ('wysiwyg','text','textarea', 'checkbox', 'switch'):
          if not(f.get('db_name')):
            f['db_name']=f['name']

          if table:=f.get('save_table'):

            if not(table in tables_1_to_1):
              tables_1_to_1[table]={
                'foreign_key':f['foreign_key'],
                'data':None
              }

            if not(tables_1_to_1[table]['data']):

              tables_1_to_1[table]['data']=form.db.query(
                query=f"select * from {table} WHERE {f['foreign_key']}={form.id}",
                onerow=1,
                errors=form.errors
              )
              if not(tables_1_to_1[table]['data']):
                tables_1_to_1[table]['data']={
                  f['foreign_key']: form.id
                }



            value=form.new_values[f['name']]
            #if f['type'] in ('checkbox', '1_to_1')
            # новое значение в данные
            tables_1_to_1[table]['data'][f['db_name']]=value
            f['value']=form.new_values[f['name']]


          else:
            tables_1_to_1[table]['data'][f['db_name']]=v

  for table in tables_1_to_1:
    form.db.save(
      table=table,
      data=tables_1_to_1[table]['data'],
      replace=1,
      #debug=1
    )
    #print('SET 1_to_1:',tables_1_to_1[table])


def save_form(form,arg):
  
  if len(form.errors): return
  save_hash={}
  
  # для сохранения полей 1_to_1


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
          print(f"v: {v} ; date_value: {date_value}")

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
        if form.s.config['auth']['encrypt_method'] == 'mysql_sha2':
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

  update_1_to_1(form)

  for f in form.fields:
    name=f['name']
    if len(form.errors): break

    if exists_arg('read_only',f) or ( name not in form.new_values ):
      continue

    value=form.new_values[name]
    if f['type']=='multiconnect':
      #print('!!NEW_VALUES:',value)
      if isinstance(value,list):
        multiconnect_save(form,f,value)
    #elif f['type']=='1_to_1_text':
    #
    elif f['type']=='in_ext_url':
        save_in_ext_url(form,f,value)

  # события после сохранения формы
  if form.success():
    if form.action=='insert':
      form.run_event('after_insert')
      form.run_event('after_save')

    if form.action=='update':
      form.run_event('after_update')
      form.run_event('after_save')


    for f in form.fields:


      if form.action=='insert':
        form.run_event('after_insert',{'field':f})
        form.run_event('after_save',{'field':f})

      if form.action=='update':
        form.run_event('after_update',{'field':f})
        form.run_event('after_save',{'field':f})
      




  #form.log.append('save_form не сделана')
