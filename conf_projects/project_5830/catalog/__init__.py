form={
    'work_table':'struct_5830_catalog', # заполняется в events,
    'work_table_id':'id',
    'title':'Каталог товаров',
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
        {'description':'title','type':'textarea','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},


        #{'description':'promo текст','type':'textarea','name':'promo_body','tab':'promo'},
        {
            'description':'Наименование рубрики в списке каталога' ,
            'type':'text',
            'name':'header',
            'tab':'main',
        },
        {
            'description':'Наименование рубрики в меню' ,
            'type':'text',
            'name':'header_menu',
            'tab':'main',
        },
        {
            'description':'Подзаголовок в списке рубрики',
            'type':'text',
            'name':'subheader',
            'tab':'main',
        },
        {
            'description':'Заголовок на странице ',
            'name':'h1',
            'type':'text',
            'tab':'main',
        },
        {
            'description':'Тип отображения',
            'name':'type',
            'type':'select_values',
            'values':[
                {'v':'1','d':'с вендорами, лого горизонтальный'}, # https://arm-it.ru/active-telecomm.html | http://armit-new.design-b2b.com/catalog/5
                {'v':'2','d':'с вендорами, лого вертикальный'}, # https://arm-it.ru/server.html | http://armit-new.design-b2b.com/catalog/2
                {'v':'3','d':'список рубрик с вкладками'}, # https://arm-it.ru/control-system.html |  http://armit-new.design-b2b.com/catalog/14
                {'v':'4','d':'список рубрик с плиткой'}, # https://arm-it.ru/devices.html | http://armit-new.design-b2b.com/catalog/53
                {'v':'5','d':'список товаров с якорями'}, # https://arm-it.ru/product/server/hewlett-packard.html
                {'v':'6','d':'только описание'}, # https://arm-it.ru/product/server/hewlett-packard.html,
                {'v':'7','d':'горизонтальный список товаров с анонсом'}, # https://arm-it.ru/product/newland/newland.html
                
            ],
            'tab':'main',
        },

        {
            'description':'Вендоры',
            'type':'1_to_m',
            'name':'vendors',
            'table':'struct_5830_catalog_vendor',
            'table_id':'id',
            'foreign_key':'catalog_id',
            'sort':1,
            'name':'vendors',
            'fields':[
                {
                    'description':'Вендор',
                    'type':'select_from_table',
                    'name':'vendor_id',
                    'table':'struct_5830_vendor',
                    'header_field':'header',
                    'value_fiel':'id',
                    'order':'header'
                }
            ],
            'tab':'main',
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
            'filedir':'./files/project_5830/catalog/promo',

            'tab':'main'
            
        },
        {
            'description':'Фото рубрики',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5830/catalog',
            'tab':'main'
            
        },
        {
            'description':'Рубрика под промо',
            'type':'checkbox',
            'name':'rub_top',
            'tab':'main'
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'tab':'main'
        },
        {
            'description':'На главную',
            'name':'top',
            'type':'checkbox',
            'tab':'main'
        },        
        {
            'description':'Табы рубрики',
            'name':'tabs',
            'type':'1_to_m',
            'table':'struct_5830_catalog_tabs',
            'table_id':'id',
            'foreign_key':'catalog_id',
            'sort':1,
            'fields':[
                {'description':'фото','name':'photo','type':'file','filedir':'./files/project_5830/catalog'},
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
        {
            'description':'Текст под названием рубрики',
            'name':'body_after_header',
            'type':'wysiwyg',
            'tab':'desc',
            'style':['/templates/2026/arm-it/assets/fonts/font-awesome/font-awesome.min.css']
        },
        {
            'description':'Описание рубрики',
            'name':'body',
            'type':'wysiwyg',
            'tab':'desc',
            'style':['/templates/2026/arm-it/assets/fonts/font-awesome/font-awesome.min.css']
        },

  ]  
    
}
      


