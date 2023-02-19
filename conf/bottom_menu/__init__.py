#from .fields import get_fields
form={
    'work_table':'bottom_menu',
    'work_table_id':'bottom_menu_id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Нижнее меню',
    'sort':1,
    'tree_use':0,
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
      


