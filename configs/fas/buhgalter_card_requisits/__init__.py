form={
    'work_table':'buhgalter_card_requisits',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Реквизиты компании',
    'sort':0,
    'tree_use':0,
    'wide_form':1,
    'explain':0,
    'QUERY_SEARCH_TABLES':[
        {'t':'buhgalter_card_requisits','a':'wt'},
        {'t':'user','a':'u','l':'wt.buhgalter_card_id=u.id'},

    ],
    'fields': [ 
    {
      'description':'Наименование компании',
      'add_description':'или ФИО для физ.лиц',
      'type':'text',
      'name':'firm',
    },
    {
      'description':'Факт. адрес',
      'name':'address',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'Юр. адрес',
      'name':'ur_address',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'ИНН',
      'name':'inn',
      'type':'text',
      'regexp_rules':[
          '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
      'tab':'rekvizits',
    },
    {
      'description':'КПП',
      'name':'kpp',
      'type':'text',
      'tab':'rekvizits',
      #regexp=>'^(\d{9})?$',
      'regexp_rules':[
          '/^(\d{9})?$/i','КПП может включать 9 цифр',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
    },
    {
      'description':'ОГРН',
      'name':'ogrn',
      'type':'text',
      'tab':'rekvizits',
      #regexp=>'^(\d{13,15})?$'
      'regexp_rules':[
          '/^(\d{13,15})?$/i','ОГРН не корректен',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
    },
    {
      'description':'р/с',
      'name':'rs',
      'type':'text',
      'tab':'rekvizits',
      'regexp_rules':[
          '/^(\d{20})?$/i','р/с не корректен',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
      #regexp=>'^(\d{20})?$'
    },
    {
      'description':'к/с',
      'name':'ks',
      'type':'text',
      'tab':'rekvizits',
      #regexp=>'^(\d{20})?$'
      'regexp_rules':[
          '/^(\d{20})?$/i','к/с не корректен',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
    },
    {
      'description':'БИК',
      'name':'bik',
      'type':'text',
      'tab':'rekvizits',
      #regexp=>'^(\d{9})?$'
      'regexp_rules':[
          '/^(\d{9})?$/i','БИК не корректен',
      ],
      'replace_rules':[
          '/[^0-9]/', ''
      ],
    },
    {
      'description':'Банк',
      'name':'bank',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'Должность ответственного лица (именит.)',
      'name':'position_otv',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'Должность ответственного лица (род.)',

      'name':'position_otv_rod',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'ФИО ген. директора (именит.)',
      'name':'fio_dir',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'ФИО ген. директора (родит.)',
      'name':'fio_dir_rod',
      'type':'text',
      'tab':'rekvizits'
    },
    {
      'description':'И.О. Фамилия директора',
      'name':'gen_dir_f_im',
      'type':'text',
      'tab':'rekvizits'
    },

  ]  
    
}
      

