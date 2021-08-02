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
  plan_data=''
  #form.pre(ov)
  if ov['plan']==1:
    plan_data+=f'План: Cуммовой<br>Сумма от: {ov["value"]}<br>'
    if ov["reward_percent"]:
      plan_data+=f'Бонус: {ov["reward_percent"]}%<br>'

  elif ov['plan']==2:
    plan_data+=f'План: колличественный<br>Кол-во: {ov["value"]}<br>'
    if ov["reward_percent"]:
      plan_data+=f'Бонус: {ov["reward_percent"]}%<br>'
  elif ov['plan']==3:
    #form.pre(ov)
    plan_data+=f'План: только % за любые закупки<br>Бонус: {ov["reward_percent"]}%<br>'

  
  period=form.ov['period']
  different_percentage=''
  
  if ov['goods_cnt_percent']>1: # в случае, когда 
    different_percentage='<div style="color: red;">% бонуса зависит от закупленного товара. Каждый товар имеет свой % бонуса</div>'


  field['after_html']=f'''
    <div style='margin-bottom: 20px;'>
      <h3>Информация о плане за {period['querter']} квартал {period['year']} </h3>
      {plan_data}
      {different_percentage}
      <p style="color: red;">данные обновляются с задержкой 1-2 дня</p>
    </div>
  '''