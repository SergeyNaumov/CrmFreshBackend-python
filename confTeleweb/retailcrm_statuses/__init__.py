
# def url_before_code(form,field):
#     #form.pre({'shop':form.shop})
#     #field['description']=form.shop['domain']
#     shop=form.s.shop
#     #form.pre(shop)
#     field['fields'][1]['values']=[
#         {'d':'ссылка на каталог товаров','v':f'https://{shop["domain"]}/good-catalog'},
#         {'d':'ссылка на каталог услуг','v':f'https://{shop["domain"]}/service-catalog'},
#     ]
form={
    'work_table':'retailcrm_statuses',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Способы оплаты',
    #'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    'search_on_load':1,
    'fields': [ 
        {
            'description':'Сортировка в RetailCRM',
            'name':'sort',
            'type':'text',
            'filter_on':True,
            'read_only':True  
        },
        {
            'description':'Активен',
            'name':'active',
            #'value':1,
            'type':'checkbox',
            'filter_on':True,
            'read_only':True  
        },
        {
            'description':'Статус в RetailCRM',
            'type':'text',
            'name':'header',
            'unique':1,
            #'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True,
            'read_only':True
        },
        {
            'description':'Код статуса',
            'name':'code',
            'type':'text',
            'filter_on':True,
            'read_only':True  
        },
        
        {
            'description':'Статус в AssistBot',
            'name':'status',
            'type':'select_values',
            'values':[
                {'v':1,'d':'в обработке'},
                {'v':2,'d':'собран'},
                {'v':3,'d':'отправлен'},
                {'v':4,'d':'доставлен'},
                {'v':5,'d':'возврат'},
                {'v':6,'d':'отменён'},
            ],
            'filter_on':True,
            'change_in_search':True,
            'make_change_in_search':True,
        }
        # {
        #     'description':'Цена',
        #     'name':'price',
        #     'type':'text',
        #     'regexp_rules':[
        #         '/^\d+$/','Укажите цену',
        #     ],
        #     'filter_on':True
        # },
        

  ]  
    
}
      


