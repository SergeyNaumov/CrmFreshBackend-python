"""
create table sale(
    id int unsigned primary key auto_increment,
    header varchar(255) not null default '',
    dat_from date,
    dat_to date,
    body text
) engine=innodb default charset=utf8;

alter table sale add url varchar(200) not null default '';
alter table sale add promo_title varchar(255) not null default '';
alter table sale add promo_description varchar(255) not null default '';
alter table sale add promo_keywords varchar(255) not null default '';

create table sale_photo(
    id int unsigned primary key auto_increment,
    sale_id int unsigned,
    sort tinyint unsigned not null default '0',
    header varchar(255) not null default '',
    photo varchar(255) not null default '',
    constraint foreign key(sale_id) references sale(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;

"""
from .ajax import ajax

form={
    'work_table':'sale',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Акции и распродажи',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'ajax':ajax,
    'fields': [ 
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'filter_on':True,
            'regexp_rules':[
                '/^\/sale\/(.+)$/','url должен начинаться с /sale',
            ],
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
            'description':'Название акции',
            'type':'text',
            'name':'header',
            'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True
        },
        {
            'description':'Дата начала акции',
            'type':'date',
            'name':'dat_from'
        },
        {
            'description':'Дата окончания акции',
            'type':'date',
            'name':'dat_to'
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'photos',
            'table':'sale_photo',
            'table_id':'id',
            'foreign_key':'sale_id',
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
                    'filedir':'./files/sale',
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
      


