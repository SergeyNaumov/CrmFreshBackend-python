# UPDATE manager set password=sha2('123',256);
import re
import os

PRODUCTION = os.environ.get('PRODUCTION')

def after_create_engine(s,errors=[]):
  ...
def after_read_form_config(form):
  if len(form.s.errors):
    form.errors=form.s.errors
  
  form.manager=form.s.manager
  form.manager['files_dir']=f'./files/project_{form.s.shop_id}'
  form.manager['files_dir_web']=f'/files/project_{form.s.shop_id}'

# def alter_all_change_action(form):
#   # Это нужно для сброса кэша у клиентских сайтов
#   host=form.s.manager['host']
#   print('Alter_all_change_action: ',host)
#   clear_cache_for_domain(host)

config={
  'title':'Crm Fresh',
  'copyright':'copyright 2004 - {{cur_year}}',
   'bottom_menu': [
      {'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  'encrypt_method':'mysql_sha2',
  'use_project':False,
  'auth':{
    # Таблица авторизации:
    'manager_table':'manager',
    'manager_table_id':'id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    #'encrypt_method':'mysql_encrypt',
    'encrypt_method':'mysql_sha2',
    # b2bb2bconnect / 123
    # UPDATE manager password=sha2('123',256) where login='b2bb2bconnect';
    # Сессия:
    'session_table':'session_owner',
    'session_fails_table':'session_owner_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
    'use_permissions':False,
    'use_roles':True,
  },
  'startpage':{ # указываем, какой компонент будет загружаться на главной странице
    'type':'src',
    'value':'/mainpage.html',
  },
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config,
  'system_email':'svcomplex@gmail.com',
  'system_url':'https://adminbot.assist-ant.su/',
  
  #'stat_log':1, # Записываем статистику посещений
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
  'controllers':{
    'left_menu':'/assist-ant/left-menu'
  },

  'docpack':{
    'user_table':'user',
    'docpack_foreign_key':'user_id'
  },
  'const':{
    'project_id':''
  },
  'events':[
    'quiz'
  ],
  'telegram':{
    # требует заполнения
    'bot_name':'',
    'bot_token':''
  },
  'vk':{
    # требует заполнения
    'bot_token': '' # vk token
  },
  'max':{
    # требует заполнения
    'bot_link':'', 
    'bot_id':'',
    'bot_token':''
  },
  'login':{
    'register':False, # возможность регистрации
    'remember':True, # возможность напоминания пароля
    
    # Доступно без авторизации
    'not_login_access': [
        '/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password'
    ]
  },
  # 8Xiddqdidkfa#762x
  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id':1,
  },


}
