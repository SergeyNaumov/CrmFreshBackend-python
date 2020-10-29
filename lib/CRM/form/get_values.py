import re
from lib.core import is_wt_field, exists_arg
def tree_to_list(tree_list,lst,level):
  for t in tree_list:
    t['d']=('..'*level) + t['d']
    lst.append({'v':t['v'],'d':t['d']})
    if exists_arg('children',t) and len(t['children']):
      tree_to_list(t['children'],lst,level+1)

def get_values_for_select_from_table(form,f):
  #print('get_values_for_select_from_table не готово')
  #values=[]
  if not exists_arg('value_field',f):
    f['value_field'] = 'id'
  
  if not exists_arg('header_field',f):
    f['header_field'] = 'header'
  
  select_fields=f'{f["value_field"]} v, {f["header_field"]} d'
  if exists_arg('tree_use',f):
    select_fields+=', parent_id'


  query=f'SELECT {select_fields} from {f["table"]}'

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
      f['where']+=f' {f.value_field}="{f.value}" '
    
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
      query=query,errors=form.errors,
      debug=1
    )
    if not len(lst): lst=[]
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

def get_1_to_m_data(form,f):
  print('get_1_to_m_data не готова')

def get_in_ext_url(form,f):
  print('get_in_ext_url не готова')

def func_get_values(form):
    values={}

    if form.id:
      values=form.db.query(
        query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
        values=[form.id],
        onerow=1,
        debug=1,
        log=form.log
      )
      #print('GET_VALUES:',values)
      if not values:
          form.errors.append(f'В инструменте {form.title} запись с id: {form.id} не найдена. Редактирование невозможно')
          return

      for f in form.fields:
        if f['type']=='password':
          del values[f['name']]



    for f in form.fields:

      #if f['type'] in ['date','datetime','text','textarea']:



      name=f['name']
      #print(f)
      if is_wt_field(f):
        #if name=='checkbox':
          #print('not name checkbox:', (not name in values) )
          #print('not value checkbox:', (not values[name]) )
        # if name in values:
        #   print('before:',name,':',values[name])
        if not name in values or (not (values[name]) and values[name]!=0 and values[name]!='0'):
            values[name]=''
        else:
          values[name]=str(values[name])
          if f['type']=='datetime' and values[name]=='0000-00-00 00:00:00':
            values[name]=''

        # if name in values:
        #   print('after:',name,':',values[name])
      # else:
      #   print('not_wt_field:',f)
          
          

      
        #if not f['value']:
        #  f['value']=''

      if form.action not in ['insert','update'] and exists_arg('orig_type',f)=='select_from_table':
         f['values']=get_values_for_select_from_table(form,f)
      # #print('f:',f)
      if f['type'] == '1_to_m':
        get_1_to_m_data(form,f)

      if f['type']=='get_in_ext_url':
        get_in_ext_url(form,f)
        #values[name]=f['value']



      if name in values:
        if values[name].isnumeric():
          values[name]=str(values[name])
        f['value']=values[name]
      #else:
      #  print(f['name'],' - not numeric:', values[name])

      #values[name]=f['value']
      
    form.values=values
    #print('GET_VALUES2:',values)


