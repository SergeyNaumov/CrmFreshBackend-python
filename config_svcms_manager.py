import re
from lib.svcmsmanager.cache_pages import clear_cache_for_domain
from configs.svcmsmanager.config_wysiwyg import config_wysiwyg
from configs.svcmsmanager.gptassist_rules import gptassist_rules


  

  
  


# 


config={
  'BaseUrl':'/manager',
  'title':'CMS Digitalstrateg',
  'BaсkendBase':'http://digitalstrateg.test/backend',
  'config_folder':'configs/svcmsmanager',
  # Разрешённые Origin'ы для CORSMiddleware (см. main.py).
  # Локальная петля (localhost/127.0.0.1 на любом порту) разрешена всегда
  # через dev_origin_regex, отдельно перечислять её не нужно.
  'cors_origins':[
    'http://digitalstrateg.test',
  ],
  'copyright':'copyright 2005 - {{cur_year}}',
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  #'encrypt_method':'mysql_sha2',
  'encrypt_method':'encrypt',
  'use_project':False,
  'cookie':{
    # В dev фронт ходит на бэк кросс-доменно (127.0.0.1:8081 -> localhost:5000).
    # Chrome не отправляет SameSite=Lax cookie в кросс-сайтном XHR, поэтому нужен
    # SameSite=None, а он требует Secure. Если деплой идёт по обычному http --
    # вернуть samesite='lax', secure=False.
    'path':'/',
    'samesite':'none',
    'secure':True,
    'httponly':True,
  },
  'auth':{
    # Таблица авторизации:
    'manager_table':'manager',
    'manager_table_id':'manager_id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    'encrypt_method':'mysql_encrypt',
    
    # b2bb2bconnect / 123
    # UPDATE manager password=sha2('123',256) where login='b2bb2bconnect';
    # Сессия:
    'session_table':'manager_session',
    'session_fails_table':'manager_session_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
    'use_roles':False,
    'use_permissions':False
    
  },
  'gptassist_rules':gptassist_rules, # функция,
  'messenger_rules':{}, # отсутствует для  svcms manager
  'telegram':{},
  # Перенёс вниз
  #'after_create_engine':after_create_engine,
  #'after_read_form_config':after_read_form_config, # Вызывается после чтения конфига от CRM
  #'after_all_change_action':  alter_all_change_action,
  'system_email':'svcomplex@gmail.com',
  'system_url':'https://digitalstrateg.ru/',
  'connects':{
    'crm_read':{
      'user':'svcms',
      'password':'',
      'host':'localhost',
      'dbname':'svcms',
    },
    'crm_write':{
      'user':'svcms',
      'password':'',
      'host':'localhost',
      'dbname':'svcms',
    },
  },
  'stat_log':0, # Записываем статистику посещений
  'controllers':{
    
    'left_menu':'/svcms/left-menu'
  },
  #'docpack':{
  #  'user_table':'user',
  #  'docpack_foreign_key':'user_id'
  #},
  'const':{
    'project_id':''
  },
  'events':[
    'quiz'
  ],

  'login':{
    'register':False, # возможность регистрации
    'remember':False, # возможность напоминания пароля
    
    # Доступно без авторизации
    'not_login_access': [
        '/gpt-assist/daemon-result',
        '/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password'
    ]
  },
  'wysiwyg':config_wysiwyg,
  'debug':{ # для отладки
    'manager_host':'demo2.digitalstrateg.ru',
    'hosts':['sv-home'],
    'manager_id': 5520, # Менеджер, под которым логинимся в том случае, если мы работаем в режиме дебага  
  }
}


async def after_create_engine(s,request,errors=[]):
  manager = request.state.manager
  if not(manager) or not manager['login']:
    return
  host=s.env['host']
  debug = config.get('debug')
  if host=='dev-crm.test' and 'manager_host' in debug:
    host=debug['manager_host']

  #print('HOST: ',s.env['host'])

  d=host.split('.')
  if d[0]=='www':
    host='.'.join(d[1:])
  
  s.manager=await s.db.query(
    query='select manager_id id,full_access,login from manager where manager_id=%s',
    values=[manager['id']],
    onerow=1
  )

  manager['host']=host
  
  request.state.manager=manager
  
  project=await s.db.query(
    query='''
      select
        d.project_id,d.template_id, if(mpa.id is null,0,1) access_for_cur_domain
      from
        domain d
        LEFT JOIN manager_project_access mpa ON d.project_id=mpa.project_id and mpa.manager_id=%s
      where d.domain=%s limit 1
    ''',
    errors=s.errors,
    debug=1,
    values=[manager['id'],host],
    onerow=1
  )
  
  if not(project):
    s.errors.append(f'Не найден проект, привязанный к {host}')
    return 
  elif not(project['access_for_cur_domain']) and not(manager['full_access']):
    s.errors.append(f'У Вас нет доступа для администрирования сайта {host}')

  request.state.project=project

def after_read_form_config(s,request,form):
  manager=request.state.manager
  project=request.state.project
  project_id=project['project_id']
  if len(form.s.errors):
    form.errors=form.s.errors

  form.manager=manager
  form.manager['files_dir']=f'./files/project_{project_id}'
  form.manager['files_dir_web']=f'/files/project_{project_id}'
  form.s=s
  form.project=request.state.project

def alter_all_change_action(form):
  # Это нужно для сброса кэша у клиентских сайтов
  manager=form.request.state.manager
  host=manager['host']
  print('Alter_all_change_action: ',host)
  clear_cache_for_domain(host)

config['after_create_engine']=after_create_engine
config['after_read_form_config']=after_read_form_config
config['alter_all_change_action']=alter_all_change_action
