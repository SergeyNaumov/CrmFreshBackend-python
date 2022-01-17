from lib.core import  date_to_rus
from lib.anna.get_cur_period import get_cur_period



def good_categories(form,field):
  #'Здесь будет какая-то инфа'
  
  #currentYear = datetime.now().year
  #form.pre([currentYear,currentMonth])
  # Текущий квартал, сколько дней прощло с начала квартала)
  #(querter,querter_begin_days)=get_cur_querter()
  cur_period=get_cur_period(form)
  prev_period=get_cur_period(form,1)

  
  set1=True # True -- показываем график выболнения плана (apteka_settings.set1)
  set2=True

  if form.manager['type']==3:
    set1=form.manager['apteka_settings']['set1']
    set2=form.manager['apteka_settings']['set2']


  #form.pre(form.manager)
  #form.pre([cur_period,prev_period])
  if form.id and form.ov:

    plan_list=form.db.query(
      query='''
        SELECT
          ap.id,ap.header,ap.begin_date,ap.end_date,ap.value,ap.reward_percent,ap.allgood,plan,
          man.header manufacturer, ap.manufacturer_id

        FROM
          action_plan ap
          LEFT JOIN manufacturer man ON man.id = ap.manufacturer_id
        WHERE  action_id=%s and ap.begin_date>=%s ORDER BY ap.end_date desc
      ''',
      values=[form.id, prev_period['date_begin']]
    )
    plan_ids=[]
    plan_dict={}
    good_list=[]
    
    show_percent=0

    for p in plan_list:
      plan_ids.append( str(p['id']) )
      p['child']=[]
      p['begin_date']=date_to_rus(p['begin_date'])
      p['end_date']=date_to_rus(p['end_date'])
      #plan_dict[p['id']]=p
      if p['plan'] == 1:
        p['plan_label']='суммовой'
        p['value_name']='Сумма от'
      elif p['plan'] == 2:
        p['plan_label']='количественный'
        p['value_name']='Кол-во'
      elif p['plan'] == 3:
        p['plan_label']='% за любые закупки'
        p['value_name']='Выплачиваемый процент'
      elif p['plan'] == 4:
        p['plan_label']='начисление по бонусу (индивидуальный бонус по товарам)'
        p['value_name']='Выплачиваемый процент'
        show_percent=1
      elif p['plan'] == 5:
        p['plan_label']='начисление по бонусу (в рублях)'
        p['value_name']='Выплачиваемый процент'
        show_percent=1

    if len(plan_ids):
      good_list=form.db.query(query='''
        SELECT
          ag.action_plan_id plan_id, g.header,
          if(g.showcase='0','нет','да') showcase,
          g.price, g.code, g.percent, g.summa
        from 
          action_plan_good ag
          JOIN good g ON ag.good_id=g.id
        WHERE ag.action_plan_id in ('''+','.join(plan_ids)+')',
        
      )
      #form.pre(good_list)
      #for g in good_list:
      #    plan_dict[g['plan_id']]['child'].append(g)
    

    for p in plan_list:
      for g in good_list:
        if g['percent']>0: show_percent=1
        if g['plan_id']==p['id']:
          #form.pre(f"""{g['header']} append to {p['header']} """)
          p['child'].append(g)

    #form.pre(plan_list)
    field['type']='accordion'

    # собираем аккордион
    accordion_data=[]



    table_data=[]
    for p in plan_list:
      table_headers=[{'h':'Штрих код товара'},{'h':'Наименование'}]
    

      if form.ov['subscribed_on_action'] or form.manager['type']==1:
        table_headers.append({
          'h':'Витрина',
          'tooltip':{
            'header':'Витрина',
            'body':'По условиям контракта, товар должен быть выложен на полке'
          }
        })
    
      table_headers.append({'h':'Сип-цена'})
      if show_percent and (form.ov['subscribed_on_action'] or form.manager['type']==1):
        if p['plan'] in (1,2,4):
          table_headers.append({
            'h':'Начисления<br> по бонусу',
            'tooltip':{
              'header':'Бонус',
              'body':'% бонуса зависит от закупленного товара. Каждый товар имеет свой % бонуса'
            }
          })
        elif p['plan']==5:
          table_headers.append({
            'h':'Начисления<br> по бонусу',
            'tooltip':{
              'header':'Бонус',
              'body':'сумма бонуса зависит от закупленного товара. Каждый товар имеет свой бонус в рублях'
            }
          })


      table_data=[]
      #form.pre({'p':})
      for g in p['child']:
        table_tr=[]
        table_tr.append(g['code']) # код
        table_tr.append(g['header']) # наименование
        if form.ov['subscribed_on_action'] or form.manager['type']==1: # витрина
          table_tr.append(g['showcase'])

        if g['price']==0 or g['price']=='0':
          table_tr.append('закупочная цена')
        else:
          table_tr.append(g['price'])

        if show_percent and (form.manager['type']==1 or (not p['reward_percent'] and form.ov['subscribed_on_action'])):
          if p['plan'] in (1,2,4):
            table_tr.append(g['percent'])
          elif p['plan']==5:
            table_tr.append(g['summa'])

        table_data.append(table_tr)
      
      


      # проверяем, есть ли прогнозный бонус для данного юрлица
      #form.pre({'exists_prognoz_bonus':exists_prognoz_bonus(form,p['id'])})
      header_data_item=p['header']+' ('+p['begin_date']+'..'+p['end_date']+') '
      pb_links=[]
      header_links=[]

      if set1 and exists_prognoz_bonus(form,p['id'],cur_period):
        # !!!!!
        header_links.append({
          'url':f"/edit_form/action_plan/{p['id']}",
          'header':'прогнозный бонус (текуший)',
          'style':'color: red;'
        })
      #form.pre(form.manager)

      if set1 and (cur_period['querter_begin_days']<=14 or form.manager['show_old_plans']) and exists_prognoz_bonus(form,p['id'],prev_period):
        
        header_links.append({
          'url':f"/edit_form/action_plan/{p['id']}?prev=1",
          'header':f'прогнозный бонус ({prev_period["querter"]} квартал {prev_period["year"]})',
          'style':'color: red;'
        })
        #  +=f'''<a href="" target="blank" style="color: red;">прогнозный бонус (тек)</a>'''
        #header_data_item+=f'''<a href="/edit_form/action_plan/{p['id']}" target="blank">прогнозный бонус (предыдущий квартал)</a>'''
      # с предыдущим периодом также....

      data_item={
        'header':header_data_item,
        'content':[],
        'header_links':header_links
      }

      if len(pb_links):
        data_item['content'].append({
            'type':'html',
            'body':f'''<p>{' | '.join(pb_links)}</p>'''
        })
      
      if form.manager['type']==1 or form.ov['subscribed_on_action']:
        body=f'''План: {p['plan_label']}<br>'''
        
        if p['plan'] in (1,2):
          body+=f'''{p['value_name']}: {p['value']} <small>в квартал на одну аптеку</small><br>'''

        elif p['plan'] != 3:
          body+=f'''{p['value_name']}: {p['value']}<br>'''

        if p['reward_percent']:
          body+=f'бонус: {p["reward_percent"]}%<br>'

        #backend_url='http://dev-crm.test/backend'
        backend_url='/backend'
        body+=f'''<div class="download_block">
          <a href="{backend_url}/anna/download/action_plan/xls/{p['id']}" target="_blank">скачать в xls</a>
           |  <a href="{backend_url}/anna/download/action_plan/dbf/{p['id']}"  target="_blank">скачать в dbf</a>
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
    field['before_html']=''
    if len(table_data):
      field['before_html']+='<h2 style="margin-top: 20px;">Группы товаров</h2>'
    else:
      field['before_html']+='<p style="margin-top: 20px; color: red;">Группы товаров отсутствуют</p>'


    #form.javascript['edit_form']+=form.template('./conf/action/templates/good_categories.js')
def exists_prognoz_bonus(form,action_plan_id,period):
  need=False
  
  if not period['id']: # Если не удалось найти период -- не выводим
    return need

  if form.script=='edit_form' and form.action=='edit' and form.ov:
    if form.manager['type']==2: # юридическое лицо
      if len(form.manager['ur_lico_ids']):

        return form.db.query(
          query=f'''
            select
              count(*)
            from
              prognoz_bonus
            where
              action_id=%s and action_plan_id=%s and ur_lico_id in ({','.join(form.manager['ur_lico_ids'])})
              and period_id=%s
          ''',
          values=[form.ov['id'],action_plan_id,period['id']],
          onevalue=1
        )
    elif form.manager['type']==3: # аптека
      if len(form.manager['apt_list_ids']):

        return form.db.query(
          query=f'''
            select
              count(*)
            from
              prognoz_bonus_apteka
            where
              action_id=%s and action_plan_id=%s and apteka_id in ({','.join(form.manager['apt_list_ids'])})
              and period_id=%s
          ''',
          values=[form.ov['id'],action_plan_id, period['id']],
          onevalue=1
        )
