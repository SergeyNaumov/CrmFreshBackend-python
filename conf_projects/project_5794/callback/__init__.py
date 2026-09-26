"""
create table struct_5794_callback(
    id int unsigned primary key auto_increment,
    name varchar(100),
    phone varchar(50),
    time varchar(50) not null default '',
    registered timestamp default current_timestamp
) engine=innodb default charset=utf8;
"""

form={
    'work_table':'struct_5794_callback',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Форма "Обратный звонок"',
    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        #{'t':'struct_5794_send_request','a':'wt'},

    ],
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'regexp_rules':[
                '^.+$','Заполните имя',
            ],
            'filter_on':1
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ],
            'filter_on':1
        },
        {
            'description':'Время',
            'type':'textarea',
            'name':'time',
            'filter_on':1
        },

  ]  
    
}
      


