#from .fields import get_fields
form={
    'work_table':'struct_5759_need_consult',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Нужна консультация',
    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5759_need_consult','a':'wt'},
        {'t':'struct_5759_service','a':'s','l':'wt.service_id=s.id','lj':1},
    ],
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'regexp_rules':[ '^.+$','Заполните имя' ],
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
            'description':'Услуга',
            'type':'select_from_table',
            'table':'struct_5759_service',
            'header_field':'header',
            'value_field':'id',
            'tablename':'s',
            'name':'service_id',
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
      


