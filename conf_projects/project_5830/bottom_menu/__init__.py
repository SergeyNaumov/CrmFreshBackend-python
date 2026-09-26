form={
    'work_table':'struct_5830_bottom_menu', # заполняется в events,
    'work_table_id':'id',
    'title':'Каталог товаров',
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
            'type':'text',
            'name':'header',
            #'tab':'main',
        },
        {
            'description':'Анонс',
            'type':'text',
            'name':'anons',
            #'tab':'main',
        },
        {
            'description':'Иконка (fa)',
            'name':'icon',
            'type':'text'
        },
        {
            'description':'url',
            'name':'url',
            'type':'text'
        },

  ]

}



