"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
form={
    'work_table':'test',
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
        {'t':'test','a':'wt'},
    ],
    'explain':0,
    'fields': [ 

        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
            'make_change_in_search':True,
            'filter_on':True

        },
        {
            'description':'Время',
            'type':'time',
            'name':'f_time',
            'make_change_in_search':True,
            'filter_on':True
        },
        {
            'description':'День и месяц',
            'type':'daymon',
            'name':'daymon',
            'make_change_in_search':True,
            #'filter_on':True
        },
        # {
        #     'description':'Большое фото',
        #     'name':'photo',
        #     'type':'file',
        #     'filedir':'',
        #     'cropper':True,
        #     'resize':[
        #         {
        #             'description':'Для спика новостей',
        #             'file':'<%filename_without_ext%>_mini1.<%ext%>',
        #             'size':'1120x450',
        #             'quality':'100'
        #         },
        #     ]
        # },
        {
            'description':'Фото для списка',
            'name':'photo',
            'type':'file',
            'filedir':'',
            'preview':'352x280',
            'cropper':True,
            'resize':[
                {
                    'description':'Для спика новостей',
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'352x280',
                    'quality':'100'
                },
                {
                    'description':'Большое фото',
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'1120x450',
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
            'filter_on':False
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
      


