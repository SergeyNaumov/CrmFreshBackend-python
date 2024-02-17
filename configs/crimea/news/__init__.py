"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
form={
    'work_table':'news',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Новости',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'news','a':'wt'},
        {'t':'snt','a':'snt', 'l':'wt.snt_id=snt.id'},
    ],
    'fields': [ 
            {
            'description':'СНТ',
            'type':'select_from_table',
            'name':'snt_id',
            'table':'snt',
            'header_field':'header',
            'value_field':'id',
            'tablename':'snt',
            'regexp_rules':[
                '/^[1-9][0-9]*$/','Поле, обязательное для заполнения'
            ],
            'filter_on':True
        },
        {
            'description':'Заголовок новости',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        # {
        #     'description':'Большое фото',
        #     'name':'photo',
        #     'type':'file',
        #     'filedir':'',
        # },
        {
            'description':'Фото для списка',
            'name':'photo2',
            'type':'file',
            'filedir':'',
            'preview':'352x280',
            'resize':[
                {
                    'description':'Для спика новостей',
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'352x280',
                    'quality':'100'
                },
            ]
        },
        {
            'description':'Краткое описание новости',
            'type':'textarea',
            'name':'anons',
            'filter_on':True
        },
        {
            'description':'Подробное описание новости',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':True
        },
        {
            'description':'Дата и время публикации',
            'type':'date',
            'name':'registered',
            'read_only':1,
            'filter_on':True
        },

  ]  
    
}
      


