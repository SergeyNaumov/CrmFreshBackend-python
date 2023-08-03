



def get_fields():
    return [ 
    {
      'description':'Дата и время отправки',
      'name':'registered',
      'type':'datetime',
      'filter_on':1
    },
    {
      'description':'Логин учётной записи',
      'name':'login',
      'type':'filter_extend_select_from_table',
      'table':'manager',
      'tablename':'m',
      'header_field':'login',
      'value_field':'id',
      'filter_code':login_filter_code,
      'filter_on':1
    },
    # {
    #   'description':'Тип отправителя',
    #   'name':'type',
    #   'type':'filter_extend_select_values',
    #   'tablename':'m',
    #   'values':[
    #     {'v':1, 'd':'Сотрудник АннА'},
    #     {'v':2, 'd':'Представитель юридического лица'},
    #     {'v':3, 'd':'Представитель аптеки'},
    #     {'v':4, 'd':'Фармацевт'},
    #   ]
    # },
    {
      'description':'ФИО',
      'name':'name',
      'type':'textarea',
      'tablename':'m',
      'filter_on':True,
      'filter_on':1
    },
    {
      'description':'Вопрос',
      'name':'question',
      'type':'textarea',
      'filter_on':1
    },

]

def login_filter_code(form,field,row):
  t=row['m__type']
  manager_type=''
  if t==1:
    manager_type='Менеджер АннА'
  
  if t==2:
    #form.pre(row)
    manager_type=f"Представитель юридического лица<br>{row['ul__header']}"
  
  if t==3:
    manager_type=f"Представитель аптеки<br>{row['apt__ur_address']}<br>{row['ul_apt__header']}"
  
  if t==4:
    manager_type=f"Фармацевт<br>{row['pharm_apt__ur_address']}<br>{row['pharm_ul__header']}"

  return f"{row['m__login']}<br>\n<small>{row['m__name']}</small>,<br><small>{manager_type}</small>"