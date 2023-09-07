

form={
    'work_table':'brand',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Администрирование брендов',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'fields': [ 
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
            'tab':'main'
        },
        {
            'description':'Лого',
            'name':'logo',
            'type':'file',
            'filedir':'./files/logo'
        }

  ]  
    
}
      

