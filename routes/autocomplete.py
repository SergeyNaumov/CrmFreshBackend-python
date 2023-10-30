from lib.core import cur_year,cur_date, exists_arg, get_name_and_ext
from fastapi import FastAPI, APIRouter
#from lib.engine import s

#import re
#from lib.send_mes import send_mes
from lib.all_configs import read_config


#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()

# изменение пароля
@router.post('/{config}')
async def autocomplete(config:str,R: dict):
  success=1
  errors=[]
  field=''
  result_list=[]
  form=read_config(
    script='autocomplete', config=config,
    R=R,
    #id=R['id']
  )
  term=R['term'] if(exists_arg('term',R)) else ''
  name=R['field_name'] if(exists_arg('field_name',R)) else ''

  if R['action'] == 'get_begin_value': # тут нужно будет доделать, хз, что это
    return get_begin_value(form=form,element=element)
  
  elif term:
    #print('NAME',name)
    #print('TERM:',term)
    # используем get_name_and_ext для получения name и subname 
    name,sub_name=get_name_and_ext(name)
    field=form.get_field(name)

    if sub_name:
      
      for f in field['fields']:
        if f['name'] == sub_name:
          field=f
    else:
      #field=form.get_field(name)
      if ajax_autocomplete:=exists_arg('ajax;autocomplete',field):
        #print('ajax_autocomplete:',ajax_autocomplete)
        result_list=ajax_autocomplete(form,field,R)
        return {
          'success':True,
          'list': result_list
        }
        print('result_list:',result_list)
      

  else: # нет поиска по строке, вывозим по depend_where (зависимый фильтр)
    
    name,sub_name=get_name_and_ext(name)
    #if sub_name:
    #  errors.append('не указан term')
    #else:
    field=form.get_field(name)
    #if 'depend_where' in field:
    #  pass
    #else:
    #  errors.append('не указан term')
  
  if not('values' in R): R['values']=[]


  if not field:
    errors.append(f'field_name: {name} not found')
  else:
    result_list=get_list(
      errors=errors,
      form=form,
      name=name,
      element=field,
      value=term,
      values=R['values']
    )
    
  
        

  return  {'success':0 if(len(errors)) else 1,'errors':errors,'list':result_list}
    
def get_list(**arg):
  form=arg['form']
  element=arg['element']
  like_values=[]
  where=''
  if arg['errors']:
    return []

  work_table=''
  if not exists_arg('value',arg) or not(arg['value']):
    arg['value']=''
  
  like_val=arg['value']

  if exists_arg('before_search',element):
    element['before_search'](form,element)

  #print("\n\nElement:",element)
  if not('orig_type' in element):
    element['orig_type']=element['type']

  T=element['orig_type'] 
  #print('T:',T)
  if T=='multiconnect':
    return form.db.query(
      query=f'''
        SELECT
            {element['relation_table_id']} as id, { element['relation_table_id'] } as value, { element['relation_table_header'] } as label
        FROM
            { element['relation_table'] }
        WHERE
            { element['relation_table_header'] } like %s
        ORDER BY
            { element['relation_table_header'] }
        LIMIT  30
      ''',
      values=['%'+arg['value']+'%']
    )
  if T == 'filter_extend_text':
    for x in form.QUERY_SEARCH_TABLES:
      if x['alias'] == element['filter_table']:
        work_table=x['table']
        element['name']=element['db_name']
        T='text'
        break

  if T in ['select_from_table','filter_extend_select_from_table']:
    

    if not exists_arg('out_header',element): 
      element['out_header'] = element['header_field']

    select_fields=element['value_field']+' v, '+element['out_header']+' d'

    if exists_arg('where', element):
      where+=element['where']
    if exists_arg('depend_where',element):
      if where:
        where+=' AND '
      where+=element['depend_where']

    #print('WHERE:',where)
    if True or like_val:
      if where:
        where=where+' AND '
      where+=f"{element['header_field']} like %s"
      like_values.append('%'+like_val+'%')

      if exists_arg('values',arg):
        values_array=[]
        for v in arg['values']:
          #print('v:',v)
          values_array.append(str(v))
        #print('values_array:',values_array)
        
        if len(values_array):
          if where: where+=' OR '
          where+=element['value_field']+' IN ('+','.join(values_array)+')'

    

    if T=='filter_extend_select_from_table' and exists_arg('filter_table',element):
      element['table']=element['filter_table']

    if not exists_arg('search_query',element):
      if where: where='WHERE '+where
      element['search_query']=f'''
          SELECT {select_fields} from {element['table']}  {where}  ORDER by {element['header_field']} limit 30
      '''

    if exists_arg('search_query',element):
      element['search_query']+=' limit 30'
      element['search_query']=element['search_query'].replace('<%like%>',like_val).replace('<%v%>','%s')
    
    #print('query:',element['search_query'])
    #print('like_values:',like_values)
    return form.db.query(

      query=element['search_query'],
      values=like_values
    );



  # T -- type
  


  #print('DB',form.db)
def ecran_ind(v):
  v=v.replace('@','\\@')
  #print re.sub(r'([\.])', r'\\\1', "example string.")

  return v

def get_begin_value(**arg):
  db=arg['form']['db']
  print('DB')
