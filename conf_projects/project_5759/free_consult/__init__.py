"""
CREATE TABLE `struct_5759_free_consult` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `phone` varchar(50) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `url` varchar(200) NOT NULL DEFAULT '',
  `registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
form={
    'work_table':'struct_5759_free_consult',
    'work_table_id':'id',
    'title':'Форма "Бесплатная консультация"',
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5759_free_consult','a':'wt'},
        #{'t':'struct_5759_service','a':'s','l':'wt.service_id=s.id','lj':1},
    ],
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'filter_on':1,
            'regexp_rules':[ '^.+$','Заполните имя']
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'filter_on':1,
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ]
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url',
            'filter_on':1,
            'regexp_rules':[
                '^.+\..+','url не заполнен или заполнен некорректно',
            ]
        },
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'filter_on':1,
            'name':'registered',
        }
  ]  
    
}
      


