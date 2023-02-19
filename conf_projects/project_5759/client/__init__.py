#from .fields import get_fields
form={
    'work_table':'struct_5759_client',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Клиенты',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'search_on_load':1,
    'fields': [ 
        {
            'description':'Название компании',
            'type':'text',
            'name':'header',
            'filter_on':1,
        },
        {
            'description':'Лого',
            'name':'logo',
            'type':'file',
            'filedir':'./files/project_5759/client',
            'preview':'350x490',
            #'crops':True,
            'resize':[
                {
                    'description':'Для главной и внутренней страниц',
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'243x240',
                    'quality':'90'
                },
                {
                    'description':'для страницы "отзывы"',
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'213x157',
                    'quality':'90'
                },
            ],
            'filter_on':1,
        },
        {
            'description':'Дата',
            'type':'date',
            'name':'dat',
            'make_change_in_search':1,
            'filter_on':1,
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'make_change_in_search':1,
            'filter_on':1,
        },
  ]  
    
}
      


