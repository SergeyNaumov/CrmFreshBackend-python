from lib.anna.get_ul_list import get_ul_list_ids
def manager_id_filter_code(form,field,row):
  if row['m__comment']:
    return f"{row['m__login']} - {row['m__comment']}"
  return row['m__login']

def manager_id_before_code(form,field):
  # узнаём, какие логины вообще у нас есть
  ids1=form.db.query(query="SELECT distinct(manager_id) FROM prognoz_bonus_pivot_ul",massive=1,str=1)
  #if form.manager['type']==2:
  #  form.pre(form.manager)

  if len(ids1):
    where=f"""id in ({','.join(ids1)})"""
    if form.manager['type']==2:
      if len(form.manager["ids"]):
        where=f'{where} and  id in ({",".join(form.manager["ids"])})'
      else:
        where=' 0 '

    field['values']=form.db.query(
      query=f"""
        SELECT
          id v,
          concat( login,if(comment='','',concat(' - ',comment))) d
        FROM
          manager
        WHERE {where}
        ORDER BY login
      """
    )
    
def permissions(form):
    #form.pre(form.script)
    if form.manager['type']==1:
        form.fields.append(
            {
            'description':'Логин',
            'type':'select_values',
            'name':'manager_id',
            'values':[],
            'filter_on':1,
            'before_code':manager_id_before_code,
            'filter_code':manager_id_filter_code
            }
        )
    if form.manager['type']==2:
        form.manager['ids']=get_ul_list_ids(form)

    if form.script=='table':
        permissions_table(form)
    


def permissions_table(form):

    form.headers=[
        {'h':'период','n':'querter'},
        {'h':'маркетинговое мероприятие','n':'action'},
        {'h':'%выполнения','n':'percent_complete'},
        {'h':'осталось выполнить в %','n':'left_to_complete_percent'},
        {'h':'осталось выполнить в рублях / штуках','n':'left_to_complete_rub'},
    ]
    form.sort='action' # поле, по которому сортируем изначально
    form.sort_desc=False
    
    
    
# ap.plan=3   -- только % за любые закупки
    # Получаем id текущего периода
    period_id=form.db.query(
        query='SELECT id from prognoz_bonus_period where date_begin<=curdate() order by date_begin desc limit 1',
        onevalue=1
    )

    if not period_id:
        period_id=0

    query=f"""
         SELECT 
            wt.action_plan_id, wt.period_id,
            
            concat(per.year,'-',per.querter) as querter,
            a.header action,
            
            if(ap.plan=3,
                'percent',
                wt.percent_complete
            ) percent_complete,

            if(
                ap.plan=3 or wt.percent_complete>=100,
                'выполнен',
                wt.left_to_complete_percent
            ) as left_to_complete_percent,
            
            if(
                ap.plan=3 or wt.percent_complete>=100,
                'выполнен',
                concat(wt.left_to_complete_rub,' ',if(ap.plan=2,'шт','руб'))

            )
            left_to_complete_rub

         from
            prognoz_bonus_pivot_ul wt
            join action_plan ap on ap.id=wt.action_plan_id
            join prognoz_bonus_period per on per.id = wt.period_id
            join action a ON a.id=wt.action_id
        WHERE
            wt.period_id={period_id} and wt.manager_id={form.manager['id']}

    """ 
    # 
    form.data=form.db.query(
        query=query,
        log=form.log,
        errors=form.errors,
        arrays=1
    )

    for d in form.data:
        if d['percent_complete']=='percent':
            d['percent_complete']='% за любые закупки'
        d['action']+=f" <small><a href='/edit-form/action_plan/{d['action_plan_id']}?open_summary=1' target='_blank'>сводные данные</a></small>"
        del d['action_plan_id']
        del d['period_id']
    form.sort=''
    #form.pre(form.data)
    

def before_search(form):
    qs=form.query_search
    
    # Собираем соответствие manager_id и ur_lico_id
    ids=form.db.query(query="SELECT distinct(manager_id) FROM prognoz_bonus_pivot_ul",massive=1,str=1)
    manager_ur_lico=[]
    form.manager_ur_lico={}
    if len(ids):
        manager_ur_lico=form.db.query(
            query=f'select manager_id,ur_lico_id from ur_lico_manager where manager_id in ({",".join(ids)}) group by manager_id',
           
        )
    
    for mu in manager_ur_lico:
        form.manager_ur_lico[mu['manager_id']]=mu['ur_lico_id']

    #form.pre(form.manager_ur_lico)

    qs['SELECT_FIELDS']=[
        'wt.id wt__id, ap.plan ap__plan, wt.manager_id wt__manager_id',
        'wt.action_plan_id wt__action_plan_id',
        'm.login m__login','m.comment m__comment',
        'ap.header ap__header',
        'if(ap.plan=3,"percent",wt.percent_complete) percent_complete',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",wt.left_to_complete_percent) left_to_complete_percent',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен", concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) ) left_to_complete_rub',
        #'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) left_to_complete_rub',
        'per.year per__year, per.querter per__querter, per.date_begin per__date_begin',
        'a.id a__id, a.header a__header'
    ]
    if form.manager['type']==2:
        qs['WHERE'].append(f"wt.manager_id={form.manager['id']}")
    
    # Для того, чтобы сортировка по "осталось выполнить...." работала верно
    if len(qs['ORDER'])==1:

        if qs['ORDER'][0]=='wt.left_to_complete_percent ':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,101,wt.left_to_complete_percent)']
        elif qs['ORDER'][0]=='wt.left_to_complete_percent desc':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,101,wt.left_to_complete_percent) desc']

        elif qs['ORDER'][0]=='wt.left_to_complete_rub ':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,9999999999, wt.left_to_complete_rub)']
        elif qs['ORDER'][0]=='wt.left_to_complete_rub desc':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,9999999999, wt.left_to_complete_rub) desc']
        elif qs['ORDER'][0]=="per.period_id desc":
            qs['ORDER']=['per.date_begin desc']
        elif qs['ORDER'][0]=="per.period_id ":
            qs['ORDER']=['per.date_begin']

events={
    'permissions':[permissions],
    'before_search':before_search
}
