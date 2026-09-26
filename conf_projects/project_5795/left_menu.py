left_menu=[
      {
         "header":"Стандартные сервисы",
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
                  "config":"temp_const"
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
            # {
            #    "header":"Нижнее меню",
            #    "value":"admin-tree",
            #    "type":"vue",
            #    "child":[],
            #    "params":{
            #       "config":"bottom_menu"
            #    }
            # },


            # {
            #    "header":"Шаблоны для wysiwyg",
            #    "value":"admin-tree",
            #    "type":"vue",
            #    "child":[],
            #    "params":{
            #       "config":"wysiwyg_template"
            #    }
            # },
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
               "params":{"config":"rubricator"},
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
         "header":"Способы доставки",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"delivery"},
         "icon":"fa fa-car"
      },
      {
         "header":"Способы оплаты",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"paid"},
         "icon":"fa fa-coins"
      },
      {
         'header':'Администрирование бота',
         'icon':'fa fa-robot',
         #"type":"vue",
         "child":[
               {
                  "header":"Команды бота",
                  
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"bot_rules"},
                  'icon':'fa fa-robot',
               },
               {
                  "header":"Администраторы бота",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"admin_tg"},
                  "icon":"fa fa-users"
               },
         ]
      },
      {
         "header":"Клиенты",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"user"},
         "icon":"fa fa-users"
      },
      {
         "header":"Рассылка",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"bot_subscribe"},
         "icon":"fa fa-users"
      },
      {
         "header":"Заказы",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"zakaz"},
         "icon":"fa fa-box-open"
      },




]
