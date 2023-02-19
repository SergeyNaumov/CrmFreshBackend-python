"""

create table struct_5759_service_stage(
    id int unsigned primary key auto_increment,
    service_id int unsigned not null,
    header varchar(200) not null default '',
    photo varchar(200) not null default '',
    body text,
    enabled tinyint unsigned not null default '0',
    constraint foreign key(service_id) references struct_5759_service(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;

create table struct_5759_service_tarif1(
    id int unsigned primary key auto_increment,
    service_id int unsigned not null,
    header varchar(200) not null default '',
    anons varchar(256) not null default '',
    price int unsigned not null default '0'
    photo varchar(200) not null default '',
    body text,
    enabled tinyint unsigned not null default '0',
    constraint foreign key(service_id) references struct_5759_service(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;

create table struct_5759_service_tarif2(
    id int unsigned primary key auto_increment,
    service_id int unsigned not null,
    header varchar(200) not null default '',
    
    price int unsigned not null default '0'
    anons varchar(256) not null default '',
    deadline varchar(255)
    photo varchar(200) not null default '',
    body text,
    enabled tinyint unsigned not null default '0',
    constraint foreign key(service_id) references struct_5759_service(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;

"""
form={
    'work_table':'struct_5759_service',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Услуги',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':True,
    'edit_form_full':True,
    'fields': [ 
        {
            'description':'Заголовок1 / наименование услуги',
            'type':'text',
            'name':'header',
            'tab':'main'
        },
        # Здесь помещаем только те поля, которые нам нужны для сайта (чтение структуры)
        {
            'description':'Иконка',
            'name':'icon',
            'type':'file',
            'filedir':'./files/project_5759/service_icon',
            'tab':'main'
            
        },
        { 'description':'цена от','type':'text', 'name':'price_from','tab':'main'},
        { 'description':'Анонс','type':'textarea', 'name':'anons','tab':'main'},
        {
            'description':'Заголовок на промо',
            'name':'promo_header',
            'type':'text',
            'tab':'promo'
        },
        {
            'description':'Заголовок на промо - 2',
            'name':'promo_header2',
            'type':'text',
            'tab':'promo'
        },
        {
            'description':'Текст promo',
            'name':'promo_body',
            'type':'wysiwyg',
            'tab':'promo'
        },
        {
            'description':'Ссылка "тариф"?',
            'name':'link_tarif',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Заголовок тарифа 1',
            'name':'header_tarif1',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Заголовок тарифа 2',
            'name':'header_tarif2',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Текстовый блок описания услуги',
            'name':'body',
            'type':'wysiwyg',
            'tab':'tarifs'
        }
  ]  
    
}
      


