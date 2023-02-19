from lib.core import exists_arg
from lib.all_configs import read_config
from .move import move

def get_branch(**arg):
  
  form=arg['form']
  parent_id=str(exists_arg('parent_id',arg) or '')
  parents=exists_arg('parents',arg)
  where=[]
  #cur_level=0
  branch={'path':[],'list':[]}
  
  if parent_id: # Если находимся не в корне, то собираем $branch->{path} (путь ветки)
    where=add_where_foreign_key(form,where)

    query_path=f'SELECT path from {form.work_table}'
    
    if len(where):
      query_path+=' WHERE '+' AND '.join(where)

    pathstr=form.db.query(
      query=query_path,
      onevalue=1,
      errors=form.errors
    )
    pathstr+='/'+parent_id
    
    if len(form.errors):
      return

    # определяем уровень вложенности
    #cur_level=len( list(pathstr.split('/')) ) -1 
    path_elements=pathstr.split('/')
    
    for id in path_elements:
      if not id:
        continue

      id=str(id)
      where=[f'w.{form.work_table_id}={id}']
      add_where_foreign_key(form,where)

      query=''
      if form.tree_select_header_query:
        query=f'{form.tree_select_header_query} AND (w.{form.work_table_id}={id})'
      else:
        query=f'SELECT * from {form.work_table} w'
        
        if len(where):
          query+=' WHERE '+' AND '.join(where)
      
      query+=' LIMIT 1000'
      item=form.db.query(
        query=query,
        onerow=1,
        debug=1,
        errors=form.errors,
      )
      

      header=form.default_find_filter or 'header'
      if item:
        for k in item.keys(): header=header.replace('<%'+k+'%>',str(item[k]))

      branch['path'].append({'header':header,'id':id})
  
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
    sql_query+=' ORDER BY w.'+form.header_field
  
  sql_query+' LIMIT 1000' # защита от дурака

  result_lst=form.db.query(
    query=sql_query,
    errors=form.errors
  )
  for item in result_lst:
    if not(form.header_field) in item:
      form.errors.append(f"в таблице {form.work_table} отсутствует поле {form.header_field}")
      return []
    id=item[form.work_table_id]
    el={
      'header':item[form.header_field],
      'id':id,
    }
    el['sort']=exists_arg('sort',item) or ''
    if form.tree_use:
      if exists_arg('get_childs',arg):
        el['childs']=get_branch(
          form=form,
          get_childs=0,
          parent_id=id
        )
    branch['list'].append(el)
  ids=[]

  if 0 and form.tree_use and exists_arg('get_childs',arg): 
    for item in branch['list']:
      ids.append(item['id'])
    child_list=get_branch(
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

def admin_tree_run(**arg):
  
  R=arg['R']
  action=exists_arg('action',R) or ''
  parent_id=str(exists_arg('parent_id',R) or '')
  if parent_id =='0':
    parent_id=''
  id=exists_arg('id',R) or ''
  
  form=read_config(
    config=arg['config'],
    script='admin_tree',
    action=action,
    id=id
  )
  
  
  if len(form.errors):
    return {
       'success':0,
       'errors':form.errors
    }
  if not form.sort_field: form.sort_field='sort'



  if form.action == 'add_branch_plain':
      headers=exists_arg('header',R).split("\n")
      data_for_multi=[]
      for h in headers:
        
        if h:
          cur_path=''
          cur_sort=0
          if parent_id and parent_id.isnumeric():
            cur_path=form.db.query(
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
            
            cur_sort=form.db.query(query=qw,onevalue=1)
            
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
          form.run_event('before_insert')
          form.run_event('before_save')
          
          form.id=form.db.save(
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

          form.run_event('after_insert')
          form.run_event('after_save')
          
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
        form.db.query(
          query=query,
          values=[R['obj_sort'][id],id],
          errors=form.errors
        )
      form.run_event('after_sort')
      return {'success':form.success(),'errors':form.errors}
    else:
      return {'success':'0','errors':['сортировка запрещена']}
  elif form.action == 'get_branch' and parent_id and parent_id.isnumeric():
    return {'success':1,'data':get_branch(form=form,parent_id=parent_id)}

  elif form.action == 'delete_branch':
    if form.make_delete:
      if form.id:
        where = [f'{form.work_table_id}={id}']
        values=[]
        add_where_foreign_key(form,where)
        cur_branch=form.db.query(
          query=f'SELECT * from {form.work_table} where {form.work_table_id}=%s',
          values=[form.id],
          onerow=1
        )

        query=add_where_to_query(f'DELETE FROM {form.work_table}',where)
        form.run_event('after_delete')
        form.db.query(query=query,errors=form.errors)

        cur_count='0'
        if form.tree_use:
          where=[f'path like %s or path like %s']
          values.append('%/'+str(form.id)+'/%')
          values.append('/%'+str(form.id))
          add_where_foreign_key(form,where)

          if  cur_branch and exists_arg('parent_id',cur_branch):
            cur_count=form.db.query(
              query=f'SELECT count(*) from {form.work_table} where parent_id=%s',
              values=[cur_branch['parent_id']],
              onevalue=1
            )
          else:
            cur_count=form.db.query(
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
        form.db.query(
          query=f'UPDATE {form.work_table} SET {form.header_field}=% WHERE {form.work_table_id}=%s',
          values=[R['header'],form.id]
        )
        return {'success':1}
      else:
        return {'success':0,'error':'не указан id'}


  elif form.action=='move':
    return move(form,R)
  
  elif form.action=='load_many_childs':
    obj_list=R['list']
    data_result={}

    if len(obj_list):
      for id in obj_list:
        data_result[id]=get_branch(form=form,get_childs=0,parent_id=id)
    return {'success':1,'data':data_result}


  else: # по умолчанию
    branch=get_branch(form=form,get_childs=1,parent_id='')
    if len(form.errors):
      return {'success':0,'errors':form.errors}

    return {
      'success':1,
      'form':{
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
            'changed_in_tree':hasattr(form,'changed_in_tree')
        },
        'log':form.log,
        'errors':form.errors,
        'tree':branch
    }




