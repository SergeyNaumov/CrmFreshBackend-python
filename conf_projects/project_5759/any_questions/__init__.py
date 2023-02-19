#from .fields import get_fields
form={
    'work_table':'struct_5759_any_questions',
    'work_table_id':'id',
    'title':'Форма "Остались вопросы / Задать вопрос"',    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5759_any_questions','a':'wt'},
        {'t':'struct_5759_service','a':'s','l':'wt.service_id=s.id','lj':1},
    ],
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'filter_on':1,
            'regexp_rules':[ '^.+$','Заполните имя']
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'filter_on':1,
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ]
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
            'filter_on':1,
            'name':'registered',
        }
  ]  
    
}
      


