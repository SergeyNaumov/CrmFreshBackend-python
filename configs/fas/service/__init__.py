form={
    'work_table':'service',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Услуги для техзаданий',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
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
          'description':'Дополнительные поля',
          'type':'1_to_m',
          'table':'service_field',
          'table_id':'id',
          'foreign_key':'service_id',
          'name':'service_fields',
          'sort':True,
          'fields':[
            {'description': 'Название поля','name':'header','type':'text'}
          ]
        }

  ]  
    
}
      


