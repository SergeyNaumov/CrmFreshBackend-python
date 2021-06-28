from lib.core import  date_to_rus
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
      p['begin_date']=date_to_rus(p['begin_date'])
      p['end_date']=date_to_rus(p['end_date'])
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
      plan_list=plan_list,
      ov=form.ov,
      manager=form.manager,
      ur_lico_subscribe=form.ur_lico_subscribe
    )
    #form.javascript['edit_form']+=form.template('./conf/action/templates/good_categories.js')
