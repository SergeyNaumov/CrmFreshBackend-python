

form={
    'work_table':'buhgalter_card',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Карточка бухгалтера',
    'sort':0,
    'tree_use':0,
    #'wide_form':1,
    'explain':0,
    'QUERY_SEARCH_TABLES':[
        {'t':'buhgalter_card','a':'wt'},
        {'t':'user','a':'u','l':'wt.id=u.id'},
        {'t':'manager','a':'m','l':'u.manager_id=m.id','lj':1,'for_fields':['manager_id','group_id']},
        {'t':'manager_group','a':'mg','l':'m.group_id=mg.id','lj':1,'for_fields':['group_id']},
    ],
    #'tabs':[
        
    #        {'description':'Ссылки','name':'links','not_save_button':1},
            
    #        {'description':'Реквизиты компании','name':'requsits','not_save_button':1},
    #        {'description':'Документы','name':'docs_buhgalter','not_save_button':1},
        #],
        #[
    #        {'description':'Общая информация','name':'info','not_save_button':1},
            #{'description':'Пакеты документов','name':'docpack'},
        #]
    #],
    'fields': [ 
        { # ссылки
          'tab':'links',
          'name':'links',
          'type':'code',
          
        },
        {
          'description':'Наименование компании',
          'type':'filter_extend_text',
          'name':'firm',
          #'full_str':1,
          'tablename':'u',
        },
        {
          'description':'Наименование компании',
          'name':'firm_c',
          'type':'code',
          ##'after_html':'5555',
          'tab':'info'
        },
        {
          'description':'Менеджер',
          'type':'filter_extend_select_from_table',
          'table':'manager',
          'header_field':'name',
          'value_field':'id',
          'name':'manager_id',
          'tablename':'m',
        },
        {
          'description':'Менеджер',
          'type':'code',
          'name':'manager_id_c',
          'tab':'info',
        },
        {
          'description':'Группа менеджера',
          'type':'filter_extend_select_from_table',
          'table':'manager_group',
          'header_field':'header',
          'value_field':'id',
          'tablename':'mg',
          'name':'group_id',
        },
        # Реквизиты
        {
          'description':'Реквизиты',
          'name':'requisits',
          'type':'1_to_m',
          'table':'buhgalter_card_requisits',
          'foreign_key':'user_id',
          'table_id':'id',
          
          
          'tab':'requsits',
          'view_type':'list',
          #'link_add':'/edit_form/buhgalter_card_requisits?user_id=<%form.id%>',
          #'link_edit':'/edit_form.pl?action=edit&config=buhgalter_card_requisits&id=<%id%>',
          'fields':[
                      {
                        'description':'Реквизиты по умолчанию',
                        'type':'checkbox',
                        'name':'main'
                      },
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
                        'name':'gen_dir_f_in',
                        'type':'text',
                        'tab':'rekvizits'
                      },

                    ]  
          
        }

  ]  
    
}
      

