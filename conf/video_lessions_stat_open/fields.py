



def get_fields():
    return [ 
    {
      'name':'ts',
      'description':'Дата события',
      'type':'date',
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
      'description':'Наименование видео',
      'name':'text',
      'type':'filter_extend_text',
      'db_name':'header',
      'tablename':'v',
      'filter_on':1
    },
    {
      'description':'Длительность просмотра видео, сек',
      'name':'sec_opened',
      'type':'text',
      'filter_type':'range',
      'filter_on':1
    }
]

def login_filter_code(form,field,row):
  t=row['m__type']
  manager_type=''
  if t==1:
    manager_type='Менеджер АннА'
  
  if t==2:
    manager_type='Представитель юридического лица'
  
  if t==3:
    manager_type='Представитель аптеки'
  
  if t==4:
    manager_type='Фармацевт'

  return f"{row['m__login']}<br>\n<small>{row['m__name']}</small>\n<small>{manager_type}</small>"