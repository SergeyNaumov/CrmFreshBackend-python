#from .fields import get_fields
"""
alter table struct_5759_case_rk add complexity text comment 'сложности проекта';
create table struct_5759_case_rk(
    id int unsigned primary key auto_increment,
    header varchar(200) not null default '' comment 'название компании',
    logo varchar(20) not null default '0',
    type tinyint unsigned not null default '0' comment 'тип блока: 1-горизонтальный, 2-вертикальный',
    anons varchar(512) not null default '',
    tbl text,
    photo_graph varchar(20) not null default '' comment 'фото графика',
    registered date
) engine=innodb default charset=utf8;

alter table struct_5759_case_rk add tasks text comment 'задачи'; 
alter table struct_5759_case_rk add solution text comment 'решение'; 
alter table struct_5759_case_rk add result text comment 'результат';
alter table struct_5759_case_rk add resume  text comment 'резюме';



create table struct_5759_case_rk_circles(
    id int unsigned primary key auto_increment,
    case_id int unsigned,
    sort int unsigned not null default '0',
    header varchar(100) not null default '',
    color varchar(7) not null default '0',
    value varchar(10) not null default '' comment 'значение',
    constraint foreign key(case_id) references struct_5759_case_rk(id) on update cascade on delete cascade
) engine=innodb default charset=utf8 comment 'Кружки: было / стало / посещаемость выросла';
"""
form={
    'work_table':'struct_5759_case_rk',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы РК',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    # 'cols':[
    #     [
    #         {'description': 'Основные данные', 'name':'main'},
    #         {'description':'Данные для РК','name':'rl'}
    #     ]
    # ],
    'fields': [ 
        #  Основные данные
        {
            'description':'Название компании',
            'type':'text',
            'name':'header',
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
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case_rk',

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
                       'size':'0x129',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото при наведении на лого',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_rk/mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'313x157', 'quality':'100'} ]
        },
        {
            'description':'Фото, отображаемое при клике на миниатюру',
            'type':'file',
            'name':'photo2',
            'filedir':'./files/project_5759/case_rk/mini2',
            #'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },        
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
        # {
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
        {
            'description':'Задачи',
            'type':'wysiwyg',
            'name':'tasks',
        },
        {
            'description':'Сложности проекта',
            'type':'wysiwyg',
            'name':'complexity',
        },
        {
            'description':'Решение',
            'type':'wysiwyg',
            'name':'solution',
        },
        {
            'description':'Результат',
            'type':'wysiwyg',
            'name':'result',
        },
        {
            'description':'Резюме',
            'type':'wysiwyg',
            'name':'resume',
        },
        {
            'description':'Контекст(таблица)',
            'name':'tbl3',
            'type':'wysiwyg'
        },
        # {
        #     'description':'кружки: (было / стало / посещаемость выросла)',
        #     'type':'1_to_m',
        #     'name':'circles',
        #     'table':'struct_5759_case_rk_circles',
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
        #     'filedir':'./files/project_5759/case_rk/graph',
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
            'table':'struct_5759_case_rk_gallery',
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
                    'filedir':'./files/project_5759/case_rk/photo_galery',
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
        }
        # {
        #     'description':'Услуга',
        #     'name':'service_id',
        #     'type':'select_from_table',
        #     'table':'struct_5759_service',
        #     #'tree_use':1,
        #     'header_field':'header',
        #     'value_field':'id'
        # },

        # Данные для РК


      
    ]
}
      


