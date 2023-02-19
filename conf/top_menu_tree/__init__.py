#from .fields import get_fields
form={
    'work_table':'top_menu_tree',
    'work_table_id':'top_menu_tree_id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Верхнее меню',
    'sort':1,
    'tree_use':1,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'fields':[
 
        {
            'description':'Наименование пункта меню',
            'type':'text',
            'name':'header',
        },
        {
          'description':'url',
          'name':'url',
          'type':'text'
        }
   
    ]
}
      


