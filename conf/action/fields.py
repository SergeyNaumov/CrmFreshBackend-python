from lib.engine import s
from lib.core import exists_arg

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
      'filter_on':1,
      'filter_code':date_start_filter_code
    }, 
    {
      'name':'date_stop',
      'description':'Окончание подписки',
      'type':'date',
      'default_off':1,
      'tab':'main',
      'filter_code':date_stop_filter_code, # в результатах поиска это поле превращается в подписку
      'filter_on':1
    },
    # {
    #   'name':'good_categories',
    #   'description':'Группы товаров',
    #   'type':'accordion',
    #   'tab':'goods',
    #   # Запрос для вывода заголовках аккордиона
    #   'headers_query':'SELECT id,header from action_plan where action_id=<id>',
      
    # },
    {
      'name':'good_categories',
      'type':'code',
      'tab':'goods',
      'description':'категории товаров',
      'code':good_categories
    },
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

def date_start_filter_code(form,field,row):
  return f"{row['wt__date_start']} - {row['wt__date_stop']}"

def date_stop_filter_code(form,field,row):

  if str(form.manager['type'])=='2': # Юридическое лицо
    #form.pre(row)
    # получаем списки подписанных и отправивших запрос на акцию юрлиц
    if not exists_arg('subscribed_ur_lico_id',row): row['subscribed_ur_lico_id']=''
    if not exists_arg('requested_ur_lico_id',row): row['requested_ur_lico_id']=''
    row['subscribed_ur_lico_id']=row['subscribed_ur_lico_id'].split('|')
    row['requested_ur_lico_id']=row['requested_ur_lico_id'].split('|')

    #ur_lico_subscribe='[{"id":"1","name":"ЗАО лекарствснаб","v":"0"},{"id":"2","name":"ФЕРЕЙН","v":"1"},{"id":"3","name":"ООО Ихтиандр","v":"2"}]'
    ur_lico_subscribe=[]
    
    for u in form.manager['ur_lico_list']:
      v=0
      if str(u['id']) in row['subscribed_ur_lico_id']: v=2 # подписанных
      elif str(u['id']) in row['requested_ur_lico_id']: v=1 # отправил запрос на подписку
      else: v=0
      ur_lico_subscribe.append({'id':u['id'],'v':str(v),'name':u['name']})

    # Количество подписанных аптек
    apteka_subscribe=0
    ur_lico_subscribe=s.to_json(ur_lico_subscribe)
    
    if (row['apteka_id_list']):
      apteka_subscribe=len(row['apteka_id_list'].split('|'))
    return f'<div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{ur_lico_subscribe}|{apteka_subscribe}</div>'


  elif str(form.manager['type'])=='3': # Аптека
    # subscribe_status: 0 - не подписна ; 1 - отправлен запрос на участие ; 2- подписана
    if not exists_arg('subscribed_apteka_id',row): row['subscribed_apteka_id']=''
    row['subscribed_apteka_id']=row['subscribed_apteka_id'].split('|')
    if not exists_arg('requested_apteka_id',row): row['requested_apteka_id']=''
    row['requested_apteka_id']=row['requested_apteka_id'].split('|')

    apteka_subscribe=[]

    for a in form.manager['apteka_list']:
      v=0
      if str(a['id']) in row['subscribed_apteka_id']: v=2
      if str(a['id']) in row['requested_apteka_id']: v=1
      apteka_subscribe.append({'id':a['id'],'v':str(v),'name':a['name']})
    apteka_subscribe=s.to_json(apteka_subscribe)

    return f'<div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{apteka_subscribe}</div>'

    form.pre(apteka_subscribe)

    #form.pre(row)
    subscribe_status=0
    return subscribe_status
    # else:
  return ''

  

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

def date_stop_before_code(form,field):
  print()
  #form.pre({'script':form.script})