

form={
    'work_table':'contract_termination2',
    'work_table_id':'id',
    'title':'Одностороннее расторжение2',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'make_delete':False,
    'read_only':True,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'contract_termination','a':'wt'},
        {'t':'manager','a':'m','l':'wt.manager_id2=m.id','lj':True},
        {'t':'user','a':'u','l':'wt.user_id2=u.id','lj':True},
      ],
    'fields': [ 
    
        {
            'description':'Дубль',
            'type':'checkbox',
            'name':'is_double',
            'filter_on':True
        },
        {
            'description':'Реестровый номер',
            'type':'text',
            'name':'reestr_number',
            'filter_on':True
        },
        {
            'description':'ИНН',
            'type':'text',
            'name':'inn',
            'filter_on':True
        },
        {
            'description':'Объект покупки',
            'type':'text',
            'name':'purchase_object',
            'filter_on':True
        },
        {
            'description':'Наименование организации',
            'type':'text',
            'name':'name_org',
            'filter_on':True
        },
        {
            'description':'Дата регистрации',
            'type':'date',
            'name':'registered_date',
            'filter_on':True
        },
        
        {
            'description':'Дата регистрации карты ОП',
            'type':'filter_extend_date',
            'name':'registered',
            'tablename':'u',
            'filter_on':True
        },
        {
            'description':'Причина1',
            'type':'text',
            'name':'reason1',
            'filter_on':True
        },
        {
            'description':'Причина2',
            'type':'text',
            'name':'reason2',
            'filter_on':True
        },
        {
            'description':'Уклонений в теч. года',
            'type':'text',
            'name':'inclusion_statistics',
            'filter_type':'range',
            'filter_on':True
        },
        {
            'description':'Ссылка',
            'type':'text',
            'name':'link',
            'filter_on':True
        },
        {
            'description':'Ссылка для скачивания',
            'type':'text',
            'name':'download_link',
            'filter_on':True
        },
        {
          'description':'Распределено на',
          'type':'select_from_table',
          'name':'manager_id2',
          'table':'manager',
          'tablename':'m',
          'header_field':'name',
          'value_field':'id',
          'filter_on':True
        },
        {
            'description':'Отправить уведомление',
            'type':'text',
            'name':'api_links',
            'filter_on':True
        },
        {
            'description':'ID карты ОП',
            'type':'text',
            'name':'user_id2',
            'filter_on':True
        },
  ]  
    
}
      


