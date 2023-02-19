"""
CREATE TABLE `struct_5759_callback` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL DEFAULT '',
  `phone` varchar(50) NOT NULL DEFAULT '',
  `time` varchar(100) not null DEFAULT '',
  `registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
form={
    'work_table':'struct_5759_callback',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Форма "обратный звонок"',
    
    'explain':False,
    'header_field':'name',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Имя',
            'type':'text',
            'name':'name',
            'regexp_rules':[
                '^.+$','Заполните имя',
            ]
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'regexp_rules':[
                '^\+7.+','Телефон не заполнен или заполнен некорректно',
            ]
        },
        {
            'description':'Удобное время для звонка',
            'type':'text',
            'name':'time',
        },
        {
            'description':'Дата и время отправки',
            'type':'text',
            'name':'registered',
        }
  ]  
    
}
      


