# UPDATE manager set password=sha2('123',256);
from confTeleweb.messenger_rules import messenger_rules
def after_create_engine(s,errors=[]):
  # для dev-а переделано!
  if not(s.manager) or not s.manager['login']:
    return
  host=s.env['host']

  d=host.split('.')
  if d[0]=='www':
    host='.'.join(d[1:])
  
  shop=s.db.query(
    query=f'''
      SELECT
        o.*, s.id shop_id, s.domain, s.template_id, s.botname,
        s.need_serv, s.need_good, s.token
      FROM
        owner o
        join shop s ON s.owner_id=o.id
      WHERE o.id=%s 
    ''',
    values=[s.manager['id']],
    onerow=1
  )
  s.manager['filedir_http']=''
  if shop:
    s.manager=shop
    s.shop=shop
    s.shop_id=shop['shop_id']
    s.template_id=shop['template_id']
    s.manager['filedir_http']=f'/files/project_{s.shop_id}'


  else:

   s.errors.append(f'У Вас нет права для администрирования {host}')
   return 

def after_read_form_config(form):
  if len(form.s.errors):
    form.errors=form.s.errors
  
  form.manager=form.s.manager
  form.manager['files_dir']=f'./files/project_{form.s.shop_id}'
  form.manager['files_dir_web']=f'/files/project_{form.s.shop_id}'

def alter_all_change_action(form):
  # Это нужно для сброса кэша у клиентских сайтов

  # Если вносятся изменения конструкторе бота, то обновляем контсанту, 
  # тем самым сообщая боту, что необходимо обновить правила
  if form.config=='bot_rules':
    form.db.query(
        query='UPDATE const set value=unix_timestamp(now()) where shop_id=%s and name=%s',
        values=[form.s.shop_id,'_last_update_botcommands'],
        #debug=1,
    )

config={
  'title':'AssistWeb admin panel',
  'copyright':'copyright 2004 - {{cur_year}}',
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  'encrypt_method':'mysql_sha2',
  'use_project':False,
  
  'auth':{
    # Таблица авторизации:
    'manager_table':'owner',
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
    'use_roles':False,
    'use_permissions':False
  },
  'messenger_rules':messenger_rules,
  'startpage':{ # указываем, какой компонент будет загружаться на главной странице
    'type':'src',
    'value':'/manager/mainpage.html',
  },
  'after_create_engine':after_create_engine,
  'after_read_form_config':after_read_form_config,
  'system_email':'svcomplex@gmail.com',
  'after_all_change_action':alter_all_change_action,
  'system_url':'https://adminbot.assist-ant.su/',
  'config_folder':'confTeleweb',
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
