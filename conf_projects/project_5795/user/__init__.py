form={
    'work_table':'bot_user',
    'work_table_id':'id',
    'title':'Способы оплаты',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'wide_form':True,
    'changed_in_tree':True,
    'read_only':1,
    'search_on_load':1,
    'fields': [ 
        {
            'description':'Id в telegram',
            'type':'text',
            'name':'tg_id',
            'tab':'main',
            'filter_on':1,
            'read_only':1,
        },
        {
            'description':'Логин в telegram',
            'type':'text',
            'name':'username',
            'read_only':1,
            'filter_on':1,
        },
        {
            'description':'Имя',
            'type':'text',
            'name':'first_name',
            'read_only':1,
            'filter_on':1,
        },
        {
            'description':'Фамилия',
            'type':'text',
            'name':'last_name',
            'read_only':1,
            'filter_on':1,
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'read_only':1,
            'filter_on':1,
        },
        {
            'description':'Время регистрации',
            'type':'date',
            'name':'ts',
            'read_only':1,
            'filter_on':1,
        },
  ]  
    
}
      


