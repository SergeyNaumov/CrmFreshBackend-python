import re
#from lib.cache_pages import clear_cache_for_domain


def after_create_engine(s,errors=[]):
  pass


# для отладки


def after_read_form_config(form):
  if len(form.s.errors):
    form.errors=form.s.errors

  form.manager=form.s.manager
  form.manager['files_dir']='./files'
  form.manager['files_dir_web']=f'/files/'

# Будет выполняться для каждой операции insert / delete / update в crm
def alter_all_change_action(form):
  pass

manager_id=1

config={
  'BaseUrl':'/manager',
  'system_email':'svcomplex@gmail.com',
  'system_url':'https://crimea.assist-ant.su/manager/',
  'BakendBase':'http://dev-crm.test/backend',
  'config_folder':'configs/crimea',
  'title':'CMS Crymea',
  'copyright':'copyright 2023 - {{cur_year}}',
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
    'encrypt_method':'mysql_sha2',

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
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config, # Вызывается после чтения конфига от CRM
  #'after_all_change_action':alter_all_change_action,

  'connects':{
    'crm_read':{
      'user':'crimea',
      'password':'',
      'host':'localhost',
      'dbname':'crimea',
    },
    'crm_write':{
      'user':'crimea',
      'password':'',
      'host':'localhost',
      'dbname':'crimea',
    },
  },
  'stat_log':0, # Записываем статистику посещений
  'controllers':{

    'left_menu':'/left-menu'
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
        '/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password'
    ]
  },

  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id': manager_id

  }
}
