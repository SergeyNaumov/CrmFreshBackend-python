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



  


    

def date_stop_before_code(form,field):
  print()
 