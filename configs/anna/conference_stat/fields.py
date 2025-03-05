



def get_fields():
    return [ 
    {
      'description':'Время перехода',
      'name':'ts',
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
    {
      'description':'Конференция',
      'name':'header',
      'type':'filter_extend_text',
      'db_name':'header',
      'tablename':'c',
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