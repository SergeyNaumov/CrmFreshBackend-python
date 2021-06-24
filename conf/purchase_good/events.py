from lib.anna.get_apt_list import get_apt_list_ids, apt_list_id_for_apt
from lib.CRM.plugins.search.xlsx import go as init_search_plugin

def events_permissions(form):
  
  init_search_plugin(form)
  if form.manager['type']==2:
    
    apt_list_ids=get_apt_list_ids(form, form.manager['id'])
    form.manager['apt_list_ids']=apt_list_ids
    

  elif form.manager['type']==3:
    form.manager['apt_list_ids']=apt_list_id_for_apt(form,form.manager['id'])
    

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
  query_count='''
    select
      count(*) cnt
    from
      purchase_good wt
      LEFT JOIN purchase p ON p.id=wt.purchase_id
      LEFT JOIN action  act ON p.action_id=act.id
      LEFT JOIN apteka a ON wt.apteka_id = a.id
    '''
  if not('action_id' in qs['on_filters_hash']) or not qs['on_filters_hash']['action_id']:
    form.errors.append('Нужно обязательно выбрать "Название маркетингового мероприятия"')

  if len(qs['WHERE']):
    query_count+=' WHERE '+' AND '.join(qs['WHERE'])
  qs['query_count']=query_count
  sf=form.query_search['SELECT_FIELDS']
  
  #sf.append('group_concat(s2.header SEPARATOR ", ") suppliers2')
  sf.append('ap.header ap__header')
  if form.manager['type'] in (2,3):
    form.query_search['WHERE'].append(f'''wt.apteka_id in ({','.join(form.manager['apt_list_ids']) })''')
    
  print(form.query_search['WHERE'])
  # # для аптеки делаем ограничение
  # if form.manager['type']==3:
    
  #   form.query_search['WHERE'].append(f"wt.apteka_id={form.manager['id']}")

  form.out_before_search=''
  #form.explain=1

events={
  'before_search':before_search,
  'permissions':[
      events_permissions
  ],
  'after_search':[]
}