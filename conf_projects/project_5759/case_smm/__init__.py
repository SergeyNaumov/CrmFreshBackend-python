#from .fields import get_fields
# alter table struct_5759_case_smm change url url_resource varchar(255) not null default '';
form={
    'work_table':'struct_5759_case_smm',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы SMM' ,
    
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
            'description':'Отрасль',
            'type':'text',
            'name':'otr_name',
        },
        {
            'description':'Сфера деятельности',
            'type':'text',
            'name':'opportunity',
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url_resourse',
        },
        {
            'description':'Регион',
            'type':'text',
            'name':'region',
        },
        {
            'description':'Информация о компании',
            'type':'textarea',
            'name':'comp_info',
        },
        {
            'description':'Целевая аудитория',
            'type':'textarea',
            'name':'audience',
        },
        {
            'description':'Задачи',
            'type':'textarea',
            'name':'tasks',
        },
        {
            'description':'Платформы',
            'type':'wysiwyg',
            'name':'platforms',
        },
        {
            'description':'Работы',
            'type':'textarea',
            'name':'works',
        },
        {
            'description':'Результаты',
            'type':'wysiwyg',
            'name':'results',
        },
        {
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case_smm',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       #'size':'340x264',
                       'size':'264x0',
                       'quality':'90'
                       },
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini2.<%ext%>',
                       'size':'135x0',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото при наведении на лого',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_smm/mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'313x157', 'quality':'100'} ]
        },
        # {
        #     'description':'Фото, отображаемое при клике на миниатюру',
        #     'type':'file',
        #     'name':'photo2',
        #     'filedir':'./files/project_5759/case_smm/mini2',
        #     #'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        # },
        {
            'description':'Текст при наведении в блоке',
            'name':'preview_text',
            'type':'text'
        },
        # {
        #     'description':'Анонс (абзац с кратким описанием в блоке)',
        #     'type':'textarea',
        #     'name':'anons'
        # },
        # { # Убрал (оказывается, в кейсах этого не нужно)
        #     'description':'Анонс2 (регион, старт, работы)',
        #     'type':'wysiwyg',
        #     'name':'tbl',
        #     # 'frontend':{
        #     #     'buttons':[
        #     #         {
        #     #             'description':'Шаблон таблицы "регионы, старт, работы"',
        #     #             'ajax':'tbl1_load_template',
        #     #         },

        #     #     ]
        #     # }
        # },
        # { # Убрал (оказывается, в кейсах свой набор)
        #     'description':'кружки: (было / стало / посещаемость выросла)',
        #     'type':'1_to_m',
        #     'name':'circles',
        #     'table':'struct_5759_case_smm_circles',
        #     'table_id':'id',
        #     'foreign_key':'case_id',
        #     'sort':True,
        #     'view_type':'list',
        #     'fields':[
        #         {
        #             'description':'заголовок',
        #             'name':'header',
        #             'type':'text'
        #         },
        #         {
        #             'description':'цвет',
        #             'name':'color',
        #             'subtype':'color',
        #             'type':'text',
        #             # Список цветов из которых можно выбрать
        #             'values':[
        #                 {'v':'#C13D9A','d':'было'},
        #                 {'v':'#9cac12','d':'стало'},
        #                 {'v':'#36a3e9','d':'итог'},
                        
        #             ]
        #         },
        #         {
        #             'description':'значение',
        #             'name':'value',
        #             'type':'text'
        #         },
        #     ]

        # },
        # {
        #     'description':'Фото графика',
        #     'type':'file',
        #     'name':'photo_graph',
        #     'filedir':'./files/project_5759/case_seo/graph',
        #     'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'1371x0', 'quality':'90'} ]
        # },
        # {
        #     'description':'Таблица2, выводимая в блоке "кейсы"',
        #     'add_description':'поисковые запросы',
        #     'type':'wysiwyg',
        #     'name':'tbl2',
        #     # 'frontend':{
        #     #     'buttons':[
        #     #         {
        #     #             'description':'шаблон таблицы "кейсы"',
        #     #             'ajax':'tbl2_load_template',
        #     #         },
        #     #     ]
        #     # }
        # },
        {
            'description':'Порядок сортировки',
            'name':'sort',
            'make_change_in_search':True,
            'type':'text'
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'gallery',
            'table':'struct_5759_case_smm_gallery',
            'table_id':'id',
            'foreign_key':'parent_id',
            'view_type':'list',
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
                    'filedir':'./files/project_5759/case_smm/photo_galery',
                    'preview':'295x0',
                    'resize':[
                            {
                                'description':'Фото1',
                                'file':'<%filename_without_ext%>_mini1.<%ext%>',
                                'size':'295x0',
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
            'description':'Описание проекта под галереей',
            'type':'wysiwyg',
            'name':'wysiwyg_after_content'
        },
        # {
        #     'description':'Тип блока',
        #     'name':'type',
        #     'type':'select_values',
        #     'values':[
        #         {'v':1,'d':'горизонтальный'},
        #         {'v':2,'d':'вертикальный'},
        #     ]
        # },
        {
            'description':'Выводить на главной странице',
            'type':'checkbox',
            'name':'main',
            'make_change_in_search':True
        },




    ]
}
      


