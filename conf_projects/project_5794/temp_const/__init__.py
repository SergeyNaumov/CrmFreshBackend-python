
form={
    'work_table':'const',
    'work_table_id':'const_id',
    'work_table_foreign_key':'template_id',
    'work_table_foreign_key_value':'id',
    'title':'Константы для сайта',
    'filedir':'./files',   # Каталог для сохранения файлов
    'filedir_http':'/files',
    'name_field':'name',
    'value_field':'value',
    'default_find_filter':'header',
    'tabs':[
        {'name':'main','description':'Общие данные'},
        
        {'name':'header','description':'Шапка'},
        {'name':'footer','description':'Footer'},
        {'name':'blocks','description':'Блоки'},
        {'name':'perpage','description':'Расстраничивание'},
    ],
    'fields':[
        # Общие данные
        {'name':'company','type':'text','description':'Название компании','tab':'main'},
        
        #{'name':'phone','type':'text','description':'Основной телефон','tab':'contacts'},
        {'name':'email_for_feedback','type':'text','description':'Email для обратной связи','tab':'main'},
        {'name':'good_thumbnail','type':'file','description':'Фото-заглушка товара','tab':'main'},
        {'name':'team_thumbnail','type':'file','description':'Фото-заглушка сотрудника','tab':'main'},
        
        
        
        {'name':'warning_on','type':'checkbox','description':'Включить блок "внимание"','tab':'header'},
        {'name':'warning','type':'textarea','description':'Текст в блоке "внимание"','tab':'header'},
        {'name':'work_time','type':'textarea','description':'Часы работы','tab':'header'},
        #{'name':'logo','type':'file','description':'Логотип','add_description':'в формате svg','tab':'header'},
        {'name':'address','type':'text','description':'Адрес','add_description':'Фактический адрес','tab':'header'},
        {'name':'fact_address','type':'text','description':'Фактический адрес','tab':'header'},
        {'name':'ur_address','type':'text','description':'Юридический адрес','tab':'header'},
        #{'name':'email','type':'text','description':'Email','tab':'header'},
        #{'name':'emails_all','type':'textarea','description':'Список Email-ов','tab':'header'},

        #{'name':'phones_all','type':'textarea','description':'Список телефонов','tab':'footer'},
        # Блоки
        #{'name':''}
        {'name':'copyright','type':'text','description':'copyright', 'tab':'footer'},
        {
            'description':'Мы используем cookie',
            'name':'cookie_txt',
            'type':'textarea',
            'tab':'footer'
        },
        {'name':'oferta','type':'textarea','description':'Оферта','tab':'footer'},
        {'name':'counter','type':'textarea','description':'Счётчики сайта','tab':'footer'},

        {'name':'video_perpage','type':'text','description':'Кол-во записей на странице "видео"', 'tab':'perpage'},
        {
            'name':'documents_perpage',
            'type':'text',
            'description':'Кол-во записей на странице "документы"',
            'tab':'perpage'
        },
        {
            'name':'video_perpage',
            'type':'text',
            'description':'Кол-во записей на странице "видео"',
            'tab':'perpage'
        },

        # Блоки
        {
            'description':'Текст над страницей "услуги"',
            'name':'block_before_servpage',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст над страницей "каталог"',
            'name':'block_before_catpage',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Над блоком "каталог"',
            'name':'block_catalog_before',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Под блоком "каталог"',
            'name':'block_catalog_after',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст над страницей "документы"',
            'name':'block_before_docpage',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст над страницей "видео"',
            'name':'block_before_vidpage',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст над формой "не нашли, что искали?"',
            'name':'block_before_form_send_request',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст над блоком "схема работы"',
            'name':'block_before_scheme',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Блок "Оплата и доставка"',
            'name':'block_paid_delivery',
            'type':'wysiwyg',
            'tab':'blocks'
        },
        {
            'description':'Текст в блоке "вас может заинтересовать" (услуги)',
            'name':'interest_services',
            'type':'wysiwyg',
            'tab':'blocks'
        },

        # 
        # Главная страница
        # {'name':'main_prefix','type':'wysiwyg','description':'Текст перед промо-изображением','tab':'main'},
        # {'name':'main_promo','type':'file','description':'Промо-изображение','add_description':'подготовленное изображение 400x210','tab':'main'},
        # {'name':'main_postfix','type':'wysiwyg','description':'Текст после промо-изображения','tab':'main'},

        # # Контакты
        # {'name':'work_time','type':'text','description':'Время работы','tab':'contacts'},
        # {'name':'address','type':'text','description':'Адрес','tab':'contacts'},
        # {'name':'email','type':'text','description':'Email','tab':'contacts'},
        # {'name':'phones','type':'text','description':'Телефоны', 'add_description':'можно указать несколько, разделив запятой','tab':'contacts'},
        # {'name':'map','type':'textarea','description':'Код для карты','tab':'contacts'},

    ]
}
      

