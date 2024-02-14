type_value=5 # rejection3
"""
# В эту таблица пишем результату распределения
create table transfere_result(
   id int unsigned primary key auto_increment,
   `type` tinyint unsigned comment 'см. assignment.type',
    `parent_id` int unsigned comment 'rejection.id или contract_termination.id в зависимости от type',
    `user_id` int unsigned not null default '0' comment 'Карта ОП, с которой мы связываем',
    `manager_id` int unsigned comment 'менеджер на которого распределяем',
    is_double tinyint unsigned not null default '0',
    unique key(parent_id,type)
) engine=innodb default charset=utf8 comment 'результаты распределений';
"""
form={
    'type_value':type_value,
    'work_table':'assignment',
    'work_table_id':'id',
    'foreign_key':'type',
    'foreign_key_value':type_value,

    'title':'',
    #'explain':1,
    'add_where':f'wt.type={type_value}',
    'QUERY_SEARCH_TABLES':[
        {'t':'assignment','a':'wt'},
        {'t':'manager','a':'m','l':'wt.manager_id=m.id'},
    ],
    'search_on_load':1,
    'fields': [ 
        {
            'description':'Менеджер',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_id',
            'header_field':'name',
            'value_field':'id',
            'tablename':'m',
            'filter_on':1
            
        },
        {
            'description':'Коэффициент',
            'name':'coefficient',
            'type':'text',
            'regexp_rules':[
                '/^(\d+)$/i','Допускается только число',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ],
            'filter_on':1
        },
        {
         'description':'Временная зона',
         'add_description':'например +4 -- это Омск, 0 -- Москва',
         'name':'timeshift',
         'type':'select_values',
         'values':[
            {'v':'-1','d':'-1 (Калининград)'},
            {'v':'0','d':'0 (Москва)'},
            {'v':'1','d':'+1 (Самара)'},
            {'v':'2','d':'+2 (Екатеринбург)'},
            {'v':'3','d':'+3 (Омск)'},
            {'v':'4','d':'+4 (Красноярск)'},
            {'v':'5','d':'+5 (Иркутск)'},
            {'v':'6','d':'+6 (Якутск)'},
            {'v':'7','d':'+7 (Владивосток)'},
            {'v':'8','d':'+8 (Магадан)'},
            {'v':'9','d':'+9 (Камчатка)'},
          ],
          'filter_on':1
        }

  ]  
    
}
      

