form={
    'work_table':'good',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Товары',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'good','a':'wt'},
        {'t':'catalog','a':'c','l':'wt.catalog_id=c.id','lj':1},
    ],
    'search_on_load':1,
    'fields': [ 

        {
            'description':'Название',
            'type':'text',
            'name':'header',
            'regexp_rules':[
                '/^.+$/','Укажите наименование товара',
            ],
            'filter_on':True
        },
        {
            'description':'Опубликовать',
            'type':'checkbox',
            'name':'enabled',
            'filter_on':False
        },
        {
            'description':'Рубрика каталога',
            'type':'select_from_table',
            'table':'catalog',
            'name':'catalog_id',
            'header_field':'header',
            'tablename':'c',
            'value_field':'id',
            'filter_on':True
        },
        # {
        #     'description':'Артикул',
        #     'type':'text',
        #     'name':'artikul',
        #     'filter_on':True
        # },
        # Положение важно, используется в events

        {
            'description':'Код производителя',
            'type':'text',
            'name':'vendor_code',
            'filter_on':True
        },
        {
            'description':'Цена',
            'type':'text',
            'name':'price',
            'value':0,
            'regexp_rules':[
                '/^\d+(\.\d+)?$/','Укажите цену',
            ],
            'replace_rules':[
                '/[^\d.,]/g','',
                '/,/','.',
            ],

            'filter_on':True
        },        

        {
            'description':'Анонс',
            'type':'textarea',
            'name':'anons',
            'filter_on':True
        },
        {
            'description':'Фотографии',
            'name':'photos',
            'type':'1_to_m',
            'table':'good_photos',
            'table_id':'id',
            'foreign_key':'good_id',
            'view_type':'list',
            'sort':1,
            'fields':[
                {
                    'description':'Название фото',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'Фото',
                    'type':'file',
                    'name':'photo',
                    'preview':'48x48',
                    'filedir':'./files/project_3/good_photos',
                    'resize':[
                        {
                            'description':'Для спика товаров',
                            'file':'<%filename_without_ext%>_mini1.<%ext%>',
                            'size':'48x48',
                            'quality':'90'
                        },
                        {
                            'description':'Для карточек товара',
                            'file':'<%filename_without_ext%>_mini2.<%ext%>',
                            'size':'476x585',
                            'quality':'90'
                        },
                    ]
                },
                {
                    'description':'Основное фото',
                    'type':'checkbox',
                    'name':'main'
                },
                {
                    'description':'Источник (если фото из yml)',
                    'type':'textarea',
                    'name':'src_url'
                },
            ]

        },
        {
            'description':'Подробное описание',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':False,
            'plugins':[
                {'type':'GPTAssist', 'set_value_button':'Отправить в описание'}
            ]
        },

  ]  
    
}
      


