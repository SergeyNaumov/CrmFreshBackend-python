
form={
    'work_table':'struct_[project_id]_zakaz', # заполняется в events
    'work_table_id':'id',
    'title':'Заказы',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'wide_form':True,
    'changed_in_tree':True,
    'search_on_load':1,
    'fields': [ 
        {
            'description':'№ заказа',
            'type':'text',
            'name':'id',
            'filter_on':1,
            'read_only':1,
        },
        {
            'description':'Статус заказа',
            'type':'select_values',
            'name':'status',
            'values':[
                {'v':'0','d':'поступил'},
                {'v':'1','d':'принят в работу'},
                {'v':'2','d':'отклонён'},
                {'v':'3','d':'передан в доставку'},
                {'v':'4','d':'доставлен'},
            ]
        },
        {
            'description':'Дата заказа',
            'type':'date',
            'read_only':1,
            'name':'registered',
            'filter_on':1
        },
        {
            'description':'Пользователь',
            'type':'select_from_table',
            'name':'user_id',
            'table':'bot_user',
            #'header_field':'username',
            'header_field':'concat("@",username," ",first_name," ",last_name," ",phone)',
            #'db_name':'username',
            'value_field':'id',
            'tablename':'u',
            #'where':'bot_id=3',
            'filter_on':1
        },
        {
            'description':'ФИО',
            'type':'text',
            'name':'name',
            'regexp_rules':[ '^.+$','Заполните имя'],
            'filter_on':1
        },
        # {
        #     'description':'Телефон',
        #     'type':'text',
        #     'name':'phone',
        #     'regexp_rules':[
        #         '^[\+0-9\-\(\)\s]+$','Телефон не заполнен или заполнен некорректно',
        #     ]
        # },
        {
            'description':'Адрес',
            'type':'text',
            'name':'address',
            'regexp_rules':[
                '^.+','Пожалуйста укажите адрес',
            ],
            'filter_on':1
        },
        {
            'description':'Пожелания к заказу',
            'type':'text',
            'name':'message',
            'filter_on':1
        },
        {
            'description':'Способ доставки',
            'type':'select_from_table',
            'table':'', # заполняем в events
            'tablename':'d',
            'name':'delivery_id',
            'header_field':'header',
            'value_field':'id',
            'order':'sort',
            'filter_on':1
        },
        {
            'description':'Способ оплаты',
            'type':'select_from_table',
            'table':'struct_[project_id]_paid', # заполняем в events
            'name':'paid_id',
            'tablename':'p',
            'header_field':'header',
            'value_field':'id',
            'order':'sort',
            'filter_on':1
        },
        {
            'description':'Товары',
            'type':'code',
            'name':'goods',
            'full_str':1,
            'after_html':'//'
        }
  ]  
    
}



