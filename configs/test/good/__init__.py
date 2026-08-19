form={
    'work_table':'struct_5830_good', # заполняется в events,
    'work_table_id':'id',
    'title':'Список товаров',
    'sort':False,
    'tree_use':False,
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
            {'description': 'Фотогалерея','name':'gal','hide':False},
            {'description': 'Описание','name':'desc','hide':False},
         ]
    ],
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5830_good','alias':'wt'},
        {'t':'struct_5830_catalog','alias':'c','link':'wt.catalog_id=c.id','lj':1},
        {'t':'struct_5830_vendor','alias':'v','link':'wt.vendor_id=v.id','lj':1},
    ],
    'fields': [ 
        {'description':'title','type':'textarea','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},
      
        {
            'description':'Наименование товара' ,
            'type':'text',
            'name':'header',
            'tab':'main',
            'filter_on':1,
        },
        {
            'description':'Рубрика' ,
            'name':'catalog_id',
            'type':'select_from_table',
            'table':'struct_5830_catalog',
            'header_field':'header',
            'value_field':'id',
            'tree_use':1,
            'tablename':'c',
            'filter_on':1,
            'tab':'main',
        },
        {
            'description':'Вендор',
            'name':'vendor_id',
            'type':'select_from_table',
            'table':'struct_5830_vendor',
            'tablename':'v',
            'header_field':'header',
            'value_field':'id',
            'tab':'main'
        },
        {
            'description':'Тип отображения',
            'name':'type',
            'type':'select_values',
            'values':[
                {'v':'1','d':'с вкладками'},
                {'v':'2','d':'без вкладок'},
                {'v':'3','d':'с фотогалереей'},
            ],
            'tab':'main'
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'tab':'main'
        },
        {
            'description':'Новинка',
            'type':'checkbox',
            'name':'new',
            'tab':'main'
        },

        {
            'description':'Спецпредложение',
            'name':'spec',
            'type':'checkbox',
            'tab':'main'
        },
        {
            'description':'Акция',
            'name':'action',
            'type':'checkbox',
            'tab':'main'
        },
        {
            'description':'Фотогалерея',
            'name':'gal',
            'type':'1_to_m',
            'table':'struct_5830_good_galery',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'название фото',
                    'name':'header',
                    'type':'text'
                },
                {
                    'description':'название фото',
                    'name':'photo',
                    'filedir':'./files/project_5830/good/galery',
                    'type':'file'
                },
            ],
            'tab':'gal'
        },
        {
            'description':'Вкл',
            'type':'enabled',
            'name':'checkbox',
            'tab':'main'
        },
        {
            'description':'Анонс (в списке товаров)',
            'type':'wysiwyg',
            'name':'anons',
            'tab':'desc',
        },

        {
            'description':'Описание',
            'name':'body',
            'type':'wysiwyg',
            'tab':'desc',
        },
        {
            'description':'Тип промо-блока',
            'type':'select_values',
            'name':'type_promo',
            'values':[
                {'v':1,'d':'без промо'},
                {'v':2,'d':'в виде фона'},
                {'v':3,'d':'с голубой плашкой'}
            ],
            'tab':'main',
        },
        {


            'description':'Фото в промоблоке',
            'name':'photo_promo',
            'type':'file',
            'filedir':'./files/project_5830/good/promo',
            'tab':'desc'
            
        },

        # Блок 1
        {
            'description':'Название блока1',
            'name':'header1',
            'type':'text',
            'tab':'desc'
        },
        {
            'description':'Фото блока1',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5830/good',
            'preview':'0x250',
            'resize':[
                { # список товаров
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'0x250',
                    'quality':'100'
                },
            ],
            'tab':'desc'
        },
        {
            'description':'Вкладки блока1',
            'name':'block1',
            'type':'1_to_m',
            'table':'struct_5830_good_block1',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'название вкладки',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'содержимок вкладки (<p>..</p>)',
                    'type':'textarea',
                    'name':'body'
                },
            ],
            'tab':'desc',
        },


        # Блок 2
        {
            'description':'Название блока2',
            'name':'header2',
            'type':'text',
            'tab':'desc'
        },
        {
            'description':'Фото блока2',
            'type':'file',
            'name':'photo2',
            'filedir':'./files/project_5830/good',
            'tab':'desc'
        },
        {
            'description':'Вкладки блока2',
            'name':'block2',
            'type':'1_to_m',
            'table':'struct_5830_good_block2',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'название вкладки',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'содержимок вкладки (<p>..</p>)',
                    'type':'textarea',
                    'name':'body'
                },
            ],
            'tab':'desc',
        },        

        # Блок 3
        {
            'description':'Название блока3',
            'name':'header3',
            'type':'text',
            'tab':'desc'
        },
        {
            'description':'Фото блока3',
            'type':'file',
            'name':'photo3',
            'filedir':'./files/project_5830/good',
            'tab':'desc'
        },
        {
            'description':'Вкладки блока3',
            'name':'block3',
            'type':'1_to_m',
            'table':'struct_5830_good_block3',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'название вкладки',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'содержимок вкладки (<p>..</p>)',
                    'type':'textarea',
                    'name':'body'
                },
            ],
            'tab':'desc',
        },

        # Блок 4
        {
            'description':'Название блока4',
            'name':'header4',
            'type':'text',
            'tab':'desc'
        },
        {
            'description':'Фото блока4',
            'type':'file',
            'name':'photo4',
            'filedir':'./files/project_5830/good',
            'tab':'desc'
        },
        {
            'description':'Вкладки блока4',
            'name':'block4',
            'type':'1_to_m',
            'table':'struct_5830_good_block4',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'название вкладки',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'содержимок вкладки (<p>..</p>)',
                    'type':'textarea',
                    'name':'body'
                },
            ],
            'tab':'desc',
        },

  ]  
    
}
      


