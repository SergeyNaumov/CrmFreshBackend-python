#from .fields import get_fields
form={
    'work_table':'files',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Promo (для оптимизаторов)',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'url',
            'type':'text',
            'name':'url',
            'filter_on':True
        },
        {
          'description':'mime-type',
          'name':'type',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
        {
          'description':'Содержимое файла',
          'name':'body',
          'type':'textarea',
          'make_change_in_search':True,
          'filter_on':True
        },
  ]  
    
}
      


