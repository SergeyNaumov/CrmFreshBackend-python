from lib.core import exists_arg
from lib.get_1_to_m_data import normalize_value_row, get_1_to_m_data
from .get_data import get_data

async def insert_or_update(form,field,arg):
    R=form.R
    #print('ARG:',arg)
    field['values']=[]
    if not exists_arg('values',R) or not len(R['values']):
      form.errors.append('обратитесь к разработчику: в запросе отсутствуют значения (values)')
    elif not field:
      form.errors.append('обратитесь к разработчику: в запросе отсутствуют значения (values)')
    
    data=get_data(form,field)
    #print('data:',data)
    foreign_key_value=form.id
    if 'foreign_key_value' in field:
      if field['foreign_key_value']:
        foreign_key_value=field['foreign_key_value']
      else:
        form.errors.append('foreign_key_value предусмотрено, но не заполнено. обратитесь к разработчику')

    if form.success():


      # INSERT
      if form.action=='insert':
        await form.run_event('before_insert_code',{'field':field,'data':data})
        await form.run_event('before_save_code',{'field':field,'data':data})

        if form.success():
          # Сортировка 1_to_m: новый слайд добавляется в конец группы (max+1),
          # иначе драг-сортировка работает, но новые записи встают по sort=0
          # в начало списка (ORDER BY sort).
          if exists_arg('sort',field):
            sort_field=exists_arg('sort_field',field) or 'sort'
            if sort_field not in data:
              cur_sort=await form.db.query(
                query=f'SELECT max({sort_field}) from {field["table"]} where {field["foreign_key"]}={foreign_key_value}',
                onevalue=1,
                errors=form.errors,
              )
              data[sort_field]=1 if not cur_sort else int(cur_sort)+1

          # Таблицы слайдов конструкторных проектов имеют project_id (FK на project):
          # без него INSERT падает с нарушением внешнего ключа. Проверяем наличие
          # колонки один раз (кэш на поле) и заполняем из контекста проекта.
          if 'project_id' not in data and 'project_id' not in (field.get('_cols') or ()):
            if field.get('_cols') is None:
              cols=await form.db.query(
                query=f'SHOW COLUMNS FROM `{field["table"]}`',
                errors=form.errors,
              ) or []
              field['_cols']=[str(r.get('Field', '')).lower() for r in cols]
            if 'project_id' in field['_cols']:
              pid=(form.project or {}).get('project_id')
              if pid:
                data['project_id']=pid

          data[field['table_id']] = await form.db.save(
            table=field['table'],
            data=data,
            errors=form.errors,
          )
          field['_id']=data[field['table_id']]
          await form.run_event('after_insert_code',{'field':field,'data':data})
          await form.run_event('after_save_code',{'field':field,'data':data})

      elif form.action=='update':
        data[field['table_id']]=arg['one_to_m_id']
        await form.run_event('before_update_code',{'field':field,'data':data})
        await form.run_event('before_save_code',{'field':field,'data':data})
        
        if form.success():
          await form.db.save(
            table=field['table'],
            where=f'{field["foreign_key"]}={foreign_key_value} and {field["table_id"]}={arg["one_to_m_id"]}',
            update=1,
            errors=form.errors,
            data=data,
          )

          # onerow=1: возвращаем одну строку-dict, а не список -- иначе
          # normalize_value_row (slide_code) падает на list indices
          data = await form.db.query(
            query=f'SELECT * from {field["table"]} WHERE {field["table_id"]}=%s',
            values=[arg["one_to_m_id"]],
            onerow=1,
            errors=form.errors,
          )
          #print('data0:',data)
          if not data:
            form.errors.append('данной записи уже не существует, возможно, кто-то удалил её')
          else:
            await normalize_value_row(form,field,data)
            #print('data1:',data)
            field['values']=data

          field['_id']=arg["one_to_m_id"]
          await form.run_event('after_update_code',{'field':field,'data':data})
          await form.run_event('after_save_code',{'field':field,'data':data})

      await get_1_to_m_data(form,field)

      return {
        'success':form.success(),
        'errors':form.errors,
        'id':exists_arg(field['table_id'],data),
        'field':field,
        'values':field['values']
      }
