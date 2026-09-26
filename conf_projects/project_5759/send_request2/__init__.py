"""
create TABLE `struct_5759_send_request2` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `phone` varchar(50) NOT NULL DEFAULT '',
  `registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `body` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COMMENT='заявка со страницы услуг';
"""
form={
    'work_table':'struct_5759_send_request2',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'заявка со страницы услуг',
    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5759_send_request2','a':'wt'},
        
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
            'description':'Что заинтересовало?',
            'type':'text',
            'name':'body',
            'filter_on':1
        },
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'name':'registered',
            'filter_on':1
        }
  ]  
    
}
      


