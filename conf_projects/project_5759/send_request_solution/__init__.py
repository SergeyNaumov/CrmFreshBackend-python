#from .fields import get_fields
form={
    'work_table':'struct_5759_send_request_solution',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Заявки на готовое решение',
    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5759_send_request_solution','a':'wt'},
        
    ],
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'regexp_rules':[
                '^.+$','Заполните имя',
            ],
            'filter_on':1
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ],
            'filter_on':1
        },
        {
            'description':'Что заинтересовало?',
            'type':'text',
            'name':'body',
            'filter_on':1
        },
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'name':'registered',
            'filter_on':1
        }
  ]  
    
}
      


