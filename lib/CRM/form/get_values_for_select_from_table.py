import re
from lib.core import exists_arg, tree_to_list
def get_values_for_select_from_table(form,f,parent_field=None, debug=False):


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
  
  #if f['name']=='service_id':
    #print('f1:',f)
  if exists_arg('query',f):
    query=f['query']
  else:


    if not exists_arg('order',f):
      if exists_arg('tree_use',f):
        f['order']='parent_id'
      else:
        f['order']=f['header_field']
  
    #print('f2:',f['order'])

    if not exists_arg('where',f):
      f['where']=''

    f_where=f['where']

    if exists_arg('autocomplete',f):
      if exists_arg('value',f):
        if f_where: f_where+=' AND '
        f_where+=f"""{f['value_field']}="{f['value']}" """
      
      elif form.script in ['edit_form','1_to_m'] and form.id and parent_field and parent_field['type']=='1_to_m': # Если есть родительский элемент
          # Если это select_from_table внутри 1_to_m и мы выводим слайд, то значения собираем для всех записей 1_to_m, 
          # чтобы в слайде было что отображать
          if f['name']=='template_id':
            
            one_to_m_ids=form.db.query(
              query=f"SELECT {f['name']} FROM {parent_field['table']} where {parent_field['foreign_key']}={form.id}",
              massive=1,
              str=True
            )
            if len(one_to_m_ids):
              if f_where: f_where+=' AND '
              f_where+=f"{f['value_field']} in ("+','.join(one_to_m_ids)+")"

              #print('1_to_m_ids:',one_to_m_ids)
              #print(f'action: {form.action}  | script: {form.script} | FLD: {f}')
      
      else:    
      #  print(f"\n\nscript:{form.script} action: {form.action}, parent_field: {parent_field}")
        return []
    if f['name']=='template_id':
      print("\n\nquery:", query)
      print("WHERE:", f_where)

    if f_where:
      #if not(re.match('^\s*where',query,re.IGNORECASE)):
      #  query+=' WHERE '
      if not(re.match('^\s*where',f_where,re.IGNORECASE)):
        #print('!!!QUERY:', query)
        #print("\n\nwhere:",f_where)
        #print("ADD STR WHERE before\n")
        query+=' WHERE '
      
      query+=f_where

    #if not re.match('^\s*order by',f['order'],re.IGNORECASE):

    query+=f" ORDER BY {f['order']}"
    #if f['name']=='service_id':
    #  print('f3:',f['order'],"\n\n")
    #  print('query:',query,f['order'])    

  lst=[]

  if exists_arg('list',f) and len(f['list']):
    _lst = f['list']
  else:
    lst=form.db.query(query=query,errors=form.errors)
    
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
