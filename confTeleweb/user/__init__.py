from lib.engine import s

form={
    #'work_table':'good',
    #'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Клиенты',
    'sort':False,
    'tree_use':False,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        
        {'t':'user','a':'wt'},
    ],
    #'read_only':True,
    'search_on_load':1,
    'fields': [ 

        {
            'description':'Id в telegram',
            'type':'text',
            'name':'tg_id',
            'filter_on':True
        },
        {
            'description':'Логин в telegram',
            'type':'text',
            'name':'username',
            'filter_on':True
        },
        {
            'description':'Имя',
            'type':'text',
            'name':'first_name',
            'filter_on':True
        },
        {
            'description':'Фамилия',
            'type':'text',
            'name':'last_name',
            'filter_on':True
        },
        {
            'description':'Метка регистрации',
            'type':'text',
            'name':'mark',
            'filter_on':True
        },
        {
            'description':'Дата и время регистрации',
            'type':'datetime',
            'name':'ts',
            'filter_on':True
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'filter_on':True
        },
  ]  
    
}
      


