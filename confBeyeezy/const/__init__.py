
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
    'fields':[
        {
            'description':'Слоган',
            'type':'text',
            'name':'slogan'
        },
        {
            'description':'Telegram',
            'type':'text',
            'name':'telegram'
        },        
        {
            'description':'VK',
            'type':'text',
            'name':'vk'
        },
        {
            'description':'Instagram',
            'type':'text',
            'name':'instagram'
        },
        {
            'description':'WhatsApp',
            'type':'text',
            'name':'whatsapp'
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email'
        },

        {
            'description':'Адрес',
            'type':'text',
            'name':'address'
        },
        {
            'description':'Время работы',
            'type':'text',
            'name':'work_time'
        },
        {
            'description':'Доставка и оплата',
            'type':'textarea',
            'name':'delivery_and_paid'
        },
        {
            'description':'Гарантия и возврат',
            'type':'textarea',
            'full_str':1,
            'name':'warranty_and_return'
        },
        {
            'description':'Таблица размеров',
            'type':'textarea',
            'full_str':1,
            'name':'size_table'
        },
        {
            'description':'Телефоны в footer-е',
            'add_description':'разлелите запятой',
            'type':'text',
            'name':'footer_phones'
        },
        {
            'description':'Copyright',
            'type':'text',
            'name':'copyright'
        },
    ]
}
      

