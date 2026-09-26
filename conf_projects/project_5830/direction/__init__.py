form={
    'work_table':'struct_5830_direction', # заполняется в events,
    'work_table_id':'id',
    'title':'Направления деятельности',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    #'max_level':2,
    'wide_form':True,
    # 'cols':[
    #     [
    #         {'description': 'SEO','name':'promo','hide':True},
    #         {'description': 'Основное','name':'main','hide':False},

    #     ],
    #     [
    #         {'description': 'Описание','name':'desc','hide':False},
    #     ]
    # ],
    'fields': [ 

        {
            'description':'Наименование',
            'type':'textarea',
            'name':'header',
            #'tab':'main',
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            #'tab':'main',
        },
        {
            'description':'Не выводить заголовок в блоке',
            'type':'checkbox',
            'name':'not_out_header',
            'tab':'desc',
        },
        # {
        #     'description':'Рубрика каталога',
        #     'name':'catalog_id',
        #     'type':'select_from_table',
        #     'table':'struct_5830_catalog',
        #     'header_field':'header',
        #     'value_field':'id',
        #     'order':'sort',
        #     'where':'parent_id is null'
        # },
        {
            'description':'Фото для блока "направления деятельности"',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5830/catalog_direction',
            #'preview':'240x332',
            # 'resize':[
            #     { 
            #         'file':'<%filename_without_ext%>_mini1.<%ext%>',
            #         'size':'240x332',
            #         'quality':'100'
            #     },
            # ],
        },


        {
            'description':'Вкл',
            'name':'enabled',
            'type':'checkbox',
            'tab':'desc',
        },
  ]  
    
}
      


