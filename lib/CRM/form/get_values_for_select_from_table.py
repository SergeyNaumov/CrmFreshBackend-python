import re
from lib.core import exists_arg, tree_to_list
def get_values_for_select_from_table(form,f):


  if not exists_arg('value_field',f):
    f['value_field'] = 'id'
  
  if not exists_arg('header_field',f):
    f['header_field'] = 'header'
  
  select_fields=f'{f["value_field"]} v, {f["header_field"]} d'
  if exists_arg('tree_use',f):
    select_fields+=', parent_id'

  
  if not(exists_arg('table',f)):
    form.errors.append(f'Для поля {f["name"]} не указан атрибут table')
    return []
  query=f'SELECT {select_fields} from {f["table"]}'
  
  if exists_arg('query',f):
    query=f['query']
  
  #form.pre(query)
  if not exists_arg('where',f):
    f['where']=''

  if not exists_arg('order',f):
    if exists_arg('tree_use',f):
      f['order']='parent_id'
    else:
      f['order']=f['header_field']

  if exists_arg('autocomplete',f):
    if exists_arg('value',f):
      if f['where']: f['where']+=' AND '
      f['where']+=f['value_field']+'="'+f['value']+'"'
    
    else:
      return []

  if f['where']:
    if not re.match('^\s*where',f['where'],re.IGNORECASE):
      query+=' WHERE '
    
    query+=f['where']

  if not re.match('^\s*order by',f['order'],re.IGNORECASE):
    query+=' ORDER BY '
  query+=f['order']

  lst=[]
  if exists_arg('list',f) and len(f['list']):
    _lst = f['list']
  else:
    lst=form.db.query(
      query=query,
      errors=form.errors,

    )
    
    if len(form.errors): 
      return lst
    
    if not len(lst): lst=[]
    if form.script not in ('admin_table','find_objects'):
      lst.insert(0,{'v':'0','d':'выберите значение'})
    # else:
    #   _list.append({'v':'0','d':'выберите значение'})

    if exists_arg('tree_use',f):
      tree_list=[]
      _hash={}
      for l in lst:
        _hash[l['v']]=l
        if exists_arg('parent_id',l):
          hash_el=_hash[l['parent_id']]
          if not exists_arg('children',hash_el):
            hash_el['children']=[]

          hash_el['children'].append(l)

        else:
          tree_list.append(l)
      lst=[]
      tree_to_list(tree_list,lst,0)

  
  return lst
