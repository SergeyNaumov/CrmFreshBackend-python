
form={
    'work_table':'admin_tg',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Правила поведения бота',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'tg_login',
    'search_on_load':True,
    'fields': [ 
        {
            'description':'Логин в telegram',
            'regexp_rules':[
                '/^[^@]+$/','Укажите логин telegram без @',
            ],
            'name':'tg_login',
            'type':'text',
            'filter_on':1,
        },
        {
            'description':'подтверждён',
            'name':'accepted',
            'type':'checkbox',
            'read_only':True,
            'filter_on':1,
        }

    ]  
    
}
      


