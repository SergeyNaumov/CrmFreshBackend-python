form={
    'work_table':'content',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Статичные страницы',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'search_on_load':1,
    'fields': [ 
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'unique':1,
            'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True
        },
        {
            'description':'Название страницы',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':False
        },
  ]  
    
}
      


