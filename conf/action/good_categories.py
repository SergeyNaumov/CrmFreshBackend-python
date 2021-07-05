from lib.core import  date_to_rus
def good_categories(form,field):
  #'Здесь будет какая-то инфа'

  if form.id and form.ov:

    plan_list=form.db.query(
      query='''
        SELECT
          ap.id,ap.header,ap.begin_date,ap.end_date,ap.value,ap.reward_percent,ap.allgood,plan,
          man.header manufacturer, ap.manufacturer_id

        FROM
          action_plan ap
          LEFT JOIN manufacturer man ON man.id = ap.manufacturer_id
        WHERE  action_id=%s ORDER BY ap.end_date desc
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

    #print('plan_list:',plan_list)
    field['type']='accordion'

    # собираем аккордион
    accordion_data=[]

    table_headers=[{'h':'Штрих код товара'},{'h':'Наименование'}]
    table_data=[]

    if form.ov['subscribed_on_action']:
      table_headers.append({
        'h':'Витрина',
        'tooltip':{
          'header':'Витрина',
          'body':'По условиям контракта, товар должен быть выложен на полке'
        }
      })
    
    table_headers.append({'h':'Сип-цена'})
    # not p['reward_percent'] and 
    if form.ov['subscribed_on_action']:
      table_headers.append({
        'h':'Начисления<br> по бонусу',
        'tooltip':{
          'header':'Бонус',
          'body':'% бонуса зависит от закупленного товара. Каждый товар имеет свой % бонуса'
        }
      })


    for p in plan_list:
      
      #form.pre({'p':p})
      for g in p['child']:
        table_tr=[]
        table_tr.append(g['code']) # код
        table_tr.append(g['header']) # наименование
        if form.ov['subscribed_on_action']: # витрина
          table_tr.append(g['showcase'])

        if g['price']==0:
          table_tr.append('закупочная цена')
        else:
          table_tr.append(g['price'])

        if not p['reward_percent'] and form.ov['subscribed_on_action']:
          table_tr.append(g['percent'])

        table_data.append(table_tr)
      
      

      data_item={
        'header':p['header']+'('+p['begin_date']+'..'+p['end_date']+')',
        'content':[]
      }
      # проверяем, есть ли прогнозный бонус для данного юрлица
      #form.pre({'exists_prognoz_bonus':exists_prognoz_bonus(form,p['id'])})
      
      if exists_prognoz_bonus(form,p['id']):
        data_item['content'].append({
          'type':'html',
          'body':f'''<p><b><a href="/edit_form/action_plan/{p['id']}" target="blank">прогнозный бонус</a></b></p>'''
        })

      if form.ov['subscribed_on_action']:
        body=f'''
          План: {p['plan']}<br>
          {p['value_name']}: {p['value']}<br>
        '''

        if p['reward_percent']:
          body+=f'% бонуса: {p["reward_percent"]}<br>'

        body+=f'''<div class="download_block">
          <a href="/backend/anna/download/action_plan/xls/{p['id']}" target="_blank">скачать в xls</a>
          <!--  |  <a href="/backend/anna/download/action_plan/dbf/{{p.id}}">скачать в dbf</a>-->
        </div>'''
        data_item['content'].append({'type':'html','body':body})


      accordion_data.append(data_item)
      if len(table_data):
        data_item['content'].append({
          'type':'table',
          'table':{
            'sort':1,
            'sort_desc':False,
            'headers':table_headers,
            'data':table_data
          }
        })

    field['data']=accordion_data
    if len(table_data):
      field['before_html']='<h2 style="margin-top: 20px;">Группы товаров</h2>'
    else:
      field['before_html']='<p style="margin-top: 20px; color: red;">Группы товаров отсутствуют</p>'
    #form.pre(accordion_data)
    #form.pre({'plan_list':plan_list})
    #form.pre(accordion_data)
    # #form.pre(plan_list)
    # field['after_html']=form.template(
    #   './conf/action/templates/good_categories.html',
    #   plan_list=plan_list,
    #   ov=form.ov,
    #   manager=form.manager,
    #   ur_lico_subscribe=form.ur_lico_subscribe
    # )
    #form.javascript['edit_form']+=form.template('./conf/action/templates/good_categories.js')
def exists_prognoz_bonus(form,action_plan_id):
  need=False
  if form.script=='edit_form' and form.action=='edit' and form.ov:
    if form.manager['type']==2: # юридическое лицо
      if len(form.manager['ur_lico_ids']):

        return form.db.query(
          query=f'''
            select count(*) from prognoz_bonus where action_id=%s and action_plan_id=%s and ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})
          ''',
          values=[form.ov['id'],action_plan_id],
          onevalue=1
        )
    elif form.manager['type']==3: # аптека
      pass
