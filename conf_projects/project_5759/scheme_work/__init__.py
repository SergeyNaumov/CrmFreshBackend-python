#from .fields import get_fields
form={
    'work_table':'struct_5759_scheme_work',
    'work_table_id':'id',
    'title':'Схема работы',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Число',
            'type':'text',
            'name':'num',
        },
        # {
        #     'description':'Иконка',
        #     'add_description':'347x265',
        #     'filedir':'./files/project_5759/scheme_work',
        #     'type':'file',
        #     'name':'icon',
        # },
        {
            'description':'Текст',
            'type':'wysiwyg',
            'name':'body',
        },
  ]  
    
}
      


