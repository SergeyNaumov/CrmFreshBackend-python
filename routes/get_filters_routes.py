from fastapi import APIRouter
from lib.core import is_errors, create_fields_hash, exists_arg
from lib.all_configs import read_config

router = APIRouter()



def get_values_for_select_from_table(f,form):
  return []


@router.get('/get-filters/{config}')
@router.post('/get-filters/{config}')
async def get_filters_controller(config: str, R:dict):
  response={}
  #print('R0:',R)
  form=read_config(
    config=config,
    R=R,
    script='admin_table'
  )
  

  if is_errors(form):
    return {
      'success':0,
      'errors':form.errors
    }

  filters=[]
  order=1
  
  for f in form.fields:
    if f.get('name')=='brand_id':
      print(f"{f['name']} {f.get('value')}")
    # if(ref($f->{before_code}) eq 'CODE'){
    #   run_event(event=>$f->{before_code},description=>'before_code for '.$f->{name},form=>$form,arg=>$f);
    # }
    if exists_arg('not_filter',f) or exists_arg('allready_out_on_result',f):
      continue
    if f['type'] in ('password','code','1_to_m','hidden'): continue

    if f['type'] in ('textarea','filter_extend_text','text'):
      f['type']='text'
    elif f['type'] in ('select_values','filter_extend_select_values'):
      f['type']='select'
    
    elif f['type'] == 'filter_extend_date':
      f['type']='date'
    
    elif f['type'] in ('filter_extend_select_from_table','select_from_table'):
      f['type']='select'
      if not(exists_arg('header_field',f)): f['header_field']='header'
      if not(exists_arg('value_field',f)): f['value_field']='id'
      
      if not exists_arg('values',f):
        f['values']=get_values_for_select_from_table(f,form)

    elif f['type']=='memo':
      f['users']=form.db.query(
        query='SELECT '+f['auth_id_field']+' v, '+f['auth_name_field']+' d from '+f['auth_table']+' ORDER BY '+f['auth_name_field'],
        errors=form.log
      )

    if f['type'] in ('date','time','datetime','daymon','yearmon') and not exists_arg('filter_type',f) : 
      f['range']=1
      #print(f['name'],f)
    
    if exists_arg('filter_type',f) and f['filter_type'] == 'range':
      f['range']=1
    
    for k in ('tablename','db_name','regexp_rules','regexp','tab','where','table_id','header_field','value_field','empty_value'): # 'filter_type' -- убрал, потому что появился filter_type: checkbox
      if exists_arg(k,f): del f[k]
    
    # order исправил на _order (конфиликтовал с беком в запросах)
    if exists_arg('filter_on',f):
      f['filter_order']=order
      order+=1

    filters.append(f)

  make_create=1
  if form.not_create: make_create=0
  search_multi_action=[]
  if hasattr(form,'search_multi_action'):
    search_multi_action=form.search_multi_action
  return {
    'success':1,
    'title':form.title,
    'filters':filters,
    'search_links':form.search_links,
    'before_filters_html':form.before_filters_html,
    'javascript':exists_arg('admin_table',form.javascript),
    #form.javascript['admin_table'],
    'filters_groups':form.filters_groups,
    'log':form.log,
    'search_plugin':form.search_plugin,
    'search_multi_action':search_multi_action,
    'permissions':{
      'make_create':make_create,
      'make_delete':form.make_delete,
      'not_edit':form.not_edit
    },
    'on_filters':form.on_filters,
    'search_plugin':form.search_plugin,
    'search_on_load':form.search_on_load,
    'errors':form.errors
  }
