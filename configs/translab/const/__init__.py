
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
            'description':'Телефон в шапке',
            'type':'text',
            'name':'top_phone',
            'full_str':1,
            'tab':'main',
        },
        {
            'description':'Адрес',
            'type':'text',
            'name':'address',
            'full_str':1,
            'tab':'main',
        },


    ]
}
      

