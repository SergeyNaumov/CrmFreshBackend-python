from lib.anna.get_ul_list import get_ul_list_ids


        #form.pre(periods)

def permissions(form):
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
    if form.script=='table':
        permissions_table(form)
    
    

def permissions_table(form):
    # ap.plan=3   -- только % за любые закупки
    # Получаем id текущего периода
    ids=get_ul_list_ids(form)
    form.headers=[
        {'h':'юр лицо', 'n':'ur_lico'},
        {'h':'период','n':'querter'},
        {'h':'маркетинговое мероприятие','n':'action'},
        {'h':'%выполнения','n':'percent_complete'},
        {'h':'осталось выполнить в %','n':'left_to_complete_percent'},
        {'h':'осталось выполнить в рублях / штуках','n':'left_to_complete_rub'},

    ]
    # Залача: https://trello.com/c/2VGHgqn1/56-%D1%81%D0%B2%D0%BE%D0%B4%D0%BD%D1%8B%D0%B5-%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5-%D0%B2-%D0%BB%D0%BA-%D1%8E%D1%80%D0%BB%D0%B8%D1%86%D0%B0
    period_id=form.db.query(
        #query='SELECT id from prognoz_bonus_period where date_begin<=curdate() and (to_days(curdate())-to_days(date_begin) > 29) order by date_begin desc limit 1',
        query='SELECT id from prognoz_bonus_period where date_begin<=curdate()  order by date_begin desc limit 1',
        onevalue=1
    )
    #period_id=4
    #form.pre({'period_id':period_id})
    if not period_id:
        period_id=0

    query=f"""
         SELECT 
            wt.action_plan_id, wt.period_id,
            ul.header ur_lico,
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
            prognoz_bonus wt
            join action_plan ap on ap.id=wt.action_plan_id
            join prognoz_bonus_period per on per.id = wt.period_id
            join action a ON a.id=wt.action_id
            JOIN ur_lico ul ON wt.ur_lico_id=ul.id
        WHERE
            
            wt.ur_lico_id in ({','.join(ids)})
        ORDER BY wt.period_id desc
    """ #  wt.period_id={period_id} and 

    #print('query:',query)
    form.data=form.db.query(
        query=query,
        log=form.log,
        errors=form.errors,
        arrays=1
    )

    for d in form.data:
        if d['percent_complete']=='percent':
            d['percent_complete']='% за любые закупки'
        d['action']+=f"<br><small><a href='/edit-form/action_plan/{d['action_plan_id']}?open_summary=1&period={d['period_id']}' target='_blank'>сводные данные </a></small>"
        del d['action_plan_id']
        del d['period_id']
    form.sort=''
    #form.pre(form.data)
    


def before_search(form):
    qs=form.query_search
    qs['SELECT_FIELDS']=[
        'wt.id wt__id, ap.plan ap__plan',
        'ul.id ul__id','ul.header ul__header',
        'wt.action_plan_id wt__action_plan_id',
        'wt.period_id wt__period_id',
        'if(ap.plan=3,"percent",wt.percent_complete) percent_complete',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",wt.left_to_complete_percent) left_to_complete_percent',
        'if(ap.plan=3 or wt.percent_complete>=100,"выполнен", concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) ) left_to_complete_rub',
        #'if(ap.plan=3 or wt.percent_complete>=100,"выполнен",concat(wt.left_to_complete_rub," ",if(ap.plan=2,"шт","руб")) left_to_complete_rub',
        'per.year per__year, per.querter per__querter',
        'a.id a__id, a.header a__header'
    ]

    # periods=form.db.query(
    #   query="select id from prognoz_bonus_period  where date_begin>=from_days(to_days(curdate())-180) order by date_begin",
    #   massive=1,
    #   str=1
    # )

    # Ограничиваем поиск текущим и предыдущим периодом:
    # if len(periods):
    #     qs['WHERE'].append(f"wt.period_id IN ({','.join(periods)})")
    #     #form.pre(qs)
    #     print('periods:',periods)
    if form.manager['type']==2 and len(form.manager['ur_lico_ids']):
        qs['WHERE'].append(f"wt.ur_lico_id IN ({','.join(form.manager['ur_lico_ids'])})")
    # Для того, чтобы сортировка по "осталось выполнить...." работала верно
    #form.pre(form.manager['ur_lico_ids'])

    if len(qs['ORDER'])==1:

        if qs['ORDER'][0]=='wt.left_to_complete_percent ':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,101,wt.left_to_complete_percent)']
        elif qs['ORDER'][0]=='wt.left_to_complete_percent desc':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,101,wt.left_to_complete_percent) desc']

        elif qs['ORDER'][0]=='wt.left_to_complete_rub ':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,9999999999, wt.left_to_complete_rub)']
        elif qs['ORDER'][0]=='wt.left_to_complete_rub desc':
            qs['ORDER']=['if(ap.plan=3 or wt.percent_complete>=100,9999999999, wt.left_to_complete_rub) desc']
    print(qs)

events={
    'permissions':[permissions],
    'before_search':before_search
}
