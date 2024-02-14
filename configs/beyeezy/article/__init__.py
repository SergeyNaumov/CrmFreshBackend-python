"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
form={
    'work_table':'article',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Статьи',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'fields': [ 
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'filter_on':True
        },
        {
            'description':'promo title',
            'type':'text',
            'name':'promo_title',
            'filter_on':False
        },
        {
            'description':'promo description',
            'type':'textarea',
            'name':'promo_description',
            'filter_on':False
        },
        {
            'description':'promo keywords',
            'type':'textarea',
            'name':'promo_keywords',
            'filter_on':False
        },
        {
            'description':'Название страницы',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Фото',
            'name':'photo',
            'type':'file',
            'filedir':'files/article'
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'photos',
            'table':'article_photo',
            'table_id':'id',
            'foreign_key':'article_id',
            'sort':True,
            'fields':[
                {
                    'description':'Название фото',
                    'type':'text',
                    'name':'header',
                    'filter_on':True
                },
                {
                    'description':'Фото',
                    'name':'photo',
                    'type':'file',
                    'filedir':'./files/article',
                },
            ]
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':False
        },
  ]  
    
}
      


