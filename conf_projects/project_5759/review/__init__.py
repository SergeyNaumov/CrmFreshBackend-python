#from .fields import get_fields
form={
    'work_table':'struct_5759_review',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Отзывы',
    'search_on_load':1,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Название компании',
            'type':'text',
            'name':'header',
            'filter_on':1
        },
        {
            'description':'Фото',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5759/review',
            'preview':'350x490',
            'add_description':'1920x0',
            #'crops':True,
            'resize':[
                {
                    'description':'Для главной и внутренней страниц',
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'350x490',
                    'quality':'90'
                },
                {
                    'description':'Для лайтбоксов',
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'800x0',
                    'quality':'90'
                },
            ]
        },
        {
            'description':'Дата',
            'type':'date',
            'name':'dat',
            'make_change_in_search':1,
            'filter_on':1
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'make_change_in_search':1,
            'filter_on':1
        },
  ]  
    
}
      


