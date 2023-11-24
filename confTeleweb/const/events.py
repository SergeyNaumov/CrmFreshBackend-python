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
            'description':'Отправка заказов в RetailCRM',
            #'type':'select_values',
            'name':'send_orders_to_retail',
            'type':'checkbox',
        },
        {
            'description':'Загрузка товаров',
            #'type':'select_values',
            'name':'goods_load',
            'type':'select',
            'values':[
                {'v':'1','d':'из YML-файла'},
                {'v':'2','d':'из Retail CRM'},
            ]
        },
        {
            'description':'Url YML-файла для товаров',
            'type':'text',
            'name':'url_yml',
        },
        {
            'description':'Удалять товары, которых нет в YML',
            'type':'checkbox',
            'name':'delete_not_exists_goods'
        },
        {
            'description':'Url YML-файла для услуг',
            'type':'text',
            'name':'url_yml_serv',
        },
        {
            'description':'Удалять услуги, которых нет в YML',
            'type':'checkbox',
            'name':'delete_not_exists_services'
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
            'description':'Вариант отображения списка товаров',
            'type':'select',
            'name':'catalog_list_view',
            'values':[
                {'v':1,'d':'Вариант1'},
                {'v':2,'d':'Вариант2'},
            ]
        },

        # {
        #     'description':'Быстрая оплата для услуг (робокасса)',
        #     'type':'checkbox',
        #     'name':'serv_fast_paid_robokassa'
        # },

        #{
        #    'description':'Copyright',
        #    'type':'text',
        #    'name':'copyright',
        #},
    ]
    if form.s.shop['serv_fast_robokassa']:
        add_fields=[
            {
                'description':'Robokassa работает в тестовом режиме',
                'type':'checkbox',
                'name':'robokassa_test',
            },
            {
                'description':'Robokassa - Логин',
                'type':'text',
                'name':'robokassa_log',
            },
            {
                'description':'Robokassa - Пароль1',
                'type':'text',
                'name':'robokassa_pas1',
            },
            {
                'description':'Robokassa - Пароль2',
                'type':'text',
                'name':'robokassa_pas2',
            },
            {
                'description':'Ссылка на файл google docs',
                'type':'text',
                'name':'google_docs_sheet',
            },
            {
                'description':'Наименование организации',
                'type':'text',
                'name':'orgname'
            },
            {
                'description':'ИНН',
                'type':'text',
                'name':'inn'
            },
            {
                'description':'ОГРН/ОГРНИП',
                'type':'text',
                'name':'ogrn'
            },
            {
                'description':'Контактный телефон',
                'type':'text',
                'name':'contact_phone'
            },
            {
                'description':'Контактный email',
                'type':'text',
                'name':'contact_email'
            },
            {
                'description':'Оферта',
                'type':'file',
                'name':'oferta'
            }
        ]
        for f in add_fields:
            form.fields.append(f)


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