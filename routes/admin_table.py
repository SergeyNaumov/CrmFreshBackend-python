from lib.core import cur_year,cur_date, success, exists_arg
from fastapi import FastAPI, APIRouter
from config import config
from lib.CRM.filters import get_filters
from lib.engine import s
from lib.run_event import run_event
from lib.all_configs import read_config


router = APIRouter()
def gen_query_search(form):
  print(1)

@router.get('/get-filters/{config}')
async def get_filters_controller(config: str):
  return get_filters(
    config=config,
    script='admin_table',
    #R=R
  )


@router.post('/get-result')
async def get_result(R: dict):
  form=read_config(
    R=R,
    config=R['config'],
    script='find_objects'
  )

  if exists_arg('page',R):
    page=str(R['page'])
    if page.isnumeric(): form.page=R[page]

  params={}


  if exists_arg('params',R):
    params=R['params']
  
    if exists_arg('priority_sort',params):
      priority_sort=params['priority_sort']
      if len(priority_sort)==2 and priority_sort[1] in ('asc','desc'):
        form.priority_sort=priority_sort
    

  form.query_search={
    'on_filters_hash':{},
    'SELECT_FIELDS':[],
    'WHERE':[],
    'ORDER':[],
    'TABLES':[],
    'GROUP':[]
  }

  if form.GROUP_BY: form.query_search['GROUP'].append(form.GROUP_BY)

  form.search_result={
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
      errors=form.errors
    )
    form.SEARCH_RESULT['total_count']=total_count
    #$form->{SEARCH_RESULT}->{count_pages}=($form->{not_perpage})?1:( ceil($total_count/$form->{perpage}) );
    #form.SEARCH_RESULT['count_pages']
  return form.search_result