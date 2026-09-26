left_menu=[
      # {
      #    "header":"Стандартные сервисы",
      #    #"value":"https://help.design-b2b.com/",
      #    "icon":"fa fa-sitemap",
      #    "type":"src",
      #    "show":True,
      #    "child":[
      #       # {
      #       #    "header":"Promo",
      #       #    "value":"admin-table",
      #       #    "type":"vue",
      #       #    "child":[],
      #       #    "params":{
      #       #       "config":"promo"
      #       #    }
      #       # },



      #       # {
      #       #    "header":"Нижнее меню",
      #       #    "value":"admin-tree",
      #       #    "type":"vue",
      #       #    "child":[],
      #       #    "params":{
      #       #       "config":"bottom_menu"
      #       #    }
      #       # },


      #       # {
      #       #    "header":"Шаблоны для wysiwyg",
      #       #    "value":"admin-tree",
      #       #    "type":"vue",
      #       #    "child":[],
      #       #    "params":{
      #       #       "config":"wysiwyg_template"
      #       #    }
      #       # },
      #    ]
      # },
      {

         "header":"Файлы для поисковиков",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "icon":"fa fa-wrench",
         "params":{
            "config":"robot_files"
         }
      },
      {
         "header":"Константы системы",
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

         "header":"Статичные текстовые страницы",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{
            "config":"content"
         }
      },

      {
         "header":"Слайдер фото в шапке",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"slider"},
         #"icon":"fa-duotone fa-image"
      },
      {
         "header":"Единицы измерения",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"ed"},
         "icon":""
      },
      {
         "header":"Услуги",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"service"},
         #"icon":"fa-duotone fa-image"
      },
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
      {
         "header":"Документы",
         "value":"admin-table",
         "type":"vue",
         "child":[],
         "params":{"config":"document"},
         "icon":""
      },
      {
         "header":"Видео",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"video"},
         "icon":""
      },
      {
         "header":"Адреса",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"address_list"},
         "icon":""
      },
      {
         "header":"Наша команда",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"team"},
         "icon":""
      },
      {
         "header":"Наши преимущества",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"advantages"},
         "icon":""
      },
      {
         "header":"Наши партнёры",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"partner"},
         "icon":""
      },


      {
         "header":"Схема работы",
         "value":"admin-tree",
         "type":"vue",
         "child":[],
         "params":{"config":"scheme_work"},
         "icon":""
      },
      {
         "header":"Формы",
         "show":True,
         "child":[
               {
                  "header":"Не нашли, что искали?",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"send_request"},
                  "icon":""
               },
               {
                  "header":"Отправить заявку",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"send_request2"},
                  "icon":""
               },
               {
                  "header":"Заказать прайс",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"get_price"},
                  "icon":""
               },
               {
                  "header":"Обратный звонок",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"callback"},
                  "icon":""
               },
               {
                  "header":"Задать вопрос",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"ask_question"},
                  "icon":""
               },
               {
                  "header":"Получить консультацию",
                  "value":"admin-table",
                  "type":"vue",
                  "child":[],
                  "params":{"config":"consultation"},
                  "icon":""
               },
              # {
              #     "header":"",
              #     "value":"admin-table",
              #     "type":"vue",
              #     "params":{"config":"send_request"},

              #  },
         ]
      }




]
