#from configs.teleweb.messenger_rules import messenger_rules
#from configs.teleweb.gptassist_rules import gptassist_rules
from configs.svcmsadmin.config_wysiwyg import config_wysiwyg


# Админка работает вне проекта, но read_config всегда читает
# request.state.project['project_id'] (lib/all_configs.py:155),
# поэтому after_create_engine обязан заполнить request.state.project.
async def after_create_engine(s, request, errors=[]):
  if not getattr(request.state, 'project', None):
    request.state.project = {
      'project_id': None,
      'template_id': None,
      'access_for_cur_domain': 1,
    }
  manager = request.state.manager
  manager['files_dir']='./files'
  manager['files_dir_web']='/files'
  if manager and manager.get('id'):
    manager['host'] = s.env.get('host', '')
    request.state.manager = manager


# Будет выполняться для каждой операции insert / delete / update в crm.
# Для админки сброс кэша клиентских сайтов не нужен -- заглушка.
def alter_all_change_action(form):
  pass


config={
  'title':'DigitalStrateg Admin Panel',
  'app_components':{
    'navigator':True
  },
  'BaseUrl':'',
  'BaсkendBase':'http://dev-crm.test/backend',
  'copyright':'copyright 2004 - {{cur_year}}',
   'bottom_menu': [
      #{'header':'Политика конфиденциальности','type':'url','url':'/securitypolicy.html','target':'_blank'}
   ],
  'encrypt_method':'mysql_encrypt',
  'use_project':False,

  'auth':{
    # Таблица авторизации (админы SV-CMS):
    'manager_table':'admin',
    'manager_table_id':'admin_id',
    'auth_log_field':'login',
    'auth_pas_field':'password',
    # Пароли в admin хранятся в старом MySQL ENCRYPT (varchar(40))
    'encrypt_method':'mysql_encrypt',
    # Сессия:
    'session_table':'admin_session',
    'session_fails_table':'admin_session_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600,
    'use_roles':False,
    'use_permissions':False
  },

  'messenger_rules':{},#messenger_rules,
  'gptassist_rules':{},#gptassist_rules, # функция,

  'startpage':{ # указываем, какой компонент будет загружаться на главной странице
    'type':'src',
    'value':'/manager/mainpage.html',
  },
  'after_create_engine':after_create_engine,
  #'after_read_form_config':after_read_form_config,
  'system_email':'svcomplex@gmail.com',
  'after_all_change_action':alter_all_change_action,
  'system_url':'https://admin.design-b2b.com/',
  'config_folder':'configs/svcmsadmin',
  #'stat_log':1, # Записываем статистику посещений
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
  'controllers':{
    'left_menu':'/svcmsadmin/left-menu-admin' # меню из таблицы admin_menu_new
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
  'wysiwyg':config_wysiwyg,
  
  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id':51, # naumov
  },

  # Фоновые задачи (очередь crm_background): воркеры стартуют внутри uvicorn.
  'background':{
    'enabled':True,
    'workers':4,
    'poll':0.5,
    'stale_minutes':10,
  },

  # Пути серверных действий админки (экспорт/клонирование/структуры).
  'paths':{
    'cms':'/var/www/sv-cms/htdocs',
    'exported_projects':'/var/www/sv-cms/htdocs/exported_projects',
    'templates':'/var/www/sv-cms/htdocs/templates',
    'files':'./files',
    'export_script':'/var/www/sv-cms/htdocs/admin2/api/scripts/copy_and_create',
    # Файлы проектов на движке сайтов (/files/project_<id>/…). URL — относительный
    # (/files/...): в превью конструктора и редакторе резолвится от домена админки.
    'engine_files':'/var/www/svcms-async/sites/files',
    'engine_files_url':'/files',
    # Оптимизация загружаемых картинок блоков: длинная сторона (px) и
    # качество webp. Растровые конвертируются в webp, svg — как есть.
    'block_images_max_side':1920,
    'block_images_quality':82,
    # Корень движка сайтов и каталог per-project конфигов (для быстрого
    # создания проекта: копирование файлов по чекбоксу «демо-контент»).
    'engine_root':'/var/www/svcms-async/sites',
    'conf_projects':'./conf_projects',
  },

  # Быстрое создание проекта (svcmsadmin-createproject): проект-эталон для
  # констант, демо-контента ds_* и файлов проекта.
  'fast_create':{
    'source_project_id':5837,
  },

}
