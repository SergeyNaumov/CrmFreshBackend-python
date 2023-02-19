#from .fields import get_fields
form={
    'work_table':'struct_5759_team',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Команда',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Должность',
            'type':'text',
            'name':'position',
        },
        {
            'description':'Фото',
            'type':'file',
            'name':'photo',
            'filedir':'./files/project_5759/team',
            'crops':True,
            'resize':[
                       {
                       'description':'Квадратное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       'size':'280x280',
                       'quality':'90'
                       }
            ]
        },

  ]  
    
}
      


