<<<<<<< HEAD
import re
#from lib.cache_pages import clear_cache_for_domain

#from lib.session import get_permissions_for
def after_create_engine(s,errors=[]):
  pass
  
  


# 
def after_read_form_config(form):

  
=======
# UPDATE manager set password=sha2('123',256);

def after_create_engine(s,errors=[]):
  if not(s.manager) or not s.manager['login']:
    return
  host=s.env['host']

  d=host.split('.')
  if d[0]=='www':
    host='.'.join(d[1:])
  
  shop=s.db.query(
    query=f'''
      SELECT
        o.*, s.id shop_id, s.domain, s.template_id
      FROM
        owner o
        join shop s ON s.owner_id=o.id
      WHERE o.id=%s and s.domain=%s
    ''',
    values=[s.manager['id'],host],
    onerow=1
  )
  s.manager['filedir_http']=''
  if shop:
    s.manager=shop
    s.shop_id=shop['shop_id']
    s.template_id=shop['template_id']
    s.manager['filedir_http']=f'/files/project_{s.shop_id}'
    
  else:
    s.errors.append(f'У Вас нет права для администрирования {host}')
    return 
#  s.manager['host']=host
  #print('MANAGER: ',s.manager)
#  print('s.manager:',s.manager)

  # shop=s.db.query(
  #   query='''
  #     select
  #       s.id,s.template_id
  #     from
  #       shop s
        
  #     where s.id=%s and domain=%s limit 1
  #   ''',
  #   errors=s.errors,
  #   debug=1,
  #   values=[s.manager['shop_id'],host],
  #   onerow=1
  # )
  

  # elif not(shop['access_for_cur_domain']) and not(s.manager['full_access']):
  #   s.errors.append(f'У Вас нет доступа для администрирования сайта {host}')



  #print("project_id:",project_id)
  #print('MANAGER:',s.manager)
  #s.errors=[f'Домен {host} не найден в базе данных! Доступ запрещён']
def after_read_form_config(form):
>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
  if len(form.s.errors):
    form.errors=form.s.errors
  
  form.manager=form.s.manager
<<<<<<< HEAD
  #manager_login=form.s.manager['id']
  #form.manager=get_permissions_for(form,manager_login)
  # form.manager['files_dir']=f'./files/project_{form.s.project_id}'
  # form.manager['files_dir_web']=f'/files/project_{form.s.project_id}'

# Будет выполняться для каждой операции insert / delete / update в crm
def alter_all_change_action(form):
  pass

config={
  'BaseUrl':'',
  'title':'CRM Fas',
  'copyright':'copyright 2005 - {{cur_year}}',
=======
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
>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  #'encrypt_method':'mysql_sha2',
  #'encrypt_method':'encrypt',
  'use_project':False,
  'auth':{
    # Таблица авторизации:
    'manager_table':'owner',
    'manager_table_id':'id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    'encrypt_method':'mysql_encrypt',
    
    # b2bb2bconnect / 123
    # UPDATE manager password=sha2('123',256) where login='b2bb2bconnect';
    # Сессия:
    'session_table':'session_owner',
    'session_fails_table':'session_owner_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
<<<<<<< HEAD
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
  'system_url':'https://fas.crm-dev.ru/',
  'connects':{
    'crm_read':{
      'user':'fas',
      'password':'',
      'host':'localhost',
      'dbname':'fas',
    },
    'crm_write':{
      'user':'fas',
      'password':'',
      'host':'localhost',
      'dbname':'fas',
=======
    'use_permissions':False
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
      'user':'teleweb',
      'password':'',
      'host':'localhost',
      'dbname':'teleweb',
    },
    'crm_write':{
      'user':'teleweb',
      'password':'',
      'host':'localhost',
      'dbname':'teleweb',
>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
    },
  },
  'stat_log':0, # Записываем статистику посещений
  'controllers':{
<<<<<<< HEAD
    
    #'left_menu':'/fas/left-menu'
=======
    'left_menu':'/assist-ant/left-menu'
  },

  'docpack':{
    'user_table':'user',
    'docpack_foreign_key':'user_id'
>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
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
<<<<<<< HEAD
    'remember':False, # возможность напоминания пароля
=======
    'remember':True, # возможность напоминания пароля
>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
    
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
<<<<<<< HEAD
    'manager_id':585
    #'manager_id': 1, # Менеджер, под которым логинимся в том случае, если мы работаем в режиме дебага  
  }
=======
    'manager_id':1,
  },


>>>>>>> a090b4abe4b7855c027819e65e8f711e45198e6a
}
