
form={
    'work_table':'const',
    'work_table_id':'id',
    #'work_table_foreign_key':'template_id',
    #'work_table_foreign_key_value':'id',
    'title':'Константы для сайта',
    'filedir':'./files',   # Каталог для сохранения файлов
    'filedir_http':'/files',
    'name_field':'name',
    'value_field':'value',
    'default_find_filter':'header',
    'tabs':[
        {'name':'main','description':'Общие данные'},
        {'name':'blocks','description':'Текстовые блоки'},
        {'name':'price','description':'Цены'},
    ],
    'fields':[
        {
            'description':'Слоган',
            'type':'text',
            'name':'slogan',
            'tab':'main',
            #'add_description':'поясняющий текст'
        },
        {
            'description':'Telegram',
            'type':'text',
            'name':'telegram',
            'tab':'main'
        },        
        {
            'description':'VK',
            'type':'text',
            'name':'vk',
            'tab':'main'
        },
        {
            'description':'Instagram',
            'type':'text',
            'name':'instagram',
            'tab':'main'
        },
        {
            'description':'WhatsApp',
            'type':'text',
            'name':'whatsapp',
            'tab':'main'
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
            'tab':'main'
        },

        {
            'description':'Адрес',
            'type':'text',
            'name':'address',
            'tab':'main'
        },
        {
            'description':'Время работы',
            'type':'text',
            'name':'work_time',
            'tab':'main'
        },
        {
            'description':'Телефоны в footer-е',
            'add_description':'разлелите запятой',
            'type':'text',
            'name':'footer_phones',
            'tab':'main'
        },
        {
            'description':'Copyright',
            'type':'text',
            'name':'copyright',
            'tab':'main'
        },
        {
            'description':'Доставка и оплата',
            'type':'textarea',
            'name':'delivery_and_paid',
            'tab':'blocks'
        },
        {
            'description':'Гарантия и возврат',
            'type':'textarea',
            'full_str':1,
            'name':'warranty_and_return',
            'tab':'blocks'
        },
        {
            'description':'Таблица размеров',
            'type':'textarea',
            'full_str':1,
            'name':'size_table',
            'tab':'blocks'
        },
        {
            'description':'Прибавить к цене',
            'name':'price_add',
            'type':'text',
            'tab':'price'
        },
        {
            'description':'Цену умножить на',
            'name':'price_multiply',
            'type':'text',
            'tab':'price'
        },

    ]
}
      

