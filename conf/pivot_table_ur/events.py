from lib.anna.get_ul_list import get_ul_list_ids
def permissions(form):
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

    ids=get_ul_list_ids(form)

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
    qs['SELECT_FIELDS']=[
        'wt.id wt__id, ap.plan ap__plan',
        'wt.action_plan_id wt__action_plan_id',
        'm.login m__login','m.comment m__comment',
        'if(ap.plan=3,"percent",wt.percent_complete) percent_complete',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",wt.left_to_complete_percent) left_to_complete_percent',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен", concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) ) left_to_complete_rub',
        #'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) left_to_complete_rub',
        'per.year per__year, per.querter per__querter',
        'a.id a__id, a.header a__header'
    ]

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

events={
    'permissions':[permissions],
    'before_search':before_search
}
