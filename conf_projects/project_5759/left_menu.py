left_menu=[
      {
         "header":"Стандартные сервисы",
         "value":"https://help.design-b2b.com/",
         "icon":"fa fa-sitemap",
         "type":"src",
         "show":True,
         "child":[
            {
               "header":"Файлы для поисковиков",
               "value":"admin-table",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"find_files"
               }
            },
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
            },
            {
               "header":"Шаблоны для wysiwyg",
               "value":"admin-tree",
               "type":"vue",
               "child":[],
               "params":{
                  "config":"wysiwyg_template"
               }
            },
         ]
      },
      {
         "header":"Администрирование бота",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"bot_rules"},
         "icon":"fa-duotone fa-image"
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
                  "header":"Сферы деятельности",
                  "value":"admin-tree",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"opportunity" }
               },
               {
                  "header":"Кейсы РК",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_rk" }
               },
               {
                  "header":"Кейсы SMM",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_smm" }
               },
               {
                  "header":"Кейсы SEO",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_seo" }
               },
               {
                  "header":"Кейсы сайты",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_sites" }
               },
               {
                  "header":"Кейсы айдентика",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{ "config":"case_identity" }
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
         "header":'Блок "Вас может заинтересовать"',
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{ "config":"interest" }
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
         "header":"Готовые решения",
         "value":"admin-tree",
         "type":"vue",
         "child":[ ],
         "params":{ "config":"solution" }
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
               "header":"Оставить заявку (со страницы услуг)",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"send_request2" }
            },
            {
               "header":"Заявки на готовое решение",
               "value":"admin-table",
               "type":"vue",
               "child":[ ],
               "params":{ "config":"send_request_solution" }
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
