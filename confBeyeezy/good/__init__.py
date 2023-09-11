form={
    'work_table':'good',
    'work_table_id':'id',

    'title':'Товары',
    'sort':False,
    'tree_use':False,
    #'explain':1,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'good','a':'wt'},
        {'t':'category','a':'c','l':'c.id=wt.category_id','lj':1,},
    ],
    'fields': [ 
        {
            'description':'Название',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Категория',
            'type':'select_from_table',
            'table':'category',
            'name':'category_id',
            'tablename':'c',
            'header_field':'header',
            'value_field':'id',
            'filter_on':True
        },
        {
            'description':'Артикул',
            'type':'text',
            'name':'artikul',
            'filter_on':True
        },
        {
            'description':'Цена',
            'type':'text',
            'name':'price',
            'filter_on':True
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'photos',
            'table':'good_galery',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,

            'fields':[
                {
                    'description':'Фото',
                    'preview':1,
                    'type':'file',
                    'name':'photo',
                    'filedir':'/files/good_galery'

                }
            ],
            'filter_on':False
        },
        {
            'description':'Параметры',
            'type':'1_to_m',
            'name':'params',
            'table':'good_param',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'параметр',
                    'type':'text',
                    'name':'header',
                },
                {
                    'description':'Значение',
                    'type':'text',
                    'name':'value',
                },
            ],
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'description',
            'filter_on':False
        },

  ]  
    
}
      


