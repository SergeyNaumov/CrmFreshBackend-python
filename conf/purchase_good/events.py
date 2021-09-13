from lib.anna.get_apt_list import get_apt_list_ids, apt_list_id_for_apt
from lib.CRM.plugins.search.xlsx import go as init_search_plugin
from lib.anna.get_ul_list import get_ul_list_ids
def events_permissions(form):
  
  init_search_plugin(form)
  if form.manager['type']==2:
    
    apt_list_ids=get_apt_list_ids(form, form.manager['id'])
    form.manager['apt_list_ids']=apt_list_ids
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])

  elif form.manager['type']==3:
    form.manager['apt_list_ids']=apt_list_id_for_apt(form,form.manager['id'])
    form.remove_field('apteka_id')
    form.remove_field('ur_lico_id')

  for f in form.fields:
    f['read_only']=1
  
  if form.script=='find_objects':
    fld=form.get_field('date_start')
    fld['description']='Даты мероприятия'

    new_query=[]
    
    # чтобы не попало в headers (в результат), убираем из поискового запроса (R['query'])
    for p in form.R['query']:
      if not(p[0]=='suppliers' and not p[1]) and  not(p[0]=='date_start' and not p[1]):
        new_query.append(p)

    form.R['query']=new_query

def before_search(form):
  qs=form.query_search
  sf=qs['SELECT_FIELDS']
  if not('action_id' in qs['on_filters_hash']) or not qs['on_filters_hash']['action_id']:
    form.errors.append('Нужно обязательно выбрать "Название маркетингового мероприятия"')


  
  #form.explain=1
  if 'priority_sort' in form.R['params']:
    ps=form.R['params']['priority_sort']
    if len(ps)==2:
      if ps[0]=='suppliers':
        qs['ORDER']=[f's2.header {ps[1]}']
    #form.pre(form.R['params']['priority_sort'])


#  form.pre(form.query_search)
  sf.append('group_concat(s2.header SEPARATOR ", ") suppliers2')
  sf.append('ap.header ap__header')
  if form.manager['type']==2: # in (2,3):
    form.query_search['WHERE'].append(f'''wt.apteka_id in ({','.join(form.manager['apt_list_ids']) })''')
  elif form.manager['type']==3:
    form.query_search['WHERE'].append(f'''a.manager_id = {form.manager['id']}''')
  query_count='''
    select
      count(*) cnt
    from
      purchase_good wt
      LEFT JOIN purchase p ON p.id=wt.purchase_id
      LEFT JOIN action  act ON p.action_id=act.id
      LEFT JOIN apteka a ON wt.apteka_id = a.id
      LEFT JOIN ur_lico ul ON a.ur_lico_id=ul.id
      LEFT JOIN action_plan ap ON ap.action_id=act.id
    '''

  if len(qs['WHERE']):
    query_count+=' WHERE '+' AND '.join(qs['WHERE'])
  qs['query_count']=query_count

  #form.out_before_search=''
  #form.out_before_search.append('<h2>Данные по закупкам отображаются по всем поставщикам</h2>')
  #form.explain=1

events={
  'before_search':[before_search],
  'permissions':[
      events_permissions
  ],
  'after_search':[]
}