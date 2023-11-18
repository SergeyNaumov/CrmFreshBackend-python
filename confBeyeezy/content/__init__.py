"""
create table content(
id int unsigned primary key auto_increment,
url varchar(255) not null default '',
body text,
unique key(url)
) engine=innodb default charset=utf8;
"""
form={
    'work_table':'content',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Текстовые страницы',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'fields': [ 
        {
            'description':'promo title',
            'type':'text',
            'name':'promo_title',
            'filter_on':True
        },
        {
            'description':'promo description',
            'type':'textarea',
            'name':'promo_description',
            'filter_on':True
        },
        {
            'description':'promo keywords',
            'type':'textarea',
            'name':'promo_keywords',
            'filter_on':True
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'filter_on':True
        },
        {
            'description':'Название страницы',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':False
        },
  ]  
    
}
      


