def inn_before_code(form,field):
    # разрешаем редактировать только руководителям и сотрудникам с расширенными полномочиями:
    if form.id:
        if not(form.is_owner_group or form.manager['permissions'].get('user_edit_all')):
            field['read_only']=True

fields=[
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
            'description':'В архиве',
            'type':'checkbox',
            'name':'archive',
            'read_only':1,
            'tab':'main'
        },
        # {
        #     'description':'Логин',
        #    'name':'login',
        #     'type':'text',
        #     'tab':'main',
        #     'filter_on':False,
        # },
        {
            'description':'Название компании',
            'name':'firm',
            'type':'text',
            'tab':'main',
            'regexp_rules':[
                #'/[абвгдеёжзийклмнопрстуфхцчшщьыъэюяa-z]+/i','Нужно указать корректное название компании',
            ],
            'filter_on':True,
        },
        {
            'description':'Регион',
            'name':'region_id',
            'type':'select_from_table',
            'table':'region',
            'tablename':'r',
            'header_field':'header',
            'value_field':'region_id',
            'frontend':{'ajax':{'name':'region_id','timeout':100}},
            'tab':'main',

        },
        {
            'description':'Город',
            'name':'city_id',
            'type':'select_from_table',
            'table':'city',
            'tablename':'c',
            'header_field':'name',
            'value_field':'city_id',
            'autocomplete':1,
            'search_query':"""
                  SELECT
                    c.city_id v, concat(r.header,' -> ', c.name ) d
                  FROM
                    city c
                    join region r ON (r.region_id=c.region_id)
                    where c.name like <%v%>
            """,
            'frontend':{'ajax':{'name':'city_id','timeout':100}},
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
            'before_code': inn_before_code,
            'frontend':{'ajax':{'name':'inn','timeout':100}},
            'regexp_rules':[
                '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ],
            'frontend':{'ajax':{'name':'inn','timeout':300}},
        },
        # {
        #     'description':'КПП',
        #     'name':'kpp',
        #     'type':'text',
        #     'tab':'main',
        #     'regexp_rules':[
        #         '/^(\d{9})?$/i','КПП должен содержать 9 цифр',
        #     ],
        #     'replace_rules':[
        #         '/[^0-9]/', ''
        #     ],
        # },
        {
            'description':'Зарегистрирована',
            'name':'registered',
            'type':'date',
            'read_only':True,
            'tab':'main',
        },
        {
            'description':'Телефон',
            'type':'filter_extend_text',
            'tablename':'uc',
            'name':'f_phone',
            'db_name':'phone'
        },
        {
            'description':'Email',
            'type':'filter_extend_text',
            'tablename':'uc',
            'name':'f_email',
            'db_name':'email'
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
                    'subtype':'email',
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
                        '/^(\+\d{6,12})$/','Номер должен быть в формате: +[код]XXXXXXXXXX, например: +74951234567',
                       
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
]