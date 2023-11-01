def permissions(form):
    db=form.db
    form.fields=[
        {
            'description':'Наименование компании',
            'type':'text',
            'name':'orgname',
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
        },
        {
            'description':'Email для форм обратной связи',
            'type':'text',
            'name':'email_for_feedback',
        },
        {
            'description':'Email для заказов',
            'type':'text',
            'name':'email_for_zakaz',
        },
        {
            'description':'Сообщение, когда бот не оплачен',
            'type':'textarea',
            'name':'not_paid_message'
        },
        # {
        #     'description':'Главный раздел сайта это',
        #     'name':'main_page_type'
        #     'type':'select_values',
        #     'values':[
        #         {'v':'1','d':'товары'},
        #         {'v':'2','d':'услуги'},
        #     ]
        # },
        # {
        #     'description':'Выводить раздел услуг',
        #     'type':'checkbox',
        #     'name':'need_serv'
        # },
        {
            'description':'Интеграция',
            #'type':'select_values',
            'name':'integration',
            'type':'select',
            'values':[
                {'v':'1','d':'YML-файл'},
                {'v':'2','d':'Retail CRM'},
            ]
        },
        {
            'description':'Домен для интеграции RetailCRM',
            'name':'retailcrm_domain',
            'type':'text',
        },
        {
            'description':'API key для интеграции RetailCRM',
            'name':'retailcrm_api_key',
            'type':'text',
        },
        {
            'description':'Url для yml (товары)',
            'type':'text',
            'name':'url_yml',
        },
        {
            'description':'Вариант отображения списка товаров',
            'type':'select',
            'name':'catalog_list_view',
            'values':[
                {'v':1,'d':'Вариант1'},
                {'v':2,'d':'Вариант2'},
            ]
        },
        {
            'description':'Url для yml (услуги)',
            'type':'text',
            'name':'url_yml_serv',
        },
        #{
        #    'description':'Copyright',
        #    'type':'text',
        #    'name':'copyright',
        #},
    ]

    # form.fields=db.query(
    #     query='''
    #         SELECT
    #              description, header name,type
    #         FROM
    #             template_const
    #         WHERE
    #             template_id=%s
    #         ORDER BY sort
    #     ''',
    #     #debug=1,
    #     errors=form.errors,
    #     values=[form.s.template_id]

    # )
    form.filedir=f"./files/project_{form.s.shop_id}"
    form.filedir_http=f"/files/project_{form.s.shop_id}"
    
    form.foreign_key='shop_id'
    form.foreign_key_value=form.s.shop_id

    #print('CONST_LIST:', form.fields)
    
    
events={
    'permissions':permissions
}