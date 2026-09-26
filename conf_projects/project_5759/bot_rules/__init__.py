"""
create table struct_5759_slider(
    id int unsigned primary key auto_increment,
    sort int unsigned not null default '0',
    header varchar(512) not null default '',
    photo varchar(20) not null default ''
) engine=innodb default charset=utf8;
alter table struct_5759_slider add photo_mob varchar(20) not null default ''
"""
form={
    'work_table':'bot_rules',
    'work_table_id':'id',
    #'work_table_foreign_key':'bot_id',
    #'work_table_foreign_key_value':1,
    'title':'Правила бота',
    'sort':1,
    'tree_use':0,
    'header_field':'command',
    'default_find_filter':'',
    #'changed_in_tree':True, 
    'fields': [ 
        {
            'description':'Команда',
            'type':'text',
            'name':'command',
        },
        
        {
            'description':'Сообщение',
            'type':'textarea',
            'name':'message',
        },
        {
            'description':'Кнопки',
            'type':'1_to_m',
            'table':'bot_rules_webapp',
            'table_id':'id',
            'foreign_key':'rule_id',
            #'view_type':'list',
            'sort':1,
            'name':'buttons',
            'cols':1,
            'fields':[
                {
                    'description':'Название кнопки',
                    'type':'text',
                    'name':'header'
                },
                {
                    'description':'Ссылка на web-приложение',
                    'type':'text',
                    'name':'url'
                },
            ]

        }

  ]  
    
}
      


