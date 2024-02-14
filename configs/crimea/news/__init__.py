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
                '^\d+$','Поле, обязательное для заполнения'
            ],
            'filter_on':True
        },
        {
            'description':'Заголовок новости',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Краткое описание новости',
            'type':'text',
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
      


