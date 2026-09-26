left_menu=[
      {
         "header":"Базовое наполнение",
         #"value":"https://help.design-b2b.com/",
         "icon":"fa fa-sitemap",
         "type":"src",
         "show":True,
         "child":[
            # {
            #    "header":"Promo",
            #    "value":"admin-table",
            #    "type":"vue",
            #    "child":[],
            #    "params":{
            #       "config":"promo"
            #    }
            # },
            # {
            #    "header":"Статичные текстовые страницы",
            #    "value":"admin-table",
            #    "type":"vue",
            #    "child":[],
            #    "params":{
            #       "config":"content"
            #    }
            # },
            {
               "header":"Настройки",
               "value":"const",
               "type":"vue",
               "child":[],
               "icon":"fa fa-wrench",
               "params":{
                  "config":"template_const"
               }
            },
            {
               "header":"Верхнее меню",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"top_menu_tree"
               },
               "icon":"fa fa-list-ul",
            },
            {
               "header":"Нижнее меню",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"bottom_menu"
               },
               "icon":"fa fa-list-ul",
            },
            {
               "header":"Слайдер для главной",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"slider_main"
               }
            },
            {
               "header":"Рекомендации",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"recomendation"
               }
            },


         ]
      },
      {
         'header':'Каталог товаров',
         'value':'admin-tree',
         "icon":"fa fa-table",
         "child":[
            {
               "header":"Рубрики каталога",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{"config":"catalog"},
               #"icon":"fa-duotone fa-image"
            },
            {
               "header":"Направления деятельности",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{"config":"direction"},
               #"icon":"fa-duotone fa-image"
            },
            {
               "header":"Товары",
               "value":"admin-table",
               "type":"vue",
               "child":[],
               "params":{"config":"good"},
               
            },
         ],
      },
      {
         'header':'Новости',
         'value':'admin-table',
         "type":"vue",
         "child":[],
         "params":{"config":"news"},
      },
      {
         'header':'Сертификаты',
         'value':'admin-table',
         "type":"vue",
         "child":[],
         "params":{"config":"cert"},
      },
      {
         'header':'Вендоры',
         'value':'admin-tree',
         "type":"vue",
         "child":[],
         "params":{"config":"vendor"},
      },
      {
         'header':'Партнёры',
         'value':'admin-tree',
         "type":"vue",
         "child":[],
         "params":{"config":"partner"},
      },
      {
         'header':'Заказчики',
         'value':'admin-tree',
         "type":"vue",
         "child":[],
         "params":{"config":"owner"},
      },
      {
         'header':'Менеджеры',
         'value':'admin-tree',
         "type":"vue",
         "child":[],
         "params":{"config":"manager"},
      },
      {
         'header':'Преимущества',
         'value':'admin-tree',
         "type":"vue",
         "child":[],
         "params":{"config":"advantages"},
      },
      {
         'header':'Текстовые страницы',
         'value':'admin-table',
         "type":"vue",
         "child":[],
         "params":{"config":"text_page"},
      },
      {
         'header':'Текстовые блоки',
         'value':'admin-table',
         "type":"vue",
         "child":[],
         "params":{"config":"text_block"},
      },
      # {
      #    "header":"Способы доставки",
      #    "value":"admin-tree",
      #    "type":"vue",
      #    "child":[],
      #    "params":{"config":"delivery"},
      #    "icon":"fa fa-car"
      # },
      # {
      #    "header":"Способы оплаты",
      #    "value":"admin-tree",
      #    "type":"vue",
      #    "child":[],
      #    "params":{"config":"paid"},
      #    "icon":"fa fa-coins"
      # },
      # {
      #    'header':'Администрирование бота',
      #    'icon':'fa fa-robot',
      #    #"type":"vue",
      #    "child":[
      #          {
      #             "header":"Команды бота",
                  
      #             "value":"admin-table",
      #             "type":"vue",
      #             "child":[],
      #             "params":{"config":"bot_rules"},
      #             'icon':'fa fa-robot',
      #          },
      #          {
      #             "header":"Администраторы бота",
      #             "value":"admin-table",
      #             "type":"vue",
      #             "child":[],
      #             "params":{"config":"admin_tg"},
      #             "icon":"fa fa-users"
      #          },
      #    ]
      # },
      # {
      #    "header":"Клиенты",
      #    "value":"admin-table",
      #    "type":"vue",
      #    "child":[],
      #    "params":{"config":"user"},
      #    "icon":"fa fa-users"
      # },
      # {
      #    "header":"Рассылка",
      #    "value":"admin-table",
      #    "type":"vue",
      #    "child":[],
      #    "params":{"config":"bot_subscribe"},
      #    "icon":"fa fa-users"
      # },
      {
         "header":"Форма обратной связи",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"feedback_form"},
         "icon":"fa fa-box-open"
      },
      {
         "header":'Форма "отправить заявку"',
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"send_request_form"},
         "icon":"fa fa-box-open"
      },



]
