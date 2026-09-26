"""
Apr 19 16:01:55 stg-web01.strateg uvicorn[3479531]: QUERY:
INSERT INTO struct_5794_service(header,sort,parent_id,path) VALUES ('1111', '2', '4', '/4');
Apr 19 16:01:55 stg-web01.strateg uvicorn[3479531]:

"""
form={
    'work_table':'struct_5794_service', # заполняется в events,
    'work_table_id':'id',
    'title':'Услуги',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':True,
    'cols':[
        [
            {'description': 'SEO','name':'promo','hide':False},
            {'description': 'Основное','name':'main','hide':False},
        ],
        [

            {'description': 'Описание','name':'desc','hide':False},
        ],

    ],
    'fields': [ 
        {'description':'title','type':'text','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},
        {'description':'h1','type':'textarea','name':'h1','tab':'promo'},
        #{'description':'promo текст','type':'textarea','name':'promo_body','tab':'promo'},
        {
            'description':'Название услуги',
            'type':'text',
            'name':'header',
            'tab':'main',
        },
        {
            'description':'url',
            'type':'text',
            'name':'url',
            'tab':'main',
        },
        {
            'description':'Анонс в списке услуг',
            'type':'text',
            'name':'anons',
            'tab':'main',
        },
        {
            'description':'Фото услуги',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5794/service',
            'preview':'229x351',
            'resize':[
                { # 1-3 фото в списке услуг на главной странице и странице списка услуг
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'399x351',
                    'quality':'100'
                },
                { # 4-5 фото в списке услуг на главной странице и странице списка услуг
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'612x275',
                    'quality':'100'
                },
                { # страница подробного описания услуги
                    'file':'<%filename_without_ext%>_mini3.<%ext%>',
                    'size':'440x367',
                    'quality':'100'
                },
                { # для карусели блока «Вас может заинтересовать»
                    'file':'<%filename_without_ext%>_mini4.<%ext%>',
                    'size':'390x343',
                    'quality':'100'
                },
            ],
            'tab':'main'
        },
        {
            'description':'Иконка услуги для меню',
            'name':'photo_menu',
            'type':'file',
            'filedir':'./files/project_5794/service',
            'tab':'main'
        },
        {
            'description':'Иконка услуги для сайдбара',
            'name':'photo_sidebar',
            'type':'file',
            'filedir':'./files/project_5794/service',
            'tab':'main'
        },
        # {
        #     'description':'Фото для меню',
        #     'name':'photo_menu',
        #     'type':'file',
        #     'filedir':'./files/project_[project_id]/service',
        #     'preview':'62x48',
        #     'resize':[
        #         { # список товаров
        #             'file':'<%filename_without_ext%>_mini1.<%ext%>',
        #             'size':'62x48',
        #             'quality':'100'
        #         },
        #     ],
        #     'tab':'main'
        # },
        # {
        #     'description':'Иконка для каталога и сайдбара',
        #     'name':'photo_sidebar',
        #     'type':'file',
        #     'filedir':'./files/project_5794/service',
        #     'tab':'main'
        # },
        {
            'description':'Иконка при наведении на тёмном фоне',
            'name':'photo_dark',
            'type':'file',
            'filedir':'./files/project_5794/service',
            'tab':'main'
        },
        {
            'description':'Цена от',
            'type':'text',
            'name':'price',
            'tab':'main',
        },
        {
            'description':'Анонс в карточке услуги',
            'type':'textarea',
            'name':'anons_in',
            'tab':'desc',
        },

        {'name':'tab1', 'description':'Вкладка 1', 'type':'text', 'tab':'desc'},
        {'name':'tab1_desc', 'description':'Описание вкладки 1', 'type':'wysiwyg', 'tab':'desc','edit_mode':1},
        {'name':'tab2', 'description':'Название вкладки "документы"', 'type':'text', 'tab':'desc'},
        #{'name':'tab2_desc', 'description':'Описание вкладки 2', 'type':'wysiwyg', 'tab':'desc'},
        {'name':'tab3', 'description':'Вкладка 3', 'type':'text', 'tab':'desc'},
        {'name':'tab3_desc', 'description':'Описание вкладки 3', 'type':'wysiwyg', 'tab':'desc','edit_mode':1},
        {'name':'tab4', 'description':'Вкладка 4', 'type':'text', 'tab':'desc'},
        {'name':'tab4_desc', 'description':'Описание вкладки 4', 'type':'wysiwyg', 'tab':'desc','edit_mode':1},
        {'name':'tab5', 'description':'Вкладка 5', 'type':'text', 'tab':'desc'},
        {'name':'tab5_desc', 'description':'Описание вкладки 5', 'type':'wysiwyg', 'tab':'desc','edit_mode':1},
        # {
        #     'description':'Технические характеристики',
        #     'type':'wysiwyg',
        #     'name':'tech',
        #     'tab':'desc',
        # },
        {
            'description':'Формат вывода документов',
            'type':'select_values',
            'name':'format_out',
            'values':[
                {'v':1,'d':'иконки'},
                {'v':2,'d':'фото документов'},
            ],
            'tab':'desc'
        },
        {
            'description':'Документы',
            'name':'documents',
            'type':'1_to_m',
            'table':'struct_5794_document',
            'table_id':'id',
            'foreign_key':'service_id',
            'tab':'desc',
            'fields':[
                {
                    'description':'название документа',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'Дата',
                    'type':'date',
                    'name':'registered',
                },
                {
                    'description':'Фото',
                    'type':'file',
                    'name':'photo',
                    'filedir':'./files/project_5794/document',
                    'itemtype':'list',
                    'preview':'214x293',
                    'resize':[
                        { # вертикальное фото
                            'file':'<%filename_without_ext%>_mini1.<%ext%>',
                            'size':'214x293',
                            'quality':'100'
                        },
                        { # горизонтальное фото
                            'file':'<%filename_without_ext%>_mini2.<%ext%>',
                            'size':'295x202',
                            'quality':'100'
                        },
                        { # лайтбокс
                            'file':'<%filename_without_ext%>_mini3.<%ext%>',
                            'size':'0x700',
                            'quality':'100'
                        },
                        { # вкладка "документы"
                            'file':'<%filename_without_ext%>_mini4.<%ext%>',
                            'size':'0x700',
                            'quality':'100'
                        },
                    ],
                },
                {
                    'description':'Вкл',
                    'type':'checkbox',
                    'name':'enabled',
                    'filter_on':1,
                    'make_change_in_search':True
                },
            ]
        },
        {
            'description':'Вкл',
            'name':'enabled',
            'type':'checkbox',
            'tab':'desc',
        },
  ]  
    
}
      


