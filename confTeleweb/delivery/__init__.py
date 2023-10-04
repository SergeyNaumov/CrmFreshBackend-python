
def url_before_code(form,field):
    #form.pre({'shop':form.shop})
    #field['description']=form.shop['domain']
    shop=form.s.shop
    #form.pre(shop)
    field['fields'][1]['values']=[
        {'d':'ссылка на каталог товаров','v':f'https://{shop["domain"]}/good-catalog'},
        {'d':'ссылка на каталог услуг','v':f'https://{shop["domain"]}/service-catalog'},
    ]

form={
    'work_table':'delivery',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Способы доставки',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    'fields': [ 
        {
            'description':'Способ доставки',
            'type':'text',
            'name':'header',
            'unique':1,
            #'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True
        },
        {
            'description':'Цена',
            'name':'price',
            'type':'text',
            'regexp_rules':[
                '/^\d+$/','Укажите цену',
            ],
            'filter_on':True
        },
        {
            'description':'Требуется адрес для доставки',
            'name':'need_address',
            'type':'checkbox'
        }
        

  ]  
    
}
      


