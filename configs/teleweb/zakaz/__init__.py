from lib.engine import s

form={
    #'work_table':'good',
    #'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Заказы от пользователей',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'zakaz','a':'wt'},
        {'t':'user','a':'u','l':'wt.user_id=u.id','lj':1},
        {'t':'paid_method','a':'pm','l':'wt.paid_method_id=pm.id','lj':1},
        {'t':'delivery','a':'d','l':'wt.delivery_id=d.id','lj':1},
    ],
    #'explain':1,
    'search_on_load':1,
    'fields': [ 

        {
            'description':'Дата и время заказа',
            'type':'datetime',
            'name':'ts',
            'read_only':True,
            'filter_on':True
        },
        {
            'description':f'Пользователь',
            'name':'user_id',
            'type':'filter_extend_select_from_table',
            'table':'user',
            'filter_on':1,
            'query':f'''
                SELECT id v, concat(first_name, ' ',phone) d
                FROM
                    user
                WHERE shop_id={s.shop_id}
            ''',
            'header_field':'first_name',
            'value_field':'id',
            'tablename':'u',
#            'filter_code':user_id_filter_code
            #'where':f'shop_id={s.shop_id}'
        },
        {
            'description':'Способ оплаты',
            'type':'select_from_table',
            'name':'paid_method_id',
            'table':'paid_method',
            'tablename':'pm',
            'header_field':'header',
            'value_field':'id'
        },
        {
            'description':'Способ доставки',
            'type':'select_from_table',
            'name':'delivery_id',
            'table':'delivery',
            'tablename':'d',
            'header_field':'header',
            'value_field':'id'
        },
        {
            'description':'Информация о заказе',
            'type':'code',
            'name':'zakaz_info'
        },
        {
            'description':'Статус заказа',
            'name':'status',
            'type':'select_values',
            'values':[
                {'v':1,'d':'в обработке'},
                {'v':2,'d':'собран'},
                {'v':3,'d':'отправлен'},
                {'v':4,'d':'доставлен'},
                {'v':5,'d':'возврат'},
                {'v':6,'d':'отменён'},
            ]
        }

        

  ]  
    
}
      


