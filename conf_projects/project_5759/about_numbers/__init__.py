#from .fields import get_fields
form={
    'work_table':'struct_5759_about_numbers',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'О нас в цифрах',
    'sort':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'changed_in_tree':True, 
    'fields': [ 
        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Цифра',
            'type':'text',
            'name':'number',
        },
        {
            'description':'Текст',
            'type':'text',
            'name':'body',
        },
  ]  
    
}
      


