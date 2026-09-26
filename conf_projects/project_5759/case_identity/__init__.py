#from .fields import get_fields
form={
    'work_table':'struct_5759_case_identity',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы айдентика',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 

        {
            'description':'Название компании',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Подзаголовок',
            'type':'text',
            'name':'header2',
        },
        {
            'description':'Сфера деятельности',
            'type':'text',
            'name':'opportunity',
        },
        {
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case_identity',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       #'size':'340x264',
                       'size':'264x0',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото при наведении на лого',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_identity/mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'313x157', 'quality':'100'} ]
        },
        {
            'description':'Текст при наведении в блоке',
            'name':'preview_text',
            'type':'text'
        },
        {
            'description':'Анонс (абзац с кратким описанием в блоке)',
            'type':'wysiwyg',
            'name':'anons'
        },
        {
            'description':'Фото, отображаемое при клике на миниатюру',
            'type':'file',
            'name':'photo2',
            'filedir':'./files/project_5759/case_identity/mini2',
            #'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'gallery',
            'table':'struct_5759_case_identity_gallery',
            'table_id':'id',
            'foreign_key':'parent_id',
            'sort':True,
            'fields':[
                {
                    'description':'Название фото',
                    'type':'text',
                    'name':'header',
                },
                {
                    'description':'Фото',
                    'type':'file',
                    'name':'photo',
                    'filedir':'./files/project_5759/case_sites/photo_galery',
                    'resize':[
                            {
                                'description':'Фото1',
                                'file':'<%filename_without_ext%>_mini1.<%ext%>',
                                'size':'388x183',
                                'quality':'100'
                            },
                            {
                                'description':'Фото2',
                                'file':'<%filename_without_ext%>_mini2.<%ext%>',
                                'size':'1000x0',
                                'quality':'90'
                            },
                    ]
                },
            ]
        },
        {
            'description':'Порядок сортировки',
            'name':'sort',
            'make_change_in_search':True,
            'type':'text'
        },
        {
            'description':'Выводить на главной странице',
            'type':'checkbox',
            'name':'main',
            'make_change_in_search':True
        }



    ]
}
      


