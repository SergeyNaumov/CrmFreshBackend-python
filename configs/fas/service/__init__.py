form={
    'work_table':'service',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Услуги для приложений договора',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'wide_form':False,
    'default_find_filter':'header',
    'fields': [ 
        # {
        #   'description':'Вкл',
        #   'type':'checkbox',
        #   'name':'enabled',
        #   'value':1
        # },
        {
          'description':'Название услуги',
          'name':'header',
          'type':'text',
          'filter_on':True
        },
        {
          'description':'Тип услуги',
          'name':'type',
          'type':'select_values',
          'values':[
            {'v':1,'d':'юр. услуга'},
            {'v':2,'d':'фин. услуга'},
          ],
          'filter_on':True
        },
        {
          'description':'Бланк',
          'add_description':'нужно выбрать бланк для приложения',
          'name':'blank_id',
          'type':'select_from_table',
          'table':'blank_document',
          'header_field':'header',
          'value_field':'id'
        },
        {
          'description':'Дополнительные поля',
          'type':'1_to_m',
          'table':'service_field',
          'table_id':'id',
          'foreign_key':'service_id',
          'name':'service_fields',
          'sort':True,
          'view_type':'list',
          'fields':[
            {
              'description': 'Название поля','name':'header','type':'text',
              'regexp_rulse':[
                '/.+/','Поле не пустое'
              ]
            },
            {
              'description': 'Имя переменной','name':'name','type':'text',
              'regexp_rulse':[
                '/.+/','Поле не пустое'
              ]
            },
          ]
        }

  ]  
    
}
      


