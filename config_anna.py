# UPDATE manager set password=sha2('123',256);
config={
  'title':'CRM АннА',
  'copyright':'copyright 2005 - {{cur_year}}',
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
    'session_table':'session',
    'session_fails_table':'session_fails',
    'max_fails_login':50,
    'max_fails_login_interval':3600,
    'max_fails_ip':20,
    'max_fails_ip_interval':3600
  },
  'startpage':{ # указываем, какой компонент будет загружаться на главной странице
    'type':'src',
    'value':'/test.html',
  },
  'system_email':'svcomplex@gmail.com',
  'system_url':'https://anna.crm-dev.ru/',
  
  'stat_log':1, # Записываем статистику посещений
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

    'left_menu':'/anna/left-menu'
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
    'register':True, # возможность регистрации
    'remember':True, # возможность напоминания пароля
    
    # Доступно без авторизации
    'not_login_access': [
        '/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password'
    ]
  },
  # 8Xiddqdidkfa#762x
  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','sv-romanovka'],
    'manager_id':212,
    #  'manager_id':217, # nadezda_t97@mail.ru
    #'manager_id':217, # nadezda_t97@mail.ru
    #'manager_id':305 # | oooanna136@gmail.com
    #'manager_id':326 #  barahta-z@yandex.ru
    #'manager_id': 243 # juliy170583@mail.ru
    #'manager_id': 1, # Менеджер, под которым логинимся в том случае, если мы работаем в режиме дебага
    
    #'manager_id': 245, # oksana_voronezh@mail.ru
    #'manager_id':194, # natalja.tolubaeva@yandex.ru # ИП "Косолапова"
    #'manager_id': 328, # представитель ООО "Ринал" rinalapteka@mail.ru
    
    #'manager_id': 193, # Юрлицо "Амрита"
    #'manager_id':243, # Менеджер Анна с множеством юрлиц
    #'manager_id':152, # tk@digitalstrateg.ru (юрлицо)
    #'manager_id': 141, # dir1@digitalstrateg.ru Кнейжиц Игорь Владимирович, Представитель юридического лица
    #'manager_id': 211, # pavlik-libra5@mail.ru, Представитель юридического лица
    
    #'manager_id':144, # Представитель артеки: apt2@digitalstrateg.ru
    #'manager_id':248, # представитель аптеки (с подпиской на акции mandarin149@yandex.ru)
    #'manager_id':246, # tifilatova@bk.ru
    #'manager_id':183, # dimy@comch.ru (представитель химфарм)
    #'manager_id':259, # представитель аптеки himfarm5@kvmail.ru 
    #'manager_id':240, # aksilife@mail.ru
    
    #'manager_id':342 ,# farmmac@yandex.ru
    
    #'manager_id':275, # provizor-259-1
    #'manager_id':'460', #  medfarm1@inbox.ru
    #'manager_id':'331', #  deshina@mail.ru
    #'manager_id':228, # (в подчинении 3 аптеки) realko2-z@mail.ru, Представитель юридического лица
  },
  # Возможен дебаг по директории, в которой запущен сервер
  # 'debug':{ # для отладки
  #   'pwd':('/home/naumov/CrmFresh/frontend'),
  #   'login':'akulov'    
  # }

}