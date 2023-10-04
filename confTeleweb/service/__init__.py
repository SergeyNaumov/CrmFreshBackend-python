form={
    'work_table':'service',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Услуги',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'service','a':'wt'},
        {'t':'service_catalog','a':'c','l':'wt.catalog_id=c.id','lj':1},
    ],
    'search_on_load':1,
    'fields': [ 

        {
            'description':'Название',
            'type':'text',
            'name':'header',
            'regexp_rules':[
                '/^.+$/','Укажите наименование услуги',
            ],
            'filter_on':True
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'filter_on':False
        },
        {
            'description':'Рубрика каталога',
            'type':'select_from_table',
            'table':'service_catalog',
            'name':'catalog_id',
            'header_field':'header',
            'tablename':'c',
            'value_field':'id',
            'filter_on':True
        },
        {
            'description':'Артикул',
            'type':'text',
            'name':'artikul',
            'filter_on':True
        },
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
            'table':'service_photos',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'view_type':'list',
            'fields':[
                {
                    'description':'Название фото',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'Основное фото',
                    'type':'checkbox',
                    'name':'main'
                },
                {
                    'description':'Фото',
                    'type':'file',
                    'name':'photo',
                    'preview':'48x48',
                    'filedir':'./files/project_3/service_photos',
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
            'filter_on':False
        },

  ]  
    
}
      


