"""
create table struct_5794_content_photos(
id int unsigned primary key auto_increment,
header varchar(100) not null default '',
photo varchar(20) not null default '',
sort tinyint unsigned not null default '0',
content_id int unsigned,
constraint foreign key(content_id) references struct_5794_content(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;
"""
form={
    'work_table':'struct_5794_content',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Статичные страницы',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'cols':[
        [
            {'description': 'SEO','name':'promo','hide':True},
            {'description': 'Основное','name':'main','hide':False},

        ],
    ],
    'fields': [
        {'description':'title','type':'text','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},
        {'description':'h1','type':'textarea','name':'h1','tab':'promo'},
        {
            'description':'Название',
            'type':'text',
            'name':'header',
            'tab':'main',
            'filter_on':True
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'tab':'main',
            'filter_on':True
        },

        {
            'description':'Фото',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5794/content',
            'preview':'379x295',
            'resize':[
                { # 1-3 фото в списке услуг на главной странице и странице списка услуг
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'379x295',
                    'quality':'100'
                },
            ],
            'tab':'main'
        },
        {
            'description':'Фотогалерея',
            'name':'gal',
            'type':'1_to_m',
            'table':'struct_5794_content_photos',
            'table_id':'id',
            'foreign_key':'content_id',
            'sort':1,
            'fields':[
                {
                    'description':'название фото',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'фото',
                    'type':'file',
                    'name':'photo',
                    'filedir':'./files/project_5794/content',
                    'preview':'379x295',
                    'resize':[
                        { # 1-3 фото в списке услуг на главной странице и странице списка услуг
                            'file':'<%filename_without_ext%>_mini1.<%ext%>',
                            'size':'379x295',
                            'quality':'100'
                        },
                    ],
                }
            ],
            'tab':'main'
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'name':'body',
            'tab':'main',
            'edit_mode':True,
            'filter_on':True
        },
  ]  
    
}
      


