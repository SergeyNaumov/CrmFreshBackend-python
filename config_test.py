import re
import configs.test.messenger_rules as messenger_rules
#print('messenger_rules:',messenger_rules.init)
config_folder='configs/test'



#from lib.cache_pages import clear_cache_for_domain

#from lib.session import get_permissions_for
def after_create_engine(s,errors=[]):
  pass
  
  


# 
def after_read_form_config(form):

  
  if len(form.s.errors):
    form.errors=form.s.errors
  
  form.manager=form.s.manager
  form.manager['files_dir']='./files'
  form.manager['files_dir_web']='/files'
  
  #manager_login=form.s.manager['id']
  #form.manager=get_permissions_for(form,manager_login)
  # form.manager['files_dir']=f'./files/project_{form.s.project_id}'
  # form.manager['files_dir_web']=f'/files/project_{form.s.project_id}'

# Будет выполняться для каждой операции insert / delete / update в crm
def alter_all_change_action(form):
  pass

config={
  'messenger_rules':{
    'init': messenger_rules.init,
    'get_socket_name': messenger_rules.get_socket_name

  },
  'BaseUrl':'https://test.crm-dev.ru/',
  'system_email':'noname@gmail.com',
  'system_url':'https://test.crm-dev.ru/',
  # Разрешённые Origin'ы для CORSMiddleware (см. main.py).
  # Локальная петля (localhost/127.0.0.1 на любом порту) разрешена всегда
  # через dev_origin_regex, отдельно перечислять её не нужно.
  'cors_origins':[
    'https://test.crm-dev.ru',
    'http://dev-crm.test',
  ],
  'BakendBase':'http://dev-crm.test/backend',
  #'config_folder':'confFas',
  'config_folder':config_folder,
  'title':'CRM Fas',
  'app_components':{ # Компоненты веб-приложения
    'messenger':{

    }
  },
  'main_page_components':[
    #{'component':'birth-days','cols':12},
    #{'component':'notifications','cols':12},
    #{'component':'manager-load','cols':12},
  ],
  'copyright':'copyright 2005 - {{cur_year}}',
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  #'encrypt_method':'mysql_sha2',
  #'encrypt_method':'encrypt',
  'use_project':False,
  'cookie':{
    # В dev фронт ходит на бэк кросс-доменно (127.0.0.1:8081 -> localhost:5000).
    # Chrome не отправляет SameSite=Lax cookie в кросс-сайтном XHR, поэтому для
    # кросс-доменной авторизации нужен SameSite=None. Chrome требует, чтобы
    # SameSite=None шёл вместе с Secure, поэтому secure=True обязателен.
    # Secure-cookie Chrome принимает на http://localhost и http://127.0.0.1
    # (это "trustworthy origins"), но НЕ примет на http://<LAN-IP>.
    # Если деплой идёт по обычному http -- вернуть samesite='lax', secure=False.
    'path':'/',
    'samesite':'none',
    'secure':True,
    'httponly':True,
  },


  'auth':{
    # Таблица авторизации:
    'manager_table':'manager',
    'manager_table_id':'id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    'encrypt_method':'mysql_encrypt',
    
    # Сессия:
    'session_table':'session',
    'session_fails_table':'session_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
    'use_roles':True,
    'use_permissions':True,
    'out_manager_card_link':True, # выводить ссылку на карточку в шапке
    
  },
  'mail':{ # Откуда отправляем почту
    'default_from_addr':'',
    'server':'',
    'port': 587,
    'user':'',
    'password':''
  },
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config, # Вызывается после чтения конфига от CRM
  #'after_all_change_action':alter_all_change_action,

  'connects':{
    'crm_read':{
      'user':'crm',
      'password':'',
      'host':'localhost',
      'dbname':'crm',
    },
    'crm_write':{
      'user':'crm',
      'password':'',
      'host':'localhost',
      'dbname':'crm',
    },
  },
  'stat_log':0, # Записываем статистику посещений
  'controllers':{
    
    #'left_menu':'/fas/left-menu'
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
        '/login','/test/mailsend',
        #'/register',
        '/remember/get-access-code',
        '/remember/check-access-code',
        '/remember/change-password'
    ]
  },
  'telegram':{
    # fas car dev bot
    'bot_name':'<имя_бота>',
    'bot_token':'<токен_бота>'
  },
  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id':
#      12066 # mai
      1
      #11709
      #11691 #Люб
      #4201 # sed
      #585 # Ак ,
      #7576 #pzm
      #11709
    
    #'manager_id':12039 # О ,
    #'manager_id': 11691 # Г
  }
}
