form={
    'work_table':'struct_5794_rubricator', # заполняется в events,
    'work_table_id':'id',
    'title':'Рубрики товаров',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    #'max_level':2,
    'wide_form':True,
    'cols':[
        [
            {'description': 'SEO','name':'promo','hide':True},
            {'description': 'Основное','name':'main','hide':False},

        ],
        [
            {'description': 'Описание','name':'desc','hide':False},
        ]

    ],
    'fields': [ 
        {'description':'title','type':'text','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},
        {'description':'promo текст','type':'textarea','name':'promo_body','tab':'promo'},
        {'description':'h1','type':'textarea','name':'h1','tab':'promo'},
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
            'tab':'main',
        },
        {
            'description':'url',
            'name':'url',
            'type':'text',
            'tab':'main',
        },
        {
            'description':'Фото на главной',
            'name':'photo_main',
            'type':'file',
            'filedir':'./files/project_[project_id]/rubricator',
            'preview':'240x332',
            'resize':[
                { # список товаров
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'240x332',
                    'quality':'100'
                },
            ],
            'tab':'main'
        },
        {
            'description':'Фото на странице каталога',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_[project_id]/rubricator',
            'preview':'609x341',
            'resize':[
                { # список товаров
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'609x341',
                    'quality':'100'
                },
            ],
            'tab':'main'
        },
        {
            'description':'Фото для меню',
            'name':'photo_menu',
            'type':'file',
            'filedir':'./files/project_[project_id]/rubricator',
            'preview':'62x48',
            'resize':[
                { # список товаров
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'62x48',
                    'quality':'100'
                },
            ],
            'tab':'main'
        },
        {
            'description':'Иконка для каталога и сайдбара',
            'name':'photo_sidebar',
            'type':'file',
            'filedir':'./files/project_[project_id]/rubricator',
            'tab':'main'
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'body',
            'tab':'desc',
            'edit_mode':1
        },
        {
            'description':'Технические характеристики',
            'type':'wysiwyg',
            'name':'tech',
            'tab':'desc',
            'edit_mode':1
        },
        {
            'description':'Вкл',
            'type':'enabled',
            'name':'checkbox',
            'tab':'desc',
        },
  ]  
    
}
      


