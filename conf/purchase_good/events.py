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


  #form.pre(qs)
  
  #form.explain=1
  if 'priority_sort' in form.R['params']:
    ps=form.R['params']['priority_sort']
    if len(ps)==2:
      if ps[0]=='suppliers':
        qs['ORDER']=[f's2.header {ps[1]}']
    #form.pre(form.R['params']['priority_sort'])


  #form.pre(form.query_search)
  #sf.append('group_concat(s2.header SEPARATOR ", ") suppliers2')
  #sf.append('ap.header ap__header')
  #form.pre(qs['GROUP'])
  #form.pre(sf)
  # Будем суммировать товары
  qs['SELECT_FIELDS']=[
      "wt.id wt__id",
      "wt.purchase_id wt__purchase_id",
      "wt.apteka_id wt__apteka_id",
      "wt.supplier_id wt__supplier_id",
      "wt.header wt__header",
      "wt.code wt__code",
      
      "wt.action_plan_id wt__action_plan_id",
      "p.id p__id",
      "p.date p__date",
      "p.action_id p__action_id",
      "act.id act__id",
      "act.header act__header",
      "a.id a__id",
      "a.header a__header",
      "a.ur_address a__ur_address",
      "a.subscribe a__subscribe",
      "a.on_notify a__on_notify",
      "a.key_from_1c a__key_from_1c",
      "a.ur_lico_id a__ur_lico_id",
      "ul.id ul__id",
      "ul.header ul__header",
      "ul.subscribe ul__subscribe",
      "ul.key_from_1c ul__key_from_1c",
      "ul.anna_manager_id ul__anna_manager_id",
      "ul.phone ul__phone",
      "ul.parent_id ul__parent_id",
     
      "ap.header ap__header",
      "ap.id ap__id",
     # 'wt.cnt wt__cnt',
     # "wt.summ wt__summ",
  ]

  # "group_concat(distinct s2.header SEPARATOR \", \") suppliers2",

  on_filter_hash=qs['on_filters_hash']
  
  if 'apteka_id' in on_filter_hash: # группируем по наименованию товара и по аптеки
    qs['GROUP']=['a.id, wt.header']
  elif 'ur_lico_id' in on_filter_hash:
    qs['GROUP']=['wt.header, ul.id']
  else:
    qs['GROUP']=['wt.header'] # , wt.header, ur_lico_id
  
  #form.pre(qs)

  if form.manager['type']==2: # in (2,3):
    qs['WHERE'].append(f'''wt.apteka_id in ({','.join(form.manager['apt_list_ids']) })''')
  elif form.manager['type']==3:
    qs['WHERE'].append(f'''a.manager_id = {form.manager['id']}''')

  #WHERE_CNT=[]

  if 'cnt' in qs['on_filters_hash']:
    cnt_val=qs['on_filters_hash']['cnt']
    if cnt_val[0] and cnt_val[0].isdigit():
      qs['WHERE'].append(f" wt.cnt>={cnt_val[0]}")
    
    if cnt_val[1] and cnt_val[1].isdigit():
      qs['WHERE'].append(f" wt.cnt<={cnt_val[1]}")

    #if len(WHERE_CNT):
    #  WHERE_CNT=f"WHERE {' AND '.join(WHERE_CNT)}"
    
    if 'priority_sort' in  form.R['params']:
      PS=form.R['params']['priority_sort']
      if PS[0]=='cnt':
        desc=''
        if PS[1]=='desc': desc='desc'
        qs['ORDER'].append(f"wt.cnt {desc}")
      

  # ДЛЯ ТОГО, чтобы кол-во считалось верно -- пишем свой запрос
  WHERE=''


  if len(qs['WHERE']):
    WHERE=f' WHERE {" AND ".join(qs["WHERE"]) } '
  WHERE2=WHERE.replace('.','__')

  GROUP=''
  if len(qs['GROUP']):
    GROUP=f' GROUP BY {" ".join(qs["GROUP"]) } '
  GROUP2=GROUP.replace('.','__')

  ORDER=''
  if len(qs['ORDER']):
    ORDER=f' ORDER BY {", ".join(qs["ORDER"]) } '
  ORDER2=ORDER.replace('.','__')
  

  perpage=int(form.perpage)
  page=int(form.page)
  LIMIT=''
  if not form.not_perpage:
    LIMIT = f' LIMIT { (page-1)*perpage },{form.perpage}'
  #form.pre({'LIMIT':LIMIT})


  # Q=f'''
  #    SELECT *, sum(wt__cnt) wt__cnt, sum(wt__summ) wt__summ
  #    FROM
  #     (
  #        SELECT
  #          {','.join(qs['SELECT_FIELDS'])}
  #        FROM
  #          {" ".join(qs['TABLES'])}
  #        {WHERE}
  #        {GROUP}
  #        {ORDER}
         
  #    ) x
  #    {GROUP2} {ORDER2}
  #'''
  #form.explain=1

    #form.pre(isinstance(cnt_val[1],str) )
    #if(cnt_val[0].isgigit()):
    #  form.pre(cnt_val[0])
    
    #if(cnt_val[1].isgigit()):
    #  form.pre(cnt_val[1])

  Q=f'''
  SELECT * FROM
  (
   SELECT
     {','.join(qs['SELECT_FIELDS'])}, sum(wt.cnt) wt__cnt, sum(wt.summ) wt__summ
   FROM
     {" ".join(qs['TABLES'])}
   {GROUP} 
  ) x {WHERE2} {ORDER2}
  '''
  #form.pre(Q)
  form.QUERY_SEARCH=Q

  qs['query_count']=f'''
    SELECT
      count(*) cnt
    from
    (
      SELECT
        wt.id
      FROM
        {" ".join(qs['TABLES'])}
      {WHERE}
      {GROUP}
    ) x
  '''

  suppliers={}

  query_supplier=f'''
    SELECT
      wt.id, group_concat(distinct s2.header SEPARATOR \", \") suppliers2
    FROM
      {" ".join(qs['TABLES'])}
      LEFT JOIN action_plan_supplier aps ON aps.action_plan_id=ap.id
      LEFT JOIN supplier s2 ON s2.id=aps.supplier_id
    {WHERE}
    {GROUP}
  '''
  # Собираем информацию о поставщиках
  if ('suppliers' in qs['on_filters_hash']):
      suppliers_list=form.db.query(
        query=query_supplier,
        values=form.query_search['VALUES'],
        #debug=1
      )
      for s in suppliers_list:
        suppliers[s['id']]=s['suppliers2']
      
      suppliers_list=None
      form.suppliers=suppliers


def after_search(form):
  form.pre(form.SEARCH_RESULT)

events={
  'before_search':[before_search],
  'permissions':[
      events_permissions
  ],
  #'after_search':[after_search]
}