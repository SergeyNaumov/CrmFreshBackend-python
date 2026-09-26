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
    'work_table':'struct_5830_feedback_form',
    'work_table_id':'id',
    'title':'Форма "Обратная связь"',
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5830_feedback_form','a':'wt'},
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
            'description':'Email',
            'name':'email',
            'type':'text',
            "regexp_rules": [
                r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$",
                "Email заполнен не корректно"
            ],
            'filter_on':1,
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
            'description':'Сообщение',
            'type':'textarea',
            'name':'message',
            'filter_on':1,
            'regexp_rules':[
                '^.+$','Введите текст сообщения',
            ]
        },
        {
            'description':'Дата и время регистрации',
            'type':'text',
            'filter_on':1,
            'read_only':True,
            'name':'registered',
        }
  ]  
    
}
      


