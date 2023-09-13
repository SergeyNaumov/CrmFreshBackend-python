

form={
    'work_table':'rejection_assignment',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Протоколы отказ (онлайн) список менеджеров',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'make_delete':False,
    'read_only':True,
    'QUERY_SEARCH_TABLES':[
        {'t':'rejection_assignment','a':'wt'},
        {'t':'manager','a':'m','l':'wt.manager_id=m.id'}
    ],

    'search_links':[
        

    ],
    'fields':
    [ 
    
    {
        'description':'Менеджер',
        'name':'manager_id',
        'filter_on':True,
        'type':'select_from_table',
        'table':'manager',
        'tablename':'m',
        'header_field':'name',
        'value_field':'id',
        'table_name':'m'
    },
    # {
    #  'description':'Коэффициент',
    #  'filter_on':1,
    #  'type':'text',
    #   #regexp=>'^\d+$',
    #  'name':'coefficient'
    # },
    {
     'description':'Временная зона',
     'add_description':'например +4 -- это Омск, 0 -- Москва',
     'name':'timeshift',
     'type':'select_values',
     'values':[
        {'v':'-1','d':'-1 (Калининград)'},
        {'v':'0','d':'0 (Москва)'},
        {'v':'1','d':'+1 (Самара)'},
        {'v':'2','d':'+2 (Екатеринбург)'},
        {'v':'3','d':'+3 (Омск)'},
        {'v':'4','d':'+4 (Красноярск)'},
        {'v':'5','d':'+5 (Иркутск)'},
        {'v':'6','d':'+6 (Якутск)'},
        {'v':'7','d':'+7 (Владивосток)'},
        {'v':'8','d':'+8 (Магадан)'},
        {'v':'9','d':'+9 (Камчатка)'},
      ]
    }
  ]  
    
}
      


