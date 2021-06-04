# UPDATE manager set password=sha2('123',256);
config={
  'title':'CRM АннА',
  'copyright':'copyright 2005 - {{cur_year}}',
  'encrypt_method':'mysql_sha2',
  'use_project':False,
  'system_email':'svcomplex@gmail.com',

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
    #'left_menu':'/left-menu'
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

  'debug':{ # для отладки
    'hosts':['sv-home','sv-digital','sv-HP-EliteBook-2570p','asus-tarusa'],
    #'manager_id': 1, # Менеджер, под которым логинимся в том случае, если мы работаем в режиме дебага
    #'manager_id':152, # tk@digitalstrateg.ru (юрлицо)
    #'manager_id': 141, # dir1@digitalstrateg.ru Кнейжиц Игорь Владимирович, Представитель юридического лица
    #'manager_id': 211, # pavlik-libra5@mail.ru, Представитель юридического лица
    #'manager_id':228, # (в подчинении 3 аптеки) realko2-z@mail.ru, Представитель юридического лица
    #'manager_id':144, # Представитель артеки: apt2@digitalstrateg.ru
    'manager_id':248, # представитель аптеки (с подпиской на акции)
  
  }
}