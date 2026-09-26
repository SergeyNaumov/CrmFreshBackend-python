
form={
    'work_table':'struct_5759_solution',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Готовые решения',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':True,
    'fields': [ 
        {
            'description':'Якорь',
            'add_description':'например: #landing',
            'type':'text',
            'name':'anchor_name',
        },
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
        },

        {
            'description':'Фото видов сайта',
            'type':'1_to_m',
            'name':'gallery',
            'table':'struct_5759_solution_galery',
            'table_id':'id',
            'foreign_key':'solution_id',
            'view_type':'list',
            'sort':True,
            'fields':[
                {
                    'description':'Подзаголовок вида сайта',
                    'type':'text',
                    'name':'header',
                },
                {
                    'description':'Фото',
                    'type':'file',
                    'name':'photo',
                    'filedir':'./files/project_5759/solutions/photo_galery',
                    'preview':'494x431',
                    'resize':[
                            {
                                'description':'Фото1',
                                'file':'<%filename_without_ext%>_mini1.<%ext%>',
                                'size':'494x431',
                                'quality':'100'
                            },
                    ]
                },
                {
                    'description':'Цена',
                    'type':'text',
                    'name':'price',
                },
                {
                    'description':'Ссылка на демо-версию',
                    'type':'text',
                    'name':'link',
                },                

            ]
        },
        {
            'description':'Текстовый блок под видами сайта',
            'type':'wysiwyg',
            'name':'body',
        },
        {
            'description':'Блоки описания',
            'type':'wysiwyg',
            'name':'body2',
        },
        {
            'description':'Ссылка на руководство пользователя',
            'type':'text',
            'name':'manual_link',
        },
        {
            'description':'Ссылка на демо',
            'type':'text',
            'name':'demo_link',
        },
        {
            'description':'Расширенная версия',
            'type':'wysiwyg',
            'name':'extend_version',
        },
        {
            'description':'Кому подойдёт?',
            'type':'wysiwyg',
            'name':'why_will_suit',
        },
  ]  
    
}
      


