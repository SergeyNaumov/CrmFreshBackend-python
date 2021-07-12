from lib.engine import s


#from lib.core import exists_arg, date_to_rus
#from .header_before_code import header_before_code
#from .good_categories import good_categories
#from .good_categories2 import good_categories2 
from .pr_bonus import pr_bonus
from .pr_bonus_apt import pr_bonus_apt

def get_fields():
    return [ 
    {
      'description':'Информация о плане',
      'name':'plan_info',
      'type':'code',
      'code':plan_info
    },
    {
      'name':'header',
      'description':'Данные по прогнозному бонусу',
      'type':'code',
      'code':pr_bonus,
      'read_only':1,
      'filter_on':1,
      #'tab':'main',
    },
    {
      'name':'header_apt',
      'description':'Данные по прогнозному бонусу для аптек',
      'type':'code',
      'code':pr_bonus_apt,
      'read_only':1,
      'filter_on':1,
      #'tab':'main',
    },
    
]

def plan_info(form,field):
  ov=form.ov
  plan_name=''
  value_name=''

  if ov['plan']==1:
    plan_name='Суммовой'
    value_name='Сумма от'

  elif ov['plan']==2:
    plan_name='Колличественный'
    value_name='Кол-во'

  elif ov['plan']==3:
    plan_name='Только % за любые закупки'
    value_name='Выплачиваемый процент'
  
  period=form.ov['period']

  field['after_html']=f'''
    <div style='margin-bottom: 20px;'>
      <h3>Информация о плане за {period['querter']} квартал {period['year']} </h3>
      План: { plan_name }<br>
      {value_name}: {ov['value']}
      <p style="color: red;">данные обновляются с задержкой 1-2 дня</p>
    </div>
  '''