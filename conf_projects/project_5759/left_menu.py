left_menu=[
      {
         "header":"Стандартные сервисы",
         "value":"https://help.design-b2b.com/",
         "icon":"fa fa-sitemap",
         "type":"src",
         "show":True,
         "child":[
            {
               "header":"Promo",
               "value":"admin-table",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"promo"
               }
            },
            {
               "header":"Статичные текстовые страницы",
               "value":"admin-table",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"content"
               }
            },
            {
               "header":"Верхнее меню",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"top_menu_tree"
               }
            },
            {
               "header":"Нижнее меню",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"bottom_menu"
               }
            },
            {
               "header":"Константы шаблона",
               "value":"const",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"template_const"
               }
            }
         ]
      },

      {
         "header":"Слайдер изображений",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"slider"},
         "icon":"fa-duotone fa-image"
      },

      {
         "header":"Кейсы",
         "value":"admin-tree",
         "type":"vue",
         "icon":"fa fa-duotone fa-suitcase",
         "show":True,
         "child":[
               {
                  "header":"Виды кейсов",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_type" }
               },
               {
                  "header":"Кейсы РК",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_rk" }
               },
               {
                  "header":"Кейсы SMM",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_smm" }
               },
               {
                  "header":"Кейсы SEO",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_seo" }
               },
               {
                  "header":"Кейсы сайты",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_sites" }
               },
         ],
         
      },
      {
         "header":"Услуги",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{ "config":"service" }
      },
      {
         "header":"Клиенты",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{ "config":"client" }
      },
      {
         "header":"Вопрос / ответ",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{ "config":"faq" }
      },
      {
         "header":"Отзывы",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{ "config":"review" }
      },
      {
         "header":"О нас в цифрах",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{ "config":"about_numbers" }
      },
      {
         "header":"Схема работы",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{ "config":"scheme_work" }
      },
      {
         "header":"Команда",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{ "config":"team" }
      },
      {
         "header":"Почему к нам?",
         "value":"admin-tree",
         "type":"vue",
         "child":[ ],
         "params":{ "config":"why_we" }
      },
      {
         "header":"Формы обратной связи",
         "type":"",
         'icon':'fa fa-arrow-right',
         "child":[
            {
               "header":"Оставить заявку",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"send_request" }
            },
            {
               "header":"Остались вопросы?",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"any_questions" }
            },
            {
               "header":"Нужна консультация?",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"need_consult" }
            },
            {
               "header":"Бесплатная консультация",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"free_consult" }
            },
            {
               "header":"Сообщить о проблеме руководству",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"owner_warning" }
            },
         ],

      }
]
