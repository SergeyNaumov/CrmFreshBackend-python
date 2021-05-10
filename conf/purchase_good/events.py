def events_permissions(form):
    
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
    '''
  if not('action_id' in qs['on_filters_hash']) or not qs['on_filters_hash']['action_id']:
    form.errors.append('Фильтр "мероприятие" обязателен')

  if len(qs['WHERE']):
    query_count+=' WHERE '+' AND '.join(qs['WHERE'])
  qs['query_count']=query_count
  sf=form.query_search['SELECT_FIELDS']
  
  sf.append('group_concat(s2.header SEPARATOR ", ") suppliers2')

  form.out_before_search=''
    

events={
  'before_search':before_search,
  'permissions':[
      events_permissions
  ],
}