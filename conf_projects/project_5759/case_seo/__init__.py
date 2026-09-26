"""
CREATE TABLE `struct_5759_case_seo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `header` varchar(200) NOT NULL DEFAULT '',
  `logo` varchar(20) NOT NULL DEFAULT '0',
  `type` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'тип блока: 1-горизонтальный, 2-вертикальный',
  `anons` varchar(512) NOT NULL DEFAULT '',
  `tbl` text,
  `photo_graph` varchar(20) NOT NULL DEFAULT '' COMMENT 'фото графика',
  `registered` date DEFAULT NULL,
  `tbl2` text COMMENT 'таблица2 (запросы)',
  `opportunity` varchar(50) NOT NULL DEFAULT '' COMMENT 'сфера деятельности',
  `main` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `preview_text` varchar(200) NOT NULL DEFAULT '',
  `photo1` varchar(20) NOT NULL DEFAULT '',
  `photo2` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

"""
form={
    'work_table':'struct_5759_case_seo',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы SEO',
    
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
            'description':'Сфера деятельности',
            'type':'text',
            'name':'opportunity',
        },
        {
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case_seo',
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
            'filedir':'./files/project_5759/case_seo/mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'313x157', 'quality':'100'} ]
        },
        {
            'description':'Фото, отображаемое при клике на миниатюру',
            'type':'file',
            'name':'photo2',
            'filedir':'./files/project_5759/case_seo/mini2',
            #'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Текст при наведении в блоке',
            'name':'preview_text',
            'type':'text'
        },
        {
            'description':'Анонс (абзац с кратким описанием в блоке)',
            'type':'textarea',
            'name':'anons'
        },
        # 
        {
            'description':'Анонс2 (регион, старт, работы)',
            #'add_description':'регион, старт работы  и т.д.',
            'type':'wysiwyg',
            'name':'tbl',
            # 'frontend':{
            #     'buttons':[
            #         {
            #             'description':'Шаблон таблицы "регионы, старт, работы"',
            #             'ajax':'tbl1_load_template',
            #         },

            #     ]
            # }
        },

        {
            'description':'кружки: (было / стало / посещаемость выросла)',
            'type':'1_to_m',
            'name':'circles',
            'table':'struct_5759_case_seo_circles',
            'table_id':'id',
            'foreign_key':'case_id',
            'sort':True,
            'view_type':'list',
            'fields':[
                {
                    'description':'заголовок',
                    'name':'header',
                    'type':'text'
                },
                {
                    'description':'цвет',
                    'name':'color',
                    'subtype':'color',
                    'type':'text',
                    # Список цветов из которых можно выбрать
                    'values':[
                        {'v':'#C13D9A','d':'было'},
                        {'v':'#9cac12','d':'стало'},
                        {'v':'#36a3e9','d':'итог'},
                        
                    ]
                },
                {
                    'description':'значение',
                    'name':'value',
                    'type':'text'
                },
            ]

        },



        {
            'description':'Фото графика',
            'type':'file',
            'name':'photo_graph',
            'filedir':'./files/project_5759/case_seo/graph',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'1371x0', 'quality':'90'} ]
        },
        {
            'description':'Таблица2, выводимая в блоке "кейсы"',
            'add_description':'поисковые запросы',
            'type':'wysiwyg',
            'name':'tbl2',
            # 'frontend':{
            #     'buttons':[
            #         {
            #             'description':'шаблон таблицы "кейсы"',
            #             'ajax':'tbl2_load_template',
            #         },
            #     ]
            # }
        },
        {
            'description':'Порядок сортировки',
            'name':'sort',
            'make_change_in_search':True,
            'type':'text'
        },
        {
            'description':'Тип блока',
            'name':'type',
            'type':'select_values',
            'values':[
                {'v':1,'d':'горизонтальный'},
                {'v':2,'d':'вертикальный'},
            ]
        },
        {
            'description':'Выводить на главной странице',
            'type':'checkbox',
            'name':'main',
            'make_change_in_search':True
        },

    ]
}
      


