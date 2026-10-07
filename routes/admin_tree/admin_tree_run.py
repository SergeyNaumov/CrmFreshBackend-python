import re
from lib.core import exists_arg
from lib.all_configs import read_config
from .move import move

async def get_branch(**arg):
  
  form=arg['form']
  parent_id=str(exists_arg('parent_id',arg) or '')
  parents=exists_arg('parents',arg)
  where=[]
  #cur_level=0
  branch={'path':[],'list':[]}
  
  if parent_id: # Если находимся не в корне, то собираем $branch->{path} (путь ветки)
    # Путь ветки собираем подъёмом по parent_id, а НЕ разбором столбца path:
    # в БД его значения могут не соответствовать соглашению "цепочка id предков"
    # (например, в ds_catalog лежит '/catalog/<id>' -- литеральный сегмент 'catalog'
    # попадал в SQL как w.id=catalog и ронял запрос). В условие попадает только
    # то, что прошло isnumeric().
    cur_id=str(parent_id)
    visited=set()
    while cur_id and cur_id not in visited:
      visited.add(cur_id)
      if not cur_id.isnumeric():
        break

      where=[f'w.{form.work_table_id}={cur_id}']
      add_where_foreign_key(form,where)

      query=''
      if form.tree_select_header_query:
        query=f'{form.tree_select_header_query} AND (w.{form.work_table_id}={cur_id})'
      else:
        query=f'SELECT * from {form.work_table} w'
        query+=' WHERE '+' AND '.join(where)

      query+=' LIMIT 1000'
      item = await form.db.query(
        query=query,
        onerow=1,
        errors=form.errors,
      )
      if len(form.errors) or not item:
        break

      header=form.default_find_filter or 'header'
      for k in item.keys(): header=header.replace('<%'+k+'%>',str(item[k]))

      # Идём от листа к корню, поэтому вставляем в начало
      branch['path'].insert(0,{'header':header,'id':cur_id})

      parent=item.get('parent_id')
      cur_id=str(parent) if parent is not None else ''
  
  # end if parent_id
  sql_query=''
  where=[]
  if form.tree_select_header_query:
      sql_query=form.tree_select_header_query
      if form.tree_use:
        if parent_id and parent_id.isnumeric():
          sql_query+=' AND parent_id='+parent_id
        else:
          sql_query+=' AND parent_id IS NULL'
  else:
      sql_query=f'SELECT * FROM {form.work_table} w'
      
      if form.tree_use:
        if parent_id and parent_id.isnumeric():
          where.append('w.parent_id='+parent_id)
        else:
          where.append('(w.parent_id is null or w.parent_id=0)')
      
      add_where_foreign_key(form,where);
      
      sql_query=add_where_to_query(sql_query,where)


  if form.sort:
    sql_query+=' ORDER BY w.'+form.sort_field
  else:
    # header_field бывает пустым (конфиги, сделанные под admin-table) -- тогда
    # получался невалидный "ORDER BY w. LIMIT 1000"
    sql_query+=' ORDER BY w.'+(form.header_field or form.work_table_id)
  
  sql_query+=' LIMIT 1000' # защита от дурака

  result_lst= await form.db.query(
    query=sql_query,
    errors=form.errors
  )
  if form.errors:
    # при ошибке в SQL db.query возвращает None -- не итерируем его
    return []
  for item in result_lst:
    if form.header_field:
      if form.header_field not in item:
        form.errors.append(f"в таблице {form.work_table} отсутствует поле {form.header_field}")
        return []
      header=item[form.header_field]
    else:
      header=item.get(form.work_table_id)
    id=item[form.work_table_id]
    el={
      'header':header,
      'id':id,
    }
    el['sort']=exists_arg('sort',item) or ''
    # Миниатюра элемента ветки: задаётся ключом photo_field (обычные списки)
    # или photo_for_gallery (галерейный вид). Поле должно быть в SELECT-строке.
    photo_field_name=getattr(form,'photo_field',None) or getattr(form,'photo_for_gallery',None)
    if photo_field_name and exists_arg(photo_field_name,item):
      photo=item[photo_field_name] or ''
      filedir=''
      if pf:=form.get_field(photo_field_name):
        filedir=exists_arg('filedir',pf) or ''
      if photo and filedir:
        el['photo']=re.sub(r'^\.\/','/',filedir)+'/'+photo
      else:
        el['photo']=photo
    if form.tree_use:
      if exists_arg('get_childs',arg):
        el['childs']=await get_branch(
          form=form,
          get_childs=0,
          parent_id=id
        )
    branch['list'].append(el)
  ids=[]

  if 0 and form.tree_use and exists_arg('get_childs',arg): 
    for item in branch['list']:
      ids.append(item['id'])
    child_list=await get_branch(
      form=form,
      get_childs=0,
      parents=ids
    )
  return branch['list']


def add_where_foreign_key(form,where):
  if hasattr(form,'foreign_key') and form.foreign_key_value:
    where.append(f'({form.foreign_key}={form.foreign_key_value})')
  return where

def add_where_to_query(query,where):
  if len(where):
    query+=' WHERE '+' AND '.join(where)
  return query

async def admin_tree_run(**arg):
  
  R=arg['R']
  action=exists_arg('action',R) or ''
  parent_id=str(exists_arg('parent_id',R) or '')
  if parent_id =='0':
    parent_id=''
  id=exists_arg('id',R) or ''
  
  form = await read_config(
    config=arg['config'],
    script='admin_tree',
    action=action,
    id=id,
    request=arg['request']
  )
  
  
  if len(form.errors):
    return {
       'success':0,
       'errors':form.errors
    }
  if not form.sort_field: form.sort_field='sort'

  # Составной первичный ключ (напр. "param_id,good_id" у ds_params_good):
  # строка результата не содержит такого поля, item[work_table_id] падал бы с
  # KeyError -> 500. admin-tree для таких конфигов неприменим, отдаём ошибку.
  if ',' in str(form.work_table_id):
    return {
      'success':0,
      'errors':[f'конфиг {form.config}: составной первичный ключ ({form.work_table_id}) не поддерживается в admin-tree']
    }



  if form.action == 'add_branch_plain':
      headers=exists_arg('header',R).split("\n")
      data_for_multi=[]
      for h in headers:
        
        if h:
          cur_path=''
          cur_sort=0
          if parent_id and parent_id.isnumeric():
            cur_path = await form.db.query(
              query=f'SELECT path from {form.work_table} where {form.work_table_id}=%s',
              values=[parent_id],
              onevalue=1
            )
            cur_path+='/'+parent_id
          if form.sort:
            qw=f'SELECT max({form.sort_field}) from {form.work_table}'
            if form.tree_use:
              
              if parent_id and parent_id.isnumeric():
                qw+=' WHERE parent_id='+parent_id
              else:
                qw+=' WHERE parent_id is null'
            
            cur_sort = await form.db.query(query=qw,onevalue=1)
            
            if not cur_sort:
              cur_sort='1'
            else:
              cur_sort=str(int(cur_sort)+1)
            

          sql_query=''
          value=[]
          fields=[]
          data={form.header_field:h}
          if form.sort:
            data[form.sort_field]=cur_sort
          
          if form.tree_use:

            if parent_id and parent_id.isnumeric():
              data['parent_id']=parent_id
              data['path']=cur_path

          if hasattr(form,'foreign_key') and hasattr(form,'foreign_key_value'):
              data[form.foreign_key]=form.foreign_key_value

          # EVENTS!
          form.new_values=data
          await form.run_event('before_insert')
          await form.run_event('before_save')
          
          form.id = await form.db.save(
            table=form.work_table,
            data=data
          )
          data_for_multi.append({
            'id':form.id,
            'sort':cur_sort,
            'header':h,
            'childs':[]
          })
          if not form.id:
            form.errors.append('произошла ошибка при добавлении раздела. Возможно, превышен максимальный уровень вложенности')

          await form.run_event('after_insert')
          await form.run_event('after_save')
          
      return {
        'success':form.success(),
        'errors':form.errors,
        'data':{ # Оставляем для старых версий, в которых нельзя добавлять много записей
          'id':form.id,
          'sort':cur_sort,
          'header':h,
          'childs':[]
        },
        'data_for_multi': data_for_multi
      }

  elif form.action == 'sort':
    if form.sort:
      where=[f'{form.work_table_id}=%s']
      add_where_foreign_key(form,where)
      if parent_id:
        where.append('parent_id='+parent_id)

      query=add_where_to_query(f'UPDATE {form.work_table} SET sort=%s',where)
      for id in R['obj_sort'].keys():
        await form.db.query(
          query=query,
          values=[R['obj_sort'][id],id],
          errors=form.errors
        )
      await form.run_event('after_sort')
      return {'success':form.success(),'errors':form.errors}
    else:
      return {'success':'0','errors':['сортировка запрещена']}
  elif form.action == 'get_branch' and parent_id and parent_id.isnumeric():
    return {'success':1,'data': await get_branch(form=form,parent_id=parent_id)}

  elif form.action == 'delete_branch':
    if form.make_delete:
      if form.id:
        where = [f'{form.work_table_id}={id}']
        values=[]
        add_where_foreign_key(form,where)
        cur_branch = await form.db.query(
          query=f'SELECT * from {form.work_table} where {form.work_table_id}=%s',
          values=[form.id],
          onerow=1
        )

        query=add_where_to_query(f'DELETE FROM {form.work_table}',where)
        await form.run_event('after_delete')
        await form.db.query(query=query,errors=form.errors)

        cur_count='0'
        if form.tree_use:
          where=[f'path like %s or path like %s']
          values.append('%/'+str(form.id)+'/%')
          values.append('/%'+str(form.id))
          add_where_foreign_key(form,where)

          if  cur_branch and exists_arg('parent_id',cur_branch):
            cur_count=await form.db.query(
              query=f'SELECT count(*) from {form.work_table} where parent_id=%s',
              values=[cur_branch['parent_id']],
              onevalue=1
            )
          else:
            cur_count=await form.db.query(
              query=f'SELECT count(*) from {form.work_table}',
              onevalue=1
            )
        return {
          'success':1,
          'cur_count':cur_count,
          'cur_branch':cur_branch
        }

      else:
        return {'success':0,'error':'Не указан id!'}

  elif form.action == 'update_branch':
    if form.read_only:
      return {'success':0,'error':'Редактирование запрещено!'}
    else:
      if form.id:
        await form.db.query(
          query=f'UPDATE {form.work_table} SET {form.header_field}=% WHERE {form.work_table_id}=%s',
          values=[R['header'],form.id]
        )
        return {'success':1}
      else:
        return {'success':0,'error':'не указан id'}


  elif form.action=='move':
    return await move(form,R)
  
  elif form.action=='load_many_childs':
    obj_list=R['list']
    data_result={}

    if len(obj_list):
      photo_field_name=getattr(form,'photo_field',None) or getattr(form,'photo_for_gallery',None)
      if photo_field_name and form.header_field and photo_field_name==form.header_field:
        photo_field_name=None
      for id in obj_list:
        sort=''
        order=''
        extra=''
        if photo_field_name:
          # для миниатюр в дочерних ветках берём и колонку фото
          extra=f', {photo_field_name} photo'

        if form.sort:
          sort=f', {form.sort_field} sort'
          order=f'ORDER BY {form.sort_field}'

        query=f'select {form.work_table_id} id,{form.header_field} header {sort} {extra} from {form.work_table} where parent_id={id} {order}'

        rows=await form.db.query(query=query)
        if photo_field_name and rows:
          filedir=''
          if pf:=form.get_field(photo_field_name):
            filedir=exists_arg('filedir',pf) or ''
          for r in rows:
            if r.get('photo') and filedir:
              r['photo']=re.sub(r'^\.\/','/',filedir)+'/'+r['photo']
        data_result[id]=rows
    return {'success':1,'data':data_result}


  else: # по умолчанию
    branch=await get_branch(form=form,get_childs=1,parent_id='')
    if len(form.errors):
      return {'success':0,'errors':form.errors}
    out_form={
      'sort':form.sort,
      'title':form.title,
      'header_field':form.header_field,
      'sort_field':form.sort_field,
      'config':form.config,
      'not_create':form.not_create,
      'tree_use':form.tree_use,
      'make_delete':form.make_delete,
      'read_only':form.read_only,
      'max_level':form.max_level,
      #'changed_in_tree':getattr(form,'changed_in_tree',False),
    }
    # для галереи
    for name in ['view_type','photo_for_gallery','photo_field','cols', 'changed_in_tree']:
      if(hasattr(form,name)):
        out_form[name]=getattr(form, name)
    

    return {
      'success':1,
      'form':out_form,
        'log':form.log,
        'errors':form.errors,
        'tree':branch
    }




