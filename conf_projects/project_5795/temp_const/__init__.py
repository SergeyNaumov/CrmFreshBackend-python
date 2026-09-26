
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
        {'name':'maindata','description':'Общие данные'},
        {'name':'main','description':'Главная страница'},
        {'name':'contacts','description':'Контакты'},
    ],
    'fields':[
        # Общие данные
        {'name':'companyname','type':'text','description':'Наименование компании','tab':'maindata'},
        {'name':'logo','type':'file','description':'Логотип','add_description':'в формате svg','tab':'maindata'},
        {'name':'email_for_feedback','type':'text','description':'Email для обратной связи','add_description':'адрес, на который будут приходить все сообщения из форм обратной связи','tab':'maindata'},
        {'name':'email_for_zakaz','type':'text','description':'Email для заказов','add_description':'адрес, на который будут приходить все заказы','tab':'maindata'},

        # Главная страница
        {'name':'main_prefix','type':'wysiwyg','description':'Текст перед промо-изображением','tab':'main'},
        {'name':'main_promo','type':'file','description':'Промо-изображение','add_description':'подготовленное изображение 400x210','tab':'main'},
        {'name':'main_postfix','type':'wysiwyg','description':'Текст после промо-изображения','tab':'main'},

        # Контакты
        {'name':'work_time','type':'text','description':'Время работы','tab':'contacts'},
        {'name':'address','type':'text','description':'Адрес','tab':'contacts'},
        {'name':'email','type':'text','description':'Email','tab':'contacts'},
        {'name':'phones','type':'text','description':'Телефоны', 'add_description':'можно указать несколько, разделив запятой','tab':'contacts'},
        {'name':'map','type':'textarea','description':'Код для карты','tab':'contacts'},

    ]
}
      

