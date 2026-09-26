

from .ajax import ajax

form={
    'work_table':'bot_subscribe',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Рассылка для telegram-бота',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    'search_on_load':1,
    'ajax':ajax,
    'fields': [ 
        {
            'description':'Название рассылки',
            'add_description':'название рассылке видно только Вам',
            'type':'text',
            'name':'header',    
            'filter_on':True
        },
        {
            'description':'Метка для отправки',
            'add_description':'это метка, с которой был зарегистрирован пользоователь. если не заполнено, то уйдёт всем',
            'name':'mark',
            'type':'text',
            'filter_on':True
        },
        {
            'description':'Дата создания',
            'type':'datetime',
            'name':'registered',
            'read_only':1,
            'filter_on':True
        },
        {
            'description':'Рассылка отправлена',
            'type':'checkbox',
            'name':'send',
            #'read_only':1,
            'filter_on':True
        },        
        {
            'description':'Время отправки',
            'type':'datetime',
            'name':'send_time',
            'read_only':1,
            'filter_on':True
        },
        {
            'descripiption':'Фото',
            'name':'photo',
            'type':'file'
        },
        {
            'description':'Текст рассылки',
            'name':'body',
            'type':'textarea',
            'regexp_rules':[
                '/.+/','Заполните поле текстом рассылки',
            ],
            'after_html':'''В тексте сообщении иожете использовать специальные строки:<br>
                <b>&lt;first_name&gt;</b> - имя<br>
                <b>&lt;last_name&gt;</b> - фамилия<br>

            '''
        },
        {
            'description':'Тип клавиатуры',
            'name':'keyboard_type',
            'type':'select_values',
            'values':[
                {'v':1,'d':'InlineKeyboardMarkup'},
                {'v':2,'d':'ReplyKeyboardMarkup'},
            ],
            'frontend':{'ajax':{'name':'keyboard_type','timeout':100}},
            'tab':'keyboard',
            'not_filter':1
        },
        {
            'description':'Кнопки',
            'name':'keyboard',
            'type':'1_to_m',
            'table':'bot_subscribe_keyboard_items',
            'table_id':'id',
            'foreign_key':'subscribe_id',
            'sort':1,
            'view_type':'list',
            #'before_code':url_before_code,
            'fields':[
                {
                    'description':'Название кнопки',
                    'name':'header',
                    'type':'text',
                },
                {
                    'description':'Действие при нажатии на кнопку',
                    'type':'select_values',
                    'name':'action',
                    'values':[
                        {'v':'3','d':'переход по ссылке'},
                        {'v':'1','d':'переход по ссылке в web-app'},
                        {'v':'2','d':'выполнить команду бота'},
                    ]
                },
                {
                    'description':'Запросить контакт при нажатии кнопки',
                    'type':'checkbox',
                    'name':'request_contact'
                },
                {
                    'description':'Ссылка / Команда',
                    'name':'url',
                    'type':'text',
                },
            ],
            'tab':'keyboard'

        },
        {
            'description':'Отправить после',
            'type':'datetime',
            'name':'send_after',
            'read_only':0,
            'filter_on':True
        },


        

  ]  
    
}
      


