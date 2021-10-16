from lib.core import cur_year,cur_date, exists_arg
from fastapi import APIRouter
from config import config

from lib.engine import s
#from lib.run_event import run_event
from lib.all_configs import read_config
from .get_result.process_result_list import process_result_list
from .get_result.gen_query_search import gen_query_search
import math

router = APIRouter()
#def get_search_tables(form):

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
  else:
    page=1


    #form.pre(f)

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
  
  for f in form.fields:
   if exists_arg('allready_out_on_result',f):
     form.R['query'].append([f['name'],""])
     form.query_search['on_filters_hash'][f['name']]=""

  for values in R['query']:
    form.query_search['on_filters_hash'][values[0]]=values[1]

  
  # 


  
  # если требуется подменить фильтры
  form.run_event('before_search_tables')

  form.get_search_tables(R['query'])
  
  form.get_search_where(R['query'])
  
  form.run_event('before_search')

  form.run_event('before_search_mysql',
    {
      'tables':' '.join(form.query_search['TABLES']),
      'where':' AND '.join(form.query_search['WHERE'])
    }
  )
  #   event=form.events[],
  #   description='events->before_search_mysql',
  #   form=form,
  #   arg={

  #   }
  # )
  
  (query,query_count)=gen_query_search(form)
  
  #print('query:',query,"\n\nquery_count:",query_count)
  if query_count:
    total_count=form.db.query(
      query='select sum(cnt) from ('+query_count+') x',
      onevalue=1,
      values=form.query_search['VALUES'],
      errors=form.errors
    )
    #print('errors:',form.errors)
    if total_count:
      total_count=int(total_count)
    else:
      total_count=0
    
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
  
  
  if form.explain:
    form.explain_query=query
    form.explain_query=form.explain_query+'<br><br>VALUES: ['+','.join(form.query_search['VALUES'])+']'

  if len(form.errors):
    return {'success':0,'errors':form.errors}




  output=process_result_list(form,R,result_list)
  form.SEARCH_RESULT['log']=form.log
  form.SEARCH_RESULT['output']=output
  form.run_event('after_search')
  
  if form.plugin_output:
    return form.plugin_output

  else : # not s['end'])

      return {
              'success':(1,0)[len(form.errors)],
              'results':form.SEARCH_RESULT,
              'errors':form.errors,
              'out_before_search':form.out_before_search,
              'javascript':form.javascript['find_objects'],
              'out_after_search':form.out_after_search,
              'explain_query':form.explain_query
      }
      



  if len(form.errors):
    return {'success':0,'errors':form.errors}

  return form.SEARCH_RESULT