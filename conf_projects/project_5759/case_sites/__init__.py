#from .fields import get_fields
"""
create table struct_5759_case_sites(
    id int unsigned primary key auto_increment,
    header varchar(200) comment 'название кейса',
    company varchar(200) not null default '' comment 'название компании',
    logo varchar(20) not null default '0',
    anons varchar(512) not null default '',
    opportunity int unsigned not null default '0',
    photo_pk varchar(20),
    photo_mobile varchar(20),
    registered date
) engine=innodb default charset=utf8;

create table struct_5759_case_sites_gallery(
    id int unsigned primary key auto_increment,
    parent_id int unsigned,
    sort tinyint unsigned not null default '0',
    header varchar(20) not null default '',
    photo varchar(20) not null default ''
) engine=innodb default charset=utf8 comment 'фотогалерея в карточке "кейсы - создание сайтов"';
# Основное фото:

"""
form={
    'work_table':'struct_5759_case_sites',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы "Создание сайтов"',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        # {
        #     'description':'Название кейса',
        #     'type':'text',
        #     'name':'header',
        # },
        {
            'description':'Название компании',
            'type':'text',
            'filter_on':1,
            'name':'header',
        },
        {
            'description':'Сфера деятельности',
            'type':'text',
            'filter_on':1,
            'name':'opportunity',
        },
        # {
        #     'description':'Сфера деятельности',
        #     'type':'select_from_table',
        #     'name':'opportunity',
        #     'table':'struct_5759_opportunity',
        #     'header_field':'header',
        #     'value_field':'id'
        # },
        # {
        #     'description':'Логотип',
        #     'type':'file',
        #     'name':'logo',
        #     'filedir':'./files/project_5759/case_sites',
        #     'resize':[
        #                {
        #                'description':'Горизонтальное фото',
        #                'file':'<%filename_without_ext%>_mini1.<%ext%>',
        #                'size':'340x264',
        #                'quality':'90'
        #                },
        #     ]
        # },
        {
            'description':'Анонс (абзац с кратким описанием в блоке)',
            'type':'wysiwyg',
            'name':'anons',
            'make_change_in_search':True
        },
        {
            'description':'Лого',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case_sites/logo',
            'resize':[ 
                {
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    #'size':'340x264',
                    'size':'264x0',
                    'quality':'100'
                },

                { 'file':'<%filename_without_ext%>_mini2.<%ext%>', 'size':'182x182', 'quality':'90'} 
            ]
        },
        {
            'description':'Фото при наведении на лого',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_sites/mini',
            'resize':[ 
                { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'313x157', 'quality':'100'} 
            ]
        },
        {
            'description':'Текст при наведении в блоке',
            'name':'preview_text',
            'type':'text'
        },
        {
            'description':'Фото, отображаемое при клике на миниатюру',
            'type':'file',
            'name':'photo2',
            'filedir':'./files/project_5759/case_sites/mini2',
            #'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        # {
        #     'description':'кружки: (было / стало / посещаемость выросла)',
        #     'type':'1_to_m',
        #     'name':'circles',
        #     'table':'struct_5759_case_sites_circles',
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
        #     'filedir':'./files/project_5759/case_sites/graph',
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
            'description':'Фото ПК',
            'type':'file',
            'name':'photo_pk',
            'filedir':'./files/project_5759/case_sites/photo_pk',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       'size':'1129x0',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото, моб.',
            'type':'file',
            'name':'photo_mobile',
            'filedir':'./files/project_5759/case_sites/photo_mobile',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       'size':'332x0',
                       'quality':'100'
                       },
            ]
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'gallery',
            'table':'struct_5759_case_sites_gallery',
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
                    'filedir':'./files/project_5759/case_sites/photo_galery',
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
        {
            'description':'Тип сайта (не используется)',
            'type':'text',
            'name':'type_site',
        },
        {
            'description':'Дизайн (не используется)',
            'type':'text',
            'name':'design',
        },
        {
            'description':'Выводить на главной странице',
            'type':'checkbox',
            'name':'main',
            'make_change_in_search':True
        }
    ]
}
      


