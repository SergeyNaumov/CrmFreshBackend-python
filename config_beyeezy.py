import re
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
  form.manager['files_dir_web']=f'/files/'

  

# Будет выполняться для каждой операции insert / delete / update в crm
def alter_all_change_action(form):
  pass

config={
  'BaseUrl':'',
  #'config_folder':'confBeyeezy', # точки нельзя
  'config_folder':'configs/beyeezy',
  'title':'CRM Beyeezy',
  'copyright':'copyright 2005 - {{cur_year}}',
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  #'encrypt_method':'mysql_sha2',
  #'encrypt_method':'encrypt',
  'use_project':False,
  'auth':{
    # Таблица авторизации:
    'manager_table':'manager',
    'manager_table_id':'id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    'encrypt_method':'mysql_encrypt',
    
    # b2bb2bconnect / 123
    # UPDATE manager password=sha2('123',256) where login='b2bb2bconnect';
    # Сессия:
    'session_table':'session',
    'session_fails_table':'session_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
    'use_roles':False,
    'use_permissions':True
    
  },
  'mail':{ # Откуда отправляем почту
    'default_from_addr':'crm@bzinfo.pro',
    'server':'email.t-pass.pro',
    'port': 587,
    'user':'crm@bzinfo.pro',
    'password':'%,52,riantInGstARdeBric'
  },
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config, # Вызывается после чтения конфига от CRM
  #'after_all_change_action':alter_all_change_action,
  'system_email':'noname@gmail.com',
  'system_url':'https://beyeezy.crm-dev.ru/',
  'connects':{
    'crm_read':{
      'user':'beyeezy',
      'password':'',
      'host':'localhost',
      'dbname':'beyeezy',
    },
    'crm_write':{
      'user':'beyeezy',
      'password':'',
      'host':'localhost',
      'dbname':'beyeezy',
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

  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id':1,
  }
}
