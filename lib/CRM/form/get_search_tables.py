from lib.core import exists_arg, get_func
import re

#def adding_select_fields()

def adding_select_fields_in_desc(form,db_field,t):
  fld_on_query=t['alias']+'.'+db_field['Field']+' '+t['alias']+'__'+db_field['Field']
  if not exists_arg('select_fields', t):
    form.query_search['SELECT_FIELDS'].append(fld_on_query)

  if exists_arg('select_fields', t) and exists_arg(field_name, t['select_fields']):
    
    form.query_search['SELECT_FIELDS'].append(fld_on_query)

    


  

def get_search_tables(form,query):
  TABLES=[]
  #if not form.QUERY_SEARCH and len(form.QUERY_SEARCH_TABLES):
    # for f in form.fields:
    #   if 0 and f.type == 'in_ext_url':
    #      in_ext_url=f['in_url']
  
  aliases_on={'wt':1}
  for t in form.QUERY_SEARCH_TABLES:
    t_str=''
    need_add_table=1
    if not exists_arg('table',t) and exists_arg('t',t):
      t['table']=t['t']
    
    if not exists_arg('alias',t)  and exists_arg('a',t):
      t['alias']=t['a']

    if not exists_arg('left_join',t) and exists_arg('lj',t):
      t['left_join']=t['lj']

    if not exists_arg('link',t)  and exists_arg('l',t):
      t['link']=t['l']

    if exists_arg('link',t):
      if exists_arg('left_join',t):
        t_str = t_str + ' LEFT '
      
      t_str = ''.join([t_str,' JOIN ',t['table'],' as ',t['alias'],' ON (',t['link'],')'])

      if exists_arg('for_fields',t) :
        need_add_table = 0
        for fld_name in t['for_fields']:
          if fld_name in form.query_search['on_filters_hash']:
            need_add_table = 0
            break

    else:
      t_str='`'+t['table']+'` `'+t['alias']+'`'

    if need_add_table:
      TABLES.append(t_str)
      
      if not exists_arg('not_add_in_select_fields', t):
        desc = form.db.query(
          query = 'desc '+t['table'],
          errors=form.log
        )
        if desc:
            for db_field in desc:
              #adding_select_fields(form,db_field,t)
              adding_select_fields_in_desc(form,db_field,t)

  for f in form.fields:
    func=get_func(f)
    if func: form.query_search['SELECT_FIELDS'].append(func+' '+f['name'])
    
  form.query_search['TABLES']=TABLES