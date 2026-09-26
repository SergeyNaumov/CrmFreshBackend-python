
form={
    'work_table':'struct_5759_service',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Услуги',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':True,
    'fields': [ 
        {
            'description':'Наименование услуги',
            'type':'text',
            'name':'header',
            'tab':'main',
            #'frontend':{
            #    'ajax':{
            #        'name':'in_ext_url'
            #    }
            #}
        },
        # {
        #     'description':'url',
        #     'name':'in_ext_url',
        #     'type':'in_ext_url',
        #     'in_url':'/service/<%id%>',
        #     'foreign_key':'project_id',
        #     'foreign_key_value':5759,
        #     'tab':'main'
        # },
        # Здесь помещаем только те поля, которые нам нужны для сайта (чтение структуры)
        {
            'description':'Иконка',
            'name':'icon',
            'type':'file',
            'filedir':'./files/project_5759/service_icon',
            'tab':'main'
        },
        {
            'description':'Описание услуги',
            'name':'body',
            'tab':'main',
            'type':'wysiwyg'
        },
        { 'description':'цена от','type':'text', 'name':'price_from','tab':'main'},
        { 'description':'Анонс','type':'textarea', 'name':'anons','tab':'main'},
        {
            'description':'Заголовок на промо',
            'name':'promo_header',
            'type':'text',
            'tab':'promo'
        },
        {
            'description':'Заголовок на промо - 2',
            'name':'promo_header2',
            'type':'text',
            'tab':'promo'
        },
        {
            'description':'Текст promo',
            'add_description':'без нумерации',
            'name':'promo_body',
            'type':'textarea',
            'tab':'promo'
        },
        {
            'description':'Фоновое изображение promo',
            'type':'file',
            'filedir':'./files/project_5759/service_promo_bg',
            'name':'promo_bg',
            'tab':'promo'
        },
        # Тарифы
        {
            'description':'Заголовок блока "тарифы"',
            'name':'tarifs_header',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Подзаголовок блока "тарифы"',
            'name':'tarifs_subheader',
            'type':'text',
            'tab':'tarifs'
        },
        {
            'description':'Содержимое блока "тарифы1"',
            'name':'tarif1',
            'type':'1_to_m',
            'table':'struct_5759_service_tarif1',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'fields':[
                {'description':'Наименование', 'name':'header','type':'text'},
                {'description':'Подзаголовок', 'name':'subheader','type':'text'},
                {'description':'Краткое описание', 'name':'anons','type':'textarea'},
                {'description':'Цена', 'name':'price','type':'text'},
            ],
            'tab':'tarifs'
        },

        # {
        #     'description':'Заголовок тарифа 2',
        #     'name':'header_tarif',
        #     'type':'text',
        #     'tab':'tarifs'
        # },
        {
            'description':'Текст над блоком "тарифы"',
            'name':'text_above_tarifs',
            'type':'textarea',
            'tab':'tarifs'
        },
        # Блок "Тарифы2"
        {
            'description':'Заголовок блока "Тарифы2"',
            'name':'tarifs_header2',
            'type':'text',
            'tab':'tarifs2'
        },
        {
            'description':'Содержимое блока "тарифы2"',
            'name':'tarif2',
            'type':'1_to_m',
            'table':'struct_5759_service_tarif2',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            #'view_type':'list',
            'fields':[
                {'description':'Наименование', 'name':'header','type':'text'},
                {'description':'Цена', 'name':'price','type':'text'},
                {'description':'Срок', 'name':'deadline','type':'text'},
                {'description':'Краткое описание', 'name':'anons','type':'textarea'},
                {'description':'Подробности', 'name':'body','type':'textarea'},
                
            ],
            'tab':'tarifs2'
        },
        # Этапы работ
        {
            'description':'Заголовок блока "Этапы работ"',
            'name':'stages_header',
            'type':'text',
            'tab':'stages'
        },
        {
            'description':'Содержимое блока "Этапы работ"',
            'name':'stages',
            'type':'1_to_m',
            'table':'struct_5759_service_stages',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            'view_type':'list',
            'fields':[
                {'description':'Заголовок', 'name':'header','type':'text'},
                {'description':'Подзаголовок', 'name':'subheader','type':'text'},
                {'description':'Подробности', 'name':'body','type':'textarea'},
                
            ],
            'tab':'stages'
        },
        # Блок "faq"
        {
            'description':'Содержимое блока "вопрос / ответ"',
            'name':'faq',
            'type':'1_to_m',
            'table':'struct_5759_service_faq',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            #'view_type':'list',
            'fields':[
                {'description':'Вопрос', 'name':'header','type':'text'},
                {'description':'Ответ', 'name':'body','type':'textarea'},
                
            ],
            'tab':'faq'
        },
        # Блок "вас заинтересует"
        {
            'description':'Содержимое блока "вас заинтересует"',
            'name':'interest',
            'type':'1_to_m',
            'table':'struct_5759_service_interest',
            'table_id':'id',
            'foreign_key':'service_id',
            'sort':1,
            #'view_type':'list',
            'fields':[
                {
                    'description':'Выберите таб',
                    'name':'interest_id',
                    'type':'select_from_table',
                    'table':'struct_5759_interest',
                    'header_field':'header',
                    'value_field':'id'

                },
            ],
            'tab':'interest'
        },
  ]  
    
}
      


