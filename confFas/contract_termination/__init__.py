

form={
    'work_table':'contract_termination',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Одностороннее расторжение',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'contract_termination','a':'wt'},
        {'t':'transfere_result','a':'tr', 'l':'tr.parent_id = wt.id','lj':1},
        {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},
        {'t':'user','a':'u','l':'tr.user_id=u.id','lj':True},
      ],
    #'explain':1,
    'search_links':[
        #{'link':'/vue/admin_table/contract_termination_assignment','description':'Список менеджеров для распределения','target':'_blank'},

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
            'filter_on':False,

        },
        
        {
            'description':'Дата регистрации карты ОП',
            'type':'filter_extend_date',
            'name':'registered',
            'tablename':'u',
            'filter_on':True,
            #'value':['2023-08-01','2023-08-02']

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
          'name':'manager_id',
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
            'name':'user_id',
            'filter_on':True
        },
  ]  
    
}
      


