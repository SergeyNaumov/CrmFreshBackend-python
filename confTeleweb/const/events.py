from .gpt_fields import add_gpt_fields



def add_robokassa_fields(form):
    # Эти поля нужны в том случае, если нам нужна робокасса
    form.tabs.append({'name':'robokassa','description':'Robokassa'})
    add_fields=[
            {
                'description':'Robokassa работает в тестовом режиме',
                'type':'checkbox',
                'name':'robokassa_test',
                'tab':'robokassa',
            },
            {
                'description':'Robokassa - Логин',
                'type':'text',
                'name':'robokassa_log',
                'tab':'robokassa',
            },
            {
                'description':'Robokassa - Пароль1',
                'type':'text',
                'name':'robokassa_pas1',
                'tab':'robokassa',
            },
            {
                'description':'Robokassa - Пароль2',
                'type':'text',
                'name':'robokassa_pas2',
                'tab':'robokassa',
            },
            {
                'description':'Наименование организации',
                'type':'text',
                'name':'orgname',
                'tab':'robokassa',
            },
            {
                'description':'ИНН',
                'type':'text',
                'name':'inn',
                'tab':'robokassa',
            },
            {
                'description':'ОГРН/ОГРНИП',
                'type':'text',
                'name':'ogrn',
                'tab':'robokassa',
            },
            {
                'description':'Контактный телефон',
                'type':'text',
                'name':'contact_phone',
                'tab':'robokassa',
            },
            {
                'description':'Контактный email',
                'type':'text',
                'name':'contact_email',
                'tab':'robokassa',
            },
            {
                'description':'Оферта',
                'type':'file',
                'name':'oferta',
                'tab':'robokassa',
            }
    ]
    for f in add_fields:
        form.fields.append(f)

def permissions(form):
    db=form.db

    form.fields=[
        {
            'description':'Наименование компании',
            'type':'text',
            'name':'orgname',
            'tab':'main',
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'tab':'main',
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
            'tab':'main',
        },
        {
            'description':'Email для форм обратной связи',
            'type':'text',
            'name':'email_for_feedback',
            'tab':'main',
        },
        {
            'description':'Email для заказов',
            'type':'text',
            'name':'email_for_zakaz',
            'tab':'main',
        },
        {
            'description':'Сообщение, когда бот не оплачен',
            'type':'textarea',
            'name':'not_paid_message',
            'tab':'main',
        },
        {
            'description':'Код счётчика(ов) посещений',
            'type':'textarea',
            'name':'counter',
            'tab':'main'
        },
        {
            'description':'Отправка заказов в RetailCRM',
            #'type':'select_values',
            'name':'send_orders_to_retail',
            'type':'checkbox',
            'tab':'integration',
        },
        {
            'description':'Загрузка товаров',
            #'type':'select_values',
            'name':'goods_load',
            'type':'select',
            'values':[
                {'v':'1','d':'из YML-файла'},
                {'v':'2','d':'из Retail CRM'},
            ],
            'add_description':'выберите один из вариантов',
            'tab':'integration',
        },
        {
            'description':'Очистить каталог товаров',
            'add_description':'Удалять все категрии и товары перез загрузкой из внешнего источника',
            'type':'checkbox',
            'name':'clear_goods_before_parse',
            'tab':'integration',
        },
        {
            'description':'YML для товаров',
            'add_description':'укажите url по которому мы сможем получить YML файл для обновления товаров',
            'type':'text',
            'name':'url_yml',
            'tab':'integration',
        },
        {
            'description':'Удалять товары, которых нет в YML',
            'type':'checkbox',
            'name':'delete_not_exists_goods',
            'tab':'integration',
        },
        {
            'description':'YML для услуг',
            'add_description':'укажите url по которому мы сможем получить YML файл для обновления услуг',
            'type':'text',
            'name':'url_yml_serv',
            'tab':'integration',
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

    add_gpt_fields(form)

    #print('zakaz_method:',form.s.shop.get('zakaz_method'))
    if form.s.shop.get('zakaz_method')==1:
        # Если метод заказа товаров робокасса
        add_robokassa_fields(form)

    if form.s.shop['serv_fast_robokassa']:

        add_robokassa_fields(form)
        add_fields=[

            {
                'description':'Ссылка на файл google docs',
                'type':'text',
                'name':'google_docs_sheet',
                'tab':'robokassa',
            },

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