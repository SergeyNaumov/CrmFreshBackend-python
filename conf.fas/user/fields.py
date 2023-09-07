fields=[
        {
            'tab':'links',
            'name':'links',
            'type':'code',
            
        },
        {
            'description':'Бренд',
            'name':'brand_id',
            'type':'select_from_table',
            'table':'brand',
            'tablename':'b',
            'header_field':'header',
            'value_field':'id',
            'tab':'main',
            'read_only':True,
            'frontend':{'ajax':{'name':'brand_id','timeout':100}},

            'filter_on':True,
        },
        {
            'description':'Название компании',
            'name':'firm',
            'type':'text',
            'tab':'main',
            'filter_on':True,
        },
        {
            'description':'Город',
            'name':'city',
            'type':'text',
            'tab':'main'
        },
        {
            'description':'Адрес',
            'name':'address',
            'subtype':'kladr',
            'kladr':{
                #'after_search':kladr_after_search
            },
            'type':'text',
            'tab':'main'
        },
        {
            'description':'Инн',
            'add_description':'для ИП 12 цифр, для остальных организаций 10',
            'name':'inn',
            'type':'text',
            'tab':'main',
            'regexp_rules':[
                '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ]
        },
        {
            'description':'КПП',
            'name':'kpp',
            'type':'text',
            'tab':'main',
            'regexp_rules':[
                '/^(\d{9})?$/i','КПП должен содержать 9 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ],
            #'subtype':'qr_call',
        },
        {
            'description':'Зарегистрирована',
            'name':'registered',
            'type':'date',
            'read_only':True,
            'tab':'main',
        },
        {
            'description':'Контакты',
            'name':'contacts',
            'type':'1_to_m',
            'table':'user_contact',
            'foreign_key':'user_id',
            'table_id':'id',
            'view_type':'list',
            'fields':[
                {
                    'description':'ФИО',
                    'name':'fio',
                    'type':'text',
                },
                {
                    'description':'Email',
                    'name':'email',
                    'type':'text',
                },
                {
                    'description':'Телефон',
                    #'add_description':'В формате +7XXXXXXXXXX, например: +74951234567',
                    'name':'phone',
                    'type':'text',
                    'subtype':'qr_call',
                    'replace_rules':[
                        '/^8/','+7',
                        '/^92/', '+792',
                        '/;/g',',',
                        
                        '/,$/',', ',
                        '/\s+,/', ', ',
                        '/\s+,/g', ',',
                        '/[^\s,\d\+]/g','',
                        '/, 8/',', +7',
                        #'\s\s+',' ',
                        #'/^\s+/','',
                        #'/\s+,/',', ',
                        
                        

                    ],
                    'regexp_rules':[
                        '/^(\+\d{6,12})(,\s\+\d{6,12})*$/','Номер должен быть в формате: +[код]XXXXXXXXXX, например: +74951234567',
                       
                    ],
                },
                {
                    'description':'Должность',
                    'name':'position',
                    'type':'text',
                },
                {
                    'description':'Ответственный',
                    'name':'otv',
                    'type':'checkbox',
                },
                {
                    'description':'Комментарий',
                    'name':'comment',
                    'type':'text',
                },
            ],
            'tab':'main',
        },        
        {
            'description':'Менеджер',
            'name':'manager_id',
            'type':'select_from_table',
            'table':'manager',
            'tablename':'m',
            'header_field':'name',
            'value_field':'id',
            'tab':'sale',
            'filter_on':True
        },
        {
            'description':'Группы менеджеров',
            'type':'filter_extend_select_from_table',
            'name':'f_manager_group',
            'table':'manager_group',
            #'tree_use':True,
            'tablename':'mg',
            'header_field':'header',
            'value_field':'id'
        },
        {
            'description':'Дата контакта',
            'name':'contact_date',
            'type':'date',
            'tab':'sale',
        },
        { # Memo
            # Комментарий 
            'description':'Состояние',
            'name':'memo',
            'type':'memo',
            'memo_table':'user_memo',
            'memo_table_id':'id',
            'memo_table_comment':'body',
            'memo_table_auth_id':'manager_id',
            'memo_table_registered':'registered',
            'memo_table_foreign_key':'user_id',
            'auth_table':'manager',
            'auth_login_field':'login',
            'auth_id_field':'id',
            'auth_name_field':'name',
            'reverse':1,
            'memo_table_alias':'memo',
            'auth_table_alias':'m_memo',
            'make_delete':False,
            'make_edit':False,
            'tab':'sale'
        },
        {
            'description':'Состояние2',
            'name':'state2',
            'type':'textarea',
            'tab':'sale'
        },
        {
            'description':'ОТК',
            'name':'otk',
            'type':'checkbox',
            'read_only':True,
            #'before_code':otk_before_code,
            'tab':'sale',
        },
        {
            'description':'ДТ2',
            'name':'dt2',
            'type':'checkbox',
            'read_only':True,
            #'before_code':dt2_before_code,
            'tab':'sale',
        },
        {
            'description':'Презентация заявки',
            'name':'prez_order',
            'type':'checkbox',
            'tab':'sale',
        },
        {
            'description':'Презентация заявки, отмена',
            'name':'prez_order_cancel',
            'type':'checkbox',
            'tab':'sale',
        },
        # {
        #     'description':'',
        #     'name':'',
        #     'type':'',
        #     'tab':'sale',
        # },
        # {
        #     'description':'',
        #     'name':'',
        #     'type':'',
        #     'tab':'sale',
        # },
    ]