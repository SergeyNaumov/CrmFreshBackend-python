from time import sleep
import re

def tree_use_transform(list,table_id='id'):
  list_hash={}
  new_list=[]
  for l in list:
    l['child']=[]
    list_hash[l[table_id]]=l

  for l in list:

    if parent_id:=l.get('parent_id'):
      if list_hash.get(parent_id):
        parent_item=list_hash[parent_id]
        parent_item['child'].append(l)
    else:
      new_list.append(l)


  return new_list

# Преобразование massive
def massive_transform(rez):
  list=[]
  for r in rez:
    for k in r.keys():
      list.append(r[k])

  return list

def out_error(self,error,arg):
    self.error_str=str(error)
    err_out=f"ERROR QUERY: {arg['query']}\n{self.error_str}"

    if arg.get('values') and len(arg['values']):
        err_out+=f"\nvalues: {arg['values']}"

    for err_name in ( 'errors', ): # ,'error'
        if (err_name in arg):
            if isinstance(arg[err_name],list): # type is list
                arg[err_name].append(err_out)
        else:
            arg[err_name]=err_out

    print("======\n",err_out,"\n======\n")

def rez_to_str(rez):
  if rez:
    for k in rez:
      print('k:',k)
      if not rez[k]: # Чтобы None не преобразовывалось в строку
        rez[k]=''
      else:
        rez[k]=str(rez[k])

def get_func(value):

  if value and isinstance(value,str):
    rez=re.match('func:\((.+)\)',value)
    if not rez:
      rez=re.match('func:(.+)',value)

    if rez:
      #print('value:',value,'rez:',rez[1])
      return rez[1]
  return ''

def get_query(self,arg): # для get и getrow
  self.error_str=''
  sf=arg.get('select_fields','*')


  if not arg.get('table'):
    out_error(self,f"FreshDB::{arg.get('method')} not set attr table",arg)
    return ''


  query='select '+sf+' FROM '+arg['table']+' wt'

  # join-ы
  if 'tables' in arg:
    for table in arg['tables']:
      if ('lj' in table ) and (table['lj']) :
        query += ' LEFT '

      query += ' JOIN '
      query += table['t']

      if ('a' in table) and (table['a']):
        query += ' '+ table['a']

      if ('l' in table) and (table['l']):
        query += ' ON '+ table['l']


  if where:=arg.get('where'):
    query += f" WHERE {where}"
  if order:=arg.get('order'):
    query += f" ORDER BY {order}"

  if arg.get('method') == 'getrow':
    arg['limit'] = 1

  if arg.get('perpage') and arg.get('table'):
    arg['perpage']=int(arg['perpage'])
    if not(arg.get('page')):
      arg['page']=1

    query_count=f"SELECT CEILING(count(*) / {arg['perpage']}) FROM {arg['table']}"

    if where:=arg.get('where'):
        query_count +=" WHERE {where}"

    if group:=arg.get('group'):
        query_count +=f" GROUP BY {group}"

    if not arg.get('values'):
        arg['values']=[]

    arg['maxpage']=self.query(query=query_count,onevalue=1,values=arg['values'])

    limit1=(arg['page']-1) * arg['perpage'];
    arg['limit']=str(limit1)+','+str(arg['perpage']);


  if limit:=arg.get('limit'):
    query += f" LIMIT {limit}"
  return query