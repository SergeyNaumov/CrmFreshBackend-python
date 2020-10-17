from lib.core import cur_year,cur_date, success, exists_arg
from fastapi import APIRouter
from config import config

from lib.engine import s
from lib.run_event import run_event
from lib.all_configs import read_config
import math

router = APIRouter()
#def get_search_tables(form):

def gen_query_search(form):
  query=''
  query_count=''
  qs=form.query_search
 # if exists_arg('ORDER',qs):
 #   if not isinstance(qs,list): qs['ORDER']=[qs['ORDER']]
 # else:
 #   qs['ORDER']=[]

  perpage=int(form.perpage)
  page=int(form.page)

  if form.QUERY_SEARCH:
      if qs['WHERE'] and len(qs['WHERE']):
        where_list=' AND '.join(qs['WHERE'])
        form.QUERY_SEARCH=form.QUERY_SEARCH.replace('<%WHERE%>',where_list)
      else:
        form.QUERY_SEARCH=form.QUERY_SEARCH.replace('<%WHERE%>','')

      query=form.QUERY_SEARCH
      
      if not form.not_perpage:
        query=query+' LIMIT '+form.page+','+form.perpage
  else:
      SELECT_FIELDS = ', '.join(qs['SELECT_FIELDS'])
      TABLES = "\n".join(qs['TABLES'])
      
      WHERE=''
      if len(qs['WHERE']):
        WHERE = ' WHERE '+' AND '.join(qs['WHERE'])

      GROUP=''
      if len(qs['GROUP']):
        GROUP = ' GROUP BY '+', '.join(qs['GROUP'])
      
      HAVING=''
      if len(qs['HAVING']):
        HAVING = ' HAVING '+', '.join(qs['HAVING'])

      query = 'SELECT '+SELECT_FIELDS + ' FROM ' + TABLES + WHERE + GROUP + HAVING

      if qs['ORDER']:
        # if not isinstance(qs['ORDER'],list): 
        #   qs['ORDER']=[qs['ORDER']]
        # if len(qs['ORDER']):
        
        query = query + ' ORDER BY '+', '.join(qs['ORDER'])

      if not form.not_perpage:
        
        
        query = query + ' LIMIT '+str( (page-1)*perpage ) +', '+form.perpage


      
      if len(qs['GROUP']):
        query_count = 'SELECT count(*) FROM (' + 'select '+ SELECT_FIELDS + ' FROM '+ TABLES + WHERE + GROUP + HAVING + ') x'
      else:
        query_count = ' SELECT count(*) cnt from ' + TABLES + WHERE + GROUP + HAVING

  return query, query_count



@router.post('/get-result')
async def get_result(R: dict):
  form=read_config(
    R=R,
    config=R['config'],
    script='find_objects'
  )

  if exists_arg('page',R):
    page=str(R['page'])
    if page.isnumeric(): form.page=page

  if exists_arg('params',R):
    params=R['params']
  
    if exists_arg('priority_sort',params):
      priority_sort=params['priority_sort']
      if len(priority_sort)==2 and priority_sort[1] in ('asc','desc'):
        form.priority_sort=priority_sort

  if form.GROUP_BY: form.query_search['GROUP'].append(form.GROUP_BY)
  
  form.SEARCH_RESULT={
    'log':form.log,
    'config':form.config,
    'headers':[],
    'card_format':form.card_format,
    'selects':{}
  }

  for values in R['query']:
    form.query_search['on_filters_hash'][values[0]]=values[1]
  
  form.get_search_tables(R['query'])
  
  form.get_search_where(R['query'])
  print('QUERY:',form.query_search)
  run_event(
    event=form.events['before_search'],
    description='events->before_search',
    form=form,
    arg={
      'tables':' '.join(form.query_search['TABLES']),
      'where':' AND '.join(form.query_search['WHERE'])
    }
  )

  run_event(
    event=form.events['before_search_mysql'],
    description='events->before_search_mysql',
    form=form,
    arg={
      'tables':' '.join(form.query_search['TABLES']),
      'where':' AND '.join(form.query_search['WHERE'])
    }
  )
  
  (query,query_count)=gen_query_search(form)
  
  
  #print('QUERY_COUNT:',query_count)
  if query_count:
    total_count=form.db.query(
      query='select sum(cnt) from ('+query_count+') x',
      onevalue=1,
      values=form.query_search['VALUES'],
      errors=form.errors
    )
    
    if total_count:
      total_count=int(total_count)
    else:
      total_count=9
    
    form.SEARCH_RESULT['count_total']=total_count
    
    

    if form.not_perpage:
      form.SEARCH_RESULT['count_pages']=1
    else:
      form.SEARCH_RESULT['count_pages']=math.ceil(total_count / int(form.perpage) )


  if int(page) > form.SEARCH_RESULT['count_pages']:
    form.page='1'

  log=[]
  
  

  result_list=form.db.query(
    query=query,
    #debug=1,
    values=form.query_search['VALUES'],
    errors=form.errors,
  )
  #print(result_list)
  if len(form.errors):
    return {'success':0,'errors':form.errors}

  output=[]
  memo_values={}
  multiconnect_values={}
  id_list=[]

  for r in result_list:

    id_list.append(r['wt__'+form.work_table_id])

  if len(id_list):
      for q in R['query']:
        name,values=q
        field=form.fields_hash[name]
        if field['type'] == 'multiconnect':
            multiconnect_arr=form.db.query(
              query="""
                SELECT
                    rst.{field['relation_save_table_id_worktable']} id,
                    group_concat(rt.{field['relation_table_header']} SEPARATOR ',') header
                FROM
                    {field['relation_save_table']} rst
                    join {field['relation_table']} rt ON (rt.{field['relation_table_id'] =rst.{field['relation_save_table_id_relation']})
                WHERE
                    rst.{field['relation_save_table_id_worktable']} IN ( {','.join(id_list)} )
                GROUP BY rst.{field['relation_save_table_id_worktable']
              """
            )
            for ma in multiconnect_arr: multiconnect_values[ma['id']]=ma['header']
  print('result_list',result_list)
  for r in result_list:
    print(r)
    data=[]
    for q in R['query']:
      name=q[0]
      

      field=form.fields_hash[name]
      type='html' #field['type']
      tbl = exists_arg('tablename',field) or 'wt'
      db_name=exists_arg('db_name',field) or name
      value=exists_arg(tbl+'__'+db_name,r)
      #print('r=>',r)
      #print(name,'=>',value)
      if not exists_arg('type_orig',type):
        field['type_orig']=field['type']

      if field['type_orig'] in ['filter_extend_select_values', 'select_values']:
          values_finded=0
          for v in field['values']:
            if v['v']==value:
              value,values_finded=v['d'],1

          if not values_finded:
            value='не выбрано'

      if not exists_arg('make_change_in_search',field) and exists_arg('filter_code',field) and not (isinstance(field['filter_code'],str)):
        value=field['filter_code'](str=str,value=value)
      else:
        if field['type']=='memo':
          type='memo'
        
        elif field['type']=='multiconnect':
          type='multiconnect'
          if exists_arg('wt__'+form.work_table_id,r):
            value=multiconnect_values[r['wt__'+form.work_table_id]]
          else: value=''

        elif field['type'].startswith('font'):
          type=field[type]

        elif field['type_orig'] in ['checkbox','switch']:
          if exists_arg('make_change_in_search',field):
            type=field['type']
          else:
            value=('нет','да')[value]

        elif field['type_orig'] in ['filter_extend_checbox','filter_extend_switch']:
          value=('нет','да')[value]

        elif field['type_orig'] in ['select_from_table','filter_extend_select_from_table']:
          if exists_arg('make_change_in_search',field):
            type='select'
            value=r[tbk+'__'+field['value_field']]
            if not exists_arg(name,form.SEARCH_RESULT['selects']):
                form.SEARCH_RESULT['selects'][name]=field['values']
          else:
            if field['db_name'].startswith('func:'):
              value = name
            elif r[tbl+'__'+field['header_field']]:
              value=r[tbl+'__'+field['header_field']]
            else:
              value=''
        elif field['type_orig'] in ['filter_extend_select_values','select_values']:
          if exists_arg('make_change_in_search',field):
            type='select'
            value=exists_arg(tbl+'__'+db_name,r)

            if not exists_arg(name,form.SEARCH_RESULT['selects']):
              form.SEARCH_RESULT['selects'][name]=field.values

        elif field['type_orig'] in ['text','textarea','filter_extend_text']:
          t='text' # или textarea ?
          type='text'
          value=exists_arg(tbl+'__'+db_name,r)

        elif field['type_orig'] == 'password':
          value='[пароль зашифрован]'

        elif field['type_orig']=='in_ext_url':
          value=exists_arg('in_ext_url__ext_url',r)

        elif field['type_orig']=='date' and exists_arg('make_change_in_search',field):
          type='date'
          #if exists_arg('make_change_in_search',field):

      data.append({
          'name':name,
          'type':type,
          'value':value
      })
    output.append({'key':r['wt__'+form.work_table_id],'data':data})
  
  # run_event(
  #     event=>$form->{events}->{after_search},
  #     description=>'events->after_search',
  #     form=>$form,
  #     arg=>[
  #         's'=>$s,
  #         form=>$form,
  #         result=>$result_list,
  #         headers=>$form->{SEARCH_RESULT}->{headers},
  #         output=>$output,
  #         tables=>join(" ",@{$form->{query_search}->{TABLES}}),
  #         where=>join(" AND ",@{$form->{query_search}->{WHERE}})
  #     ]
  # );


  if 1 : # not s['end'])
      form.SEARCH_RESULT['log']=form.log
      form.SEARCH_RESULT['output']=output
      print('SEARCH_RESULT:',form.SEARCH_RESULT)
      return {
              'success':(1,0)[len(form.errors)],
              'results':form.SEARCH_RESULT,
              'errors':form.errors,
              'out_before_search':form.out_before_search,
              'out_after_search':form.out_after_search,
              'explain_query':form.explain_query
      }
      
  

#  print('result_list:',result_list)

  # if not query_count:
  #   form.SEARCH_RESULT['count_total']=total_count
  #   if form_not_perpage:
  #     form.SEARCH_RESULT['count_pages']=1
  #   else:
  #     form.SEARCH_RESULT['count_pages']=math.ceil(total_count / perpage)


  if len(form.errors):
    return {'success':0,'errors':form.errors}

  return form.SEARCH_RESULT