from lib.engine import s
import importlib,os
import json

# def get_product_options():
#   options=s.db.query(
#     query='''
#       select options from project where project_id=%s
#     ''',
#     values=[s.manager['project_id']],
#     onevalue=1
#   )
#   options_on={}
#   if options:
    
#     for o in options.replace(';;',';').split(';'):
#       if o: options_on[o]=True
#   return options_on



def left_menu():
  errors=[]
  manager=None
  manager_menu_table=None
  #print('manager',s.manager,s.project)

    
  #s.pre('5555')  

  left_menu=[
    {
      'header':'Главная',
      'value':'mainpage',
      'type':'vue',
      'child':[],
      'icon':'fa fa-arrow-right',
      
    },
    {
      'header':'Перейти на сайт',
      'value':f'http://{s.manager["host"]}',
      'type':'newtab',
      'child':[],
      'icon':'fa fa-arrow-right',
    },
    # {
    #   'header':'Руководство пользователя',
    #   'value':'https://help.design-b2b.com/',
    #   'type':'newtab',
    #   'child':[],
    #   'icon':'fa fa-arrow-right',

    # },
    #standart_service,
    #extended_service
  ]
  path_to_menu=f'./conf_projects/project_{s.project_id}/left_menu.py'
  if os.path.isfile(path_to_menu): # Загружаем меню из файла
    #return {'file':'exists'}
    try:
      module_path=f'conf_projects.project_{s.project_id}.left_menu'
      module=importlib.import_module(module_path)
      _list=module.left_menu
      for m in _list:
        left_menu.append(m)
    except SyntaxError as e:
      errors.append(f'Ошибка синтаксиса в {path_to_menu}')
  else: # Формируем на основании БД
      left_menu.append(get_standart_service(errors))
      left_menu.append(get_extended_service(errors))
    

  manager=s.db.query(
    query='select manager_id id,login from manager where login=%s',
    values=[s.login],
    onerow=1,
  )


  return {
    'left_menu':left_menu,

    'manager':manager,
    'errors':errors,
    'success': not len(errors),
  }
  
# Получение стандартных сервисов
def get_standart_service(errors): # Получение стандартных сервисов
  standart_service={
      'header':'Стандартные сервисы',
      'value':'https://help.design-b2b.com/',
      'icon':'fa fa-sitemap',
      'type':'src',
      'child':[],
  }
  #print("srv: ",serv_list)
  serv_list=s.db.query(
      query='''
        SELECT
          header,link,json
        FROM
          struct_public sp, project_struct_public psp
        WHERE sp.struct_public_id=psp.struct_public_id and psp.project_id=%s
       ''',
       errors=errors,
       values=[s.project_id]
  )

  for srv in serv_list:
    try:
      data = json.loads(srv['json'])
      standart_service['child'].append(data)
    except ValueError as e:
      errors.append([f"При чтении struct_public: routes/svcms/left_menu.py: {srv['header']} - ошибка парсинга JSON {e}"])

  return standart_service




# Получение расширенных сервисов
def get_extended_service(errors):
    extended_service={
      'header':'Расширенные сервисы',
      'value':'https://help.design-b2b.com/',
      'icon':'fas fa-star',
      'type':'src',
      'child':[
        # {
        #   'header':'Руководство пользователя',
        #   'value':'https://help.design-b2b.com/',
        #   'type':'src',
        #   'child':[],
        # }
      ],
    }
    #print('GET_EXTENDED')
    serv_list=s.db.query(
      query='select header,json from project_menu where project_id=%s order by sort',
      values=[s.project_id],
      errors=errors,
    )
    for srv in serv_list:
      try:
        data = json.loads(srv['json'])
        extended_service['child'].append(data)
      except ValueError as e:
        errors.append([f"При чтении project_menu (get_extended_service): routes/svcms/left_menu.py: {srv['header']} - ошибка парсинга JSON {e}"])
    #print('serv_list:',serv_list)
    return extended_service
