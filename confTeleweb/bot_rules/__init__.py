from .command import after_html as command_after_html
from .ajax import ajax
def url_before_code(form,field):
    #form.pre({'shop':form.shop})
    #field['description']=form.shop['domain']
    shop=form.s.shop
    #form.pre(shop)
    field['fields'][1]['values']=[
        {'d':'ссылка на каталог товаров','v':f'https://{shop["domain"]}/good-catalog'},
        {'d':'ссылка на каталог услуг','v':f'https://{shop["domain"]}/service-catalog'},
    ],

form={
    'work_table':'bot_rules',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Правила поведения бота',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'search_on_load':1,
    'form_wide':1,
    'cols':[
        [
            {'description':'Команда и сообщение','name':'command','hide':False,'wide':True},
            {'description':'Клавиатура','name':'keyboard','hide':False}
        ],
    ],
    'ajax':ajax,
    'fields': [ 
        {
            'description':'Команда',
            'type':'text',
            'name':'command',
            'unique':1,
            'after_html':command_after_html,
            #'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True,
            'tab':'command'
        },
        {
            'description':'Изображение',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_<%shop_id%>/good_photos',
            'filter_on':True,
            'tab':'command'
        },
        {
            'description':'Текстовое сообщение в ответ',
            'name':'message',
            'type':'textarea',
            'filter_on':True,
            'tab':'command'
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
            'description':'Изменить размер клавиатуры по вертикали для оптимального соответствия ',
            'name':'resize_keyboard',
            'type':'checkbox',
            'tab':'keyboard',
            'not_filter':1
        },  # только для reply
        # {
        #     'description':'Всегда показывать (не скрывать) клавиатуру',
        #     'name':'is_persistent',
        #     'type':'checkbox',
        #     'tab':'keyboard',
        #     'not_filter':1
        # },
        {
            'description':'Cкрыть клавиатуру, как только она будет использована',
            'name':'one_time_keyboard',
            'type':'checkbox',
            'tab':'keyboard',
            'not_filter':1,
        },

        {
            'description':'Кнопки',
            'name':'keyboard',
            'type':'1_to_m',
            'table':'bot_rules_keyboard_items',
            'table_id':'id',
            'foreign_key':'rule_id',
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

        }

  ]  
    
}
      


