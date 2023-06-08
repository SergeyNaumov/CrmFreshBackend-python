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
    price int unsigned not null default '0',
    photo varchar(200) not null default '',
    body text,
    enabled tinyint unsigned not null default '0',
    constraint foreign key(service_id) references struct_5759_service(id) on update cascade on delete cascade
) engine=innodb default charset=utf8 comment 'Тарифы1'; 

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
    
    'fields': [ 
        {
            'description':'Наименование услуги',
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
        {
            'description':'Описание услуги',
            'name':'body',
            'tab':'main',
            'type':'wysiwyg'
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
            'add_description':'без нумерации',
            'name':'promo_body',
            'type':'textarea',
            'tab':'promo'
        },
        # Тарифы
        {
            'description':'Заголовок блока "тарифы"',
            'name':'tarifs_header',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Подзаголовок блока "тарифы"',
            'name':'tarifs_subheader',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Содержимое блока "тарифы1"',
            'name':'tarif1',
            'type':'1_to_m',
            'table':'struct_5759_service_tarif1',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'fields':[
                {'description':'Наименование', 'name':'header','type':'text'},
                {'description':'Подзаголовок', 'name':'subheader','type':'text'},
                {'description':'Краткое описание', 'name':'anons','type':'textarea'},
                {'description':'Цена', 'name':'price','type':'text'},
            ],
            'tab':'tarifs'
        },

        # {
        #     'description':'Заголовок тарифа 2',
        #     'name':'header_tarif',
        #     'type':'text',
        #     'tab':'tarifs'
        # },
        {
            'description':'Текст над блоком "тарифы"',
            'name':'text_above_tarifs',
            'type':'textarea',
            'tab':'tarifs'
        },
        # Блок "Тарифы2"
        {
            'description':'Заголовок блока "Тарифы2"',
            'name':'tarifs_header2',
            'type':'text',
            'tab':'tarifs2'
        },
        {
            'description':'Содержимое блока "тарифы2"',
            'name':'tarif2',
            'type':'1_to_m',
            'table':'struct_5759_service_tarif2',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'view_type':'list',
            'fields':[
                {'description':'Наименование', 'name':'header','type':'text'},
                {'description':'Цена', 'name':'price','type':'text'},
                {'description':'Срок', 'name':'deadline','type':'text'},
                {'description':'Краткое описание', 'name':'anons','type':'textarea'},
                {'description':'Подробности', 'name':'body','type':'textarea'},
                
            ],
            'tab':'tarifs2'
        },
        # Этапы работ
        {
            'description':'Содержимое блока "Этапы работ"',
            'name':'stages',
            'type':'1_to_m',
            'table':'struct_5759_service_stages',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'view_type':'list',
            'fields':[
                {'description':'Заголовок', 'name':'header','type':'text'},
                {'description':'Подзаголовок', 'name':'subheader','type':'text'},
                {'description':'Подробности', 'name':'body','type':'textarea'},
                
            ],
            'tab':'stages'
        },
        # Блок "faq"
        {
            'description':'Содержимое блока "вопрос / ответ"',
            'name':'faq',
            'type':'1_to_m',
            'table':'struct_5759_service_faq',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            #'view_type':'list',
            'fields':[
                {'description':'Вопрос', 'name':'header','type':'text'},
                {'description':'Ответ', 'name':'body','type':'textarea'},
                
            ],
            'tab':'faq'
        },
        # Блок "вас заинтересует"
        {
            'description':'Содержимое блока "вас заинтересует"',
            'name':'interest',
            'type':'1_to_m',
            'table':'struct_5759_service_interest',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            #'view_type':'list',
            'fields':[
                {
                    'description':'Выберите таб',
                    'name':'interest_id',
                    'type':'select_from_table',
                    'table':'struct_5759_interest',
                    'header_field':'header',
                    'value_field':'id'

                },
            ],
            'tab':'interest'
        },
  ]  
    
}
      


