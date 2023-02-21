# UPDATE manager set password=sha2('123',256);

import re
def after_create_engine(s,errors=[]):
  #print('AFTER CREATE ENGINE: ',s.manager)
  if not(s.manager) or not s.manager['login']:
    return
  
  
  host=s.env['host']

  d=host.split('.')
  if d[0]=='www':
    host='.'.join(d[1:])
  
  s.manager=s.db.query(
    query='select manager_id id,full_access,login from manager where manager_id=%s',
    values=[s.manager['id']],
    onerow=1
  )
  
  s.manager['host']=host
  
  host='newds.design-b2b.com' # for debug
  project=s.db.query(
    query='''
      select
        d.project_id,d.template_id, if(mpa.id is null,0,1) access_for_cur_domain
      from
        domain d
        LEFT JOIN manager_project_access mpa ON d.project_id=mpa.project_id and mpa.manager_id=%s
      where d.domain=%s limit 1
    ''',
    errors=s.errors,
    #debug=1,
    values=[s.manager['id'],host],
    onerow=1
  )
  #print('Project:',project)
  if not(project):
    s.errors.append(f'Не найден проект, привязанный к {host}')
    return 
  elif not(project['access_for_cur_domain']) and not(s.manager['full_access']):
    s.errors.append(f'У Вас нет доступа для администрирования сайта {host}')

  s.project_id=project['project_id']
  s.template_id=project['template_id']

  #print("project_id:",s.project_id)
  #print('MANAGER:',s.manager)
  #s.errors=[f'Домен {host} не найден в базе данных! Доступ запрещён']
  
  


# 
def after_read_form_config(form):
  if len(form.s.errors):
    form.errors=form.s.errors
  
  print('s:',form.s)
  form.manager=form.s.manager
  form.manager['files_dir']=f'./files/project_{form.s.project_id}'
  form.manager['files_dir_web']=f'/files/project_{form.s.project_id}'

# Будет выполняться для каждой операции insert / delete / update в crm
def alter_all_change_action(form):
  # Это нужно для сброса кэша у клиентских сайтов
  host=form.s.manager['host']
  print('Alter_all_change_action: ',host)
  

config={
  'BaseUrl':'/manager',
  'title':'CMS Digitalstrateg',
  'copyright':'copyright 2005 - {{cur_year}}',
   'bottom_menu': [
      {'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  #'encrypt_method':'mysql_sha2',
  
  'use_project':False,
  'auth':{
    # Таблица авторизации:
    'manager_table':'manager',
    'manager_table_id':'manager_id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    #'encrypt_method':'mysql_encrypt',
    'encrypt_method':'mysql_sha2',
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
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config, # Вызывается после чтения конфига от CRM
  'after_all_change_action':alter_all_change_action,
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
        '/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password'
    ]
  },

  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id': 4624, # b2bb2bconnect  
  }
}



  
  # Если нет доступа ко всем сайтам, то смотрим, есть ли он к данному домену

