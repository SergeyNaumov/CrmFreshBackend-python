"""
create table test_onetom(
    id int unsigned primary key auto_increment,
    parent_id int,
    sort int,
    f1 varchar(200) not null default '' comment 'text',
    f2 varchar(200) not null default '' comment 'textarea',
    f3 tinyint unsigned not null default '0' comment 'select',
    f4 date comment 'date',
    f5 datetime comment 'datetime',
    f6 time comment 'time',
    constraint foreign key(parent_id) references test(id) on update cascade on delete cascade
) engine=innodb default charset=utf8;
"""
form={
    'work_table':'test',
    'work_table_id':'id',
    'title':'Тест 1_to_m',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    ''
    'fields': [
        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
            'regexp_rules':[
                '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/g', ''
            ],
        },

        {
            'description':'Один ко многим',
            'type':'1_to_m',
            'name':'onetom',
            'table':'test_onetom',
            'table_id':'id',
            'foreign_key':'parent_id',
            'sort':1,
            'view_type':'list',
            'fields':[
                {
                    'description':'Текстовое поле',
                    'name':'f1',
                    'type':'text',
                    'regexp_rules':[
                        '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
                    ],
                    'replace_rules':[
                        '/[^0-9]/g', ''
                    ],
                },
                {
                    'description':'select',
                    'name':'f2',
                    'type':'select_values',
                    'replace_rules':[
                        '4', '2',
                        '5', '3',
                    ],
                    'values':[
                        {'v':1,'d':'первый'},
                        {'v':2,'d':'второй'},
                        {'v':3,'d':'третий'},
                        {'v':4,'d':'четвёртый'},
                        {'v':5,'d':'пятый'},
                    ]
                },
            ]
        }
    ]

}