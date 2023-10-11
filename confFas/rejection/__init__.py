

form={
    'work_table':'rejection',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Протоколы-отказ',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'rejection','a':'wt'},
        
        {'t':'transfere_result','a':'tr', 'l':'tr.parent_id = wt.id','lj':1},
        {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},

        
    ],
    'GROUP_BY':'',
    'search_links':[
        #{'link':'/vue/admin_table/rejection_assignment','description':'Список менеджеров для распределения','target':'_blank'},

    ],
    'fields': [ 
    
    {
      'description':'id',
      'name':'id',
      'type':'text',
      'filter_type':'range',
      'read_only':1,
      'filter_on':1,
    },
    {
      'description':'Рег. номер','name':'reg_number',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'НМЦК',
      'filter_type':'range',
      'type':'text',
      'filter_on':1,
      'name':'start_price',
    },
    {
      'description':'Обеспечение исполнения контракта',
      'filter_type':'range',
      'filter_on':1,
      'name':'contract_obesp',
      'type':'text',
    },
    {
      'description':'Сумма ГО',
      'filter_type':'range',
      'filter_on':1,
      'type':'text',
      'name':'bg_sum',
    },
    {
      'description':'Размер обеспечения заявки',
      'filter_type':'range',
      'filter_on':1,
      'type':'text',
      'name':'application_guarantee',
    },
    # {
    #   'description':'Наименование организации','name':'Name_Org',
    #   'filter_on':1
    # },
    {
      'description':'ИНН заказчика','name':'customer_inn',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Наименование заказчика','name':'customer_name',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'ИНН','name':'inn',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Наменование','name':'header',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Не FTP',
      'type':'checkbox',
      'name':'without_ftp',
      'filter_on':1,
    },
    {
      'description':'Организация',
      'type':'text',
      'name':'org_name',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Выручка в прошлом году',
      'name':'revenue_last_year',
      'type':'text',
      'filter_type':'range',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Прибыль в прошлом году',
      'name':'profit_last_year',
      'type':'text',
      'filter_type':'range',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Город компании',
      'type':'text',
      'filter_on':1,
      'name':'rejector_city',
    },
    {
      'description':'Рег. дата',
      'name':'registered',
      'type':'datetime',
      'filter_on':1,
      #'default_off':1,
      'not_order':0
      #'not_order':1
    },
    {
      'description':'Фактическое время парсинга',
      'type':'date',
      'name':'ts',
      #'default_off':0,
      'filter_on':1,
    },
    {
      'description':'Причина1','name':'reason1',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Причина2','name':'reason2',
      'type':'text',
      'filter_on':1,
      'not_order':1
    },
    {
      'description':'Links','name':'link',
      'type':'text',
      'filter_on':1,
      'not_order':1,

    },
    {
      'description':'Отправить уведомление',
      'name':'api_links',
      'type':'text',
      'filter_on':1,

    },
    {
      'description':'Распределено на',
      'type':'select_from_table',
      'name':'manager_id',
      'table':'manager',
      'tablename':'m',
      'header_field':'name',
      'value_field':'id',
      'filter_on':1
    },
    {
      'description':'ID карты ОП',
      'type':'filter_extend_text',
      'tablename':'tr',
      'filter_type':'range',
      'name':'user_id',
      #'read_only':1,
      'filter_on':1,
    },
    {
      'description':'Уклонений в теч. года',
      'name':'inclusion_statistics',
      'type':'text',
      'filter_type':'range',
      'filter_on':1
    },
    {
      'description':'Дубль',
      'type':'filter_extend_checkbox',
      'tablename':'tr',
      'name':'is_double',
      'filter_on':1,
    }
  ]  
    
}
      


