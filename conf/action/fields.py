
def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Название',
      'type':'text',
      'filter_code':header_filter_code,
      'read_only':1,
      'filter_on':1,
      'tab':'main'
    },
    {
      'name':'date_start',
      'description':'Начало подписки',
      'type':'date',
      'tab':'main',
      'filter_on':1
    }, 
    {
      'name':'date_stop',
      'description':'Окончание подписки',
      'type':'date',
      'default_off':1,
      'tab':'main',
      'filter_on':1
    },
    {
      'name':'good_categories',
      'description':'Группы товаров',
      'type':'accordion',
      'tab':'goods',
      # Запрос для вывода заголовках аккордиона
      'headers_query':'SELECT id,header from action_plan where action_id=<id>',
      
    },
    # {
    #   'name':'good_categories',
    #   'type':'code',
    #   'tab':'goods',
    #   'description':'категории товаров',
    #   'code':good_categories
    # },
    {
      'name':'distrib',
      'description':'Разрешённые дистрибьюторы',
      'type':'code',
      'tab':'distrib',
      'code':distrib_code
    }
]


def distrib_code(form,field):
  if form.script == 'edit_form' and form.action=='edit':
    suppliers_lst=form.db.query(
      query='''
        select
          s.header
        from
          action_plan ap
          LEFT JOIN action_plan_supplier aps ON aps.action_plan_id=ap.id
          LEFT JOIN supplier s ON s.id = aps.supplier_id
        WHERE ap.action_id=%s and s.id is not null GROUP BY s.id ORDER BY s.header 
      ''',
      massive=1,
      values=[form.id]
    )
    field['after_html']='<br>'.join(suppliers_lst)
  
  
def header_filter_code(form,field,row):
  return f'<a href="/edit-form/action/{row["wt__id"]}" target="_blank">{row["wt__header"]}</a>'

def good_categories(form,field):
  #'Здесь будет какая-то инфа'

  if form.id:
    plan_list=form.db.query(
      query='''
        SELECT
          ap.id,ap.header,ap.begin_date,ap.end_date,ap.value,ap.reward_percent,ap.allgood,plan,
          man.header manufacturer, ap.manufacturer_id

        FROM
          action_plan ap
          LEFT JOIN manufacturer man ON man.id = ap.manufacturer_id
        WHERE action_id=%s
      ''',
      values=[form.id]
    )
    plan_ids=[]
    plan_dict={}
    for p in plan_list:
      plan_ids.append( str(p['id']) )
      p['child']=[]

      plan_dict[p['id']]=p
      if p['plan'] == 1:
        p['plan']='суммовой'
        p['value_name']='Сумма от'
      elif p['plan'] == 2:
        p['plan']='количественный'
        p['value_name']='Кол-во'
      elif p['plan'] == 3:
        p['plan']='только процент за любые закупки'
        p['value_name']='Выплачиваемый процент'
    

    if len(plan_ids):
      good_list=form.db.query(query='''
        SELECT
          ag.action_plan_id plan_id, g.header,
          if(g.showcase='0','нет','да') showcase,
          g.price, g.code, g.percent
        from 
          action_plan_good ag
          JOIN good g ON ag.good_id=g.id
        WHERE ag.action_plan_id in ('''+','.join(plan_ids)+')',
        
      )

      for g in good_list:
        plan_dict[g['plan_id']]['child'].append(g)

    #form.pre(plan_list)
    field['after_html']=form.template(
      './conf/action/templates/good_categories.html',
      plan_list=plan_list
    )
    form.run_js=form.template('./conf/action/templates/good_categories.js')