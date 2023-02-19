#from .fields import get_fields
form={
    'work_table':'struct_5759_owner_warning',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Форма "сообщить о проблеме руководству',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Тема сообщения',
            'type':'text',
            'name':'header',
            'regexp_rules':[
                '^.+','Тема не указана',
            ],
            'filter_on':1
        },
        {
            'description':'Срочность',
            'type':'text',
            'name':'ugency_id',
            'values':[
                {'v':1,'d':''},
                {'v':2,'d':''},
                {'v':3,'d':''},
            ],
        },
        {
            'description':'Сообщение',
            'type':'text',
            'name':'message',
            'regexp_rules':[
                '^.+','Сообщение не заполнено',
            ]
        },
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ]
        },
        {
            'description':'Название компании',
            'type':'text',
            'name':'firm',
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
            'regexp_rules':[
                '^.+@.+','Адрес электронной почты заполнен не корректно',
            ]
        },
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'name':'registered',
            'filter_on':1
        }
  ]  
    
}
      


