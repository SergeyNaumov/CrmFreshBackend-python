from lib.engine import s
from lib.core import exists_arg, date_to_rus
from .header_before_code import header_before_code
from .good_categories import good_categories 
#from .pr_bonus import pr_bonus
from .subscribes import subscribes
def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Название',
      'type':'text',
      #'filter_code':header_filter_code,
      'read_only':1,
      'filter_on':1,
      'tab':'main',
      # При выводе фильтров и при поиска превращаем данное текстовое поле в autocomplete
      'before_code':header_before_code
    },
    {
        'name':'date_subscribe',
        'description':'Даты подписки',
        'type':'yearmon',
        'filter_on':1,
        'filter_type':'range',
        'not_process':1,
        'filter_code':date_subscribe_filter_code
    },

    # {
    #     'name':'date_start',
    #     'description':'Начало подписки',
    #     'type':'yearmon',
    #     'filter_on':1,
    #     'filter_type':'eq',
    #     'not_process':1,
    #     'filter_code':date_start_filter_code
    # },
    # {
    #   'name':'date_stop',
    #   'description':'Окончание подписки',
    #   'type':'yearmon',
    #   'filter_type':'eq',
    #   'not_process':1,
    #   'tab':'main',
    #   'filter_code':date_stop_filter_code, # в результатах поиска это поле превращается в подписку
    #   'filter_on':1
    # },

    {
      'name':'subscribes',
      'type':'code',
      'tab':'goods',
      'description':'Подписки',

      'code':subscribes
    },
    {
      'name':'good_categories2',
      'type':'code',
      'tab':'goods',
      'description':'категории товаров',
      'code':good_categories,
      'data':[]
      # 'data':[
      #   {
      #     'header':'Заголовок1',
      #     'content':[
      #       {'type':'html','body':'<p>Это абзац</p>'},
      #       {'type':'html','body':'<p>Это второй абзац</p>'},
      #       {
      #         'type':'table',
      #         'table':{
      #           'headers':[
      #             {
      #               'h':'столбец1',
      #               'tooltip':{
      #                 'header':'Заголовок для подсказки',
      #                 'body':'подсказка'
      #               }
      #             },
      #             {'h':'столбец2'},
      #             {'h':'столбец3'}
      #           ],
      #           'data':[
      #             ['Иванов','1','i2'],
      #             ['Абрамович','8','d6'],
      #             ['Яшин','800','9'],
      #             ['Петров','136','9'],
      #             ['Сидоров','518','d6'],
      #           ]
      #         }
      #       }
      #     ]
      #   },
        
      #   {
      #     'header':'Заголовок2',
      #     'content':[

      #     ]
      #   },
        
      # ]
    },
    # {
    #   'name':'prognoz_bonus',
    #   'type':'code',
    #   'tab':'pr_bonus',
    #   'description':'Информация о бонусах',
    #   'code':pr_bonus,
    #   'data':[]
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
    #form.pre(form.manager)
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
    if len(suppliers_lst):
      field['after_html']='<br>'.join(suppliers_lst)
    else:
      field['after_html']=f'<p>В расчет принимаются закупки от всех дистрибьюторов</p>'
  
  

#def date_subscribe_filter_code(form,field,row):
#  return f"{date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop']) }"

#def date_start_filter_code(form,field,row):
#  return f"{date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop']) }"

def date_subscribe_filter_code(form,field,row):
  



  if str(form.manager['type'])=='2': # Юридическое лицо
    #form.pre(row)
    # получаем списки подписанных и отправивших запрос на акцию юрлиц
    if not exists_arg('subscribed_ur_lico_id',row): row['subscribed_ur_lico_id']=''
    if not exists_arg('subscribed_apteka_id',row): row['subscribed_apteka_id']=''

    if not exists_arg('requested_ur_lico_id',row): row['requested_ur_lico_id']=''
    
    row['subscribed_apteka_id']=row['subscribed_apteka_id'].split('|')
    row['subscribed_ur_lico_id']=row['subscribed_ur_lico_id'].split('|')
    row['requested_ur_lico_id']=row['requested_ur_lico_id'].split('|')
    #form.pre(row['subscribed_apteka_id'])
    #ur_lico_subscribe='[{"id":"1","name":"ЗАО лекарствснаб","v":"0"},{"id":"2","name":"ФЕРЕЙН","v":"1"},{"id":"3","name":"ООО Ихтиандр","v":"2"}]'
    ur_lico_subscribe=[]
    

    for u in form.manager['ur_lico_list']:
      
      need_append=False
      
      if not exists_arg('ur_lico_id',form.query_hash):
        need_append=True
      elif exists_arg('ur_lico_id',form.query_hash) and len(form.query_hash['ur_lico_id']):
        # В том случае, когда мы фильтруем по юрлицам -- выводим информацию о подписке только по тем юрлицам, по которым ищем
        if u['id'] in form.query_hash['ur_lico_id']:
          need_append=True
        else:
          need_append=False
      v=0
      if str(u['id']) in row['subscribed_ur_lico_id']: v=2 # подписанных
      elif str(u['id']) in row['requested_ur_lico_id']: v=1 # отправил запрос на подписку
      else: v=0
      
      if need_append:
        # u['apt_ids'] -- id-шники аптек для конкретного юрлица
        #form.pre({
        #  'u_apt_ids':u['apt_ids'],
        #  'subscribed_apteka_id':row['subscribed_apteka_id'],
        #  'cnt_apt':len(list(set(u['apt_ids']) & set(row['subscribed_apteka_id'])))
        #})
        ur_lico_subscribe.append({
          'id':u['id'],
          'action_id':row['wt__id'],
          'v':str(v),
          'name':u['name'],
          'apt_cnt':len(list(set(u['apt_ids']) & set(row['subscribed_apteka_id'])))
        })

    #form.pre(['subscribe',ur_lico_subscribe])
    # Количество подписанных аптек
    apteka_subscribe=0
    ur_lico_subscribe=s.to_json(ur_lico_subscribe)
    
    if (row['apteka_id_list']):
      apteka_subscribe=len(row['apteka_id_list'].split('|'))
    return f'''
      {date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop'])}
      <div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{ur_lico_subscribe}|{apteka_subscribe}</div>'''


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

    return f'''{date_to_rus(row['wt__date_start']) } - { date_to_rus(row['wt__date_stop'])}
      <div id="anna_subscr{row["wt__id"]}" class="subscibe_buttons">{apteka_subscribe}</div>'''

    #form.pre(apteka_subscribe)

    #form.pre(row)
    subscribe_status=0
    return subscribe_status
    # else:
  return ''

  


    

def date_stop_before_code(form,field):
  print()
  #form.pre({'script':form.script})