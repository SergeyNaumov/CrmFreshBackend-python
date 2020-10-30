from lib.core import exists_arg
from lib.get_1_to_m_data import normalize_value_row
from .get_data import get_data

def insert_or_update(form,field,arg):
    R=form.R
    field['values']=[]
    if not exists_arg('values',R) or not len(R['values']):
      form.errors.append('обратитесь к разработчику: в запросе отсутствуют значения (values)')
    elif not field:
      form.errors.append('обратитесь к разработчику: в запросе отсутствуют значения (values)')
    
    data=get_data(form,field)

    if form.success():

      # INSERT
      if form.action=='insert':
        form.run_event('before_insert_code',{'field':field,'data':data})
        form.run_event('before_save_code',{'field':field,'data':data})

        if form.success():
          data[field['table_id']]=form.db.save(
            table=field['table'],
            data=data,
            debug=1,
            errors=form.errors,
          )

        form.run_event('after_insert_code',{'field':field,'data':data})
        form.run_event('after_save_code',{'field':field,'data':data})    

      elif form.action=='update':
        data[field['table_id']]=arg['one_to_m_id']
        form.run_event('before_update_code',{'field':field,'data':data})
        form.run_event('before_save_code',{'field':field,'data':data})
        
        if form.success():
          data=form.db.save(
            table=field['table'],
            where=f'{field["foreign_key"]}={form.id} and {field["table_id"]}={arg["one_to_m_id"]}',
            update=1,
            errors=form.errors,
            data=data,
            debug=1
          )

          data=form.db.query(
            query=f'SELECT * from {field["table"]} WHERE {field["table_id"]}=%s',
            values=[arg["one_to_m_id"]]
          )
          if not data:
            form.errors.append('данной записи уже не существует, возможно, кто-то удалил её')
          
          normalize_value_row(form,field,data)
          field['values']=data
        form.run_event('after_update_code',{'field':field,'data':data})
        form.run_event('after_save_code',{'field':field,'data':data})



      return {
        'success':form.success(),
        'errors':form.errors,
        'id':exists_arg(field['table_id'],data),
        'values':field['values']
      }