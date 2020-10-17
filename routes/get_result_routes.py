from lib.core import cur_year,cur_date, success, exists_arg
from fastapi import APIRouter
from config import config

from lib.engine import s
from lib.run_event import run_event
from lib.all_configs import read_config


router = APIRouter()
#def get_search_tables(form):

def gen_query_search(form):
  query=''
  query_count=''
  qs=form.query_search
  if exists_arg('ORDER',qs):
    if not isinstance(qs,list): qs['ORDER']=[qs['ORDER']]
  else:
    qs['ORDER']=[]

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
        if not isinstance(qs['ORDER'],list): 
          qs['ORDER']=[qs['ORDER']]
        if len(qs['ORDER']):
          query = query + ' ORDER BY '+', '.join(qs['ORDER'])

      if not form.not_perpage:
        perpage=int(form.perpage)
        page=int(form.page)
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
    'card_format':form.card_format
  }

  for values in R['query']:
    form.query_search['on_filters_hash'][values[0]]=values[1]

  form.get_search_tables(R['query'])
  form.get_search_where(R['query'])
  
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
  
  
  if query_count:
    total_count=form.db.query(
      query='select sum(cnt) from ('+query_count+') x',
      onevalue=1,
      debug=1,
      errors=form.errors
    )

    form.SEARCH_RESULT['total_count']=total_count
    #$form->{SEARCH_RESULT}->{count_pages}=($form->{not_perpage})?1:( ceil($total_count/$form->{perpage}) );

  if len(form.errors):
    return {'success':0,'errors':form.errors}

  return form.SEARCH_RESULT