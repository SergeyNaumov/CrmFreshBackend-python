"""
create table struct_5759_slider(
    id int unsigned primary key auto_increment,
    sort int unsigned not null default '0',
    header varchar(512) not null default '',
    photo varchar(20) not null default ''
) engine=innodb default charset=utf8;
alter table struct_5759_slider add photo_mob varchar(20) not null default ''
"""

from .command import after_html as command_after_html
from .ajax import ajax
async def url_before_code(form,field):
    #form.pre({'shop':form.shop})
    #field['description']=form.shop['domain']
    shop=getattr(form.request.state,'shop',None) or {}
    #form.pre(shop)
    field['fields'][1]['values']=[
        {'d':'ссылка на каталог товаров','v':f'https://{shop.get("domain","")}/good-catalog'},
        {'d':'ссылка на каталог услуг','v':f'https://{shop.get("domain","")}/service-catalog'},
    ],

form={
    'work_table':'bot_rules',
    'work_table_id':'id',
    #'work_table_foreign_key':'bot_id',
    #'work_table_foreign_key_value':1,
    'title':'Правила бота',
    'sort':1,
    'tree_use':0,
    'header_field':'command',
    'default_find_filter':'',
    'form_wide':1,
    'search_on_load':1,
    'wide_form':True,
    'cols':[
        [
            {'description':'Команда и сообщение','name':'command','hide':False,'wide':True},

        ],
        [
            {'description':'Клавиатура','name':'keyboard','hide':False}
        ]
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
            'filedir': '', # заполняется в events,
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
                {'v':1,'d':'Клавиатура сообщений (InlineKeyboardMarkup)'},
                {'v':2,'d':'Клавиатура ответов (ReplyKeyboardMarkup)'},
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
        {
            'description':'Cкрыть клавиатуру, как только она будет использована',
            'name':'one_time_keyboard',
            'type':'checkbox',
            'tab':'keyboard',
            'not_filter':1,
        },
        {
            'description':'Количество колонок',
            'type':'text',
            'name':'cols',
            'tab':'keyboard',
            'not_filter':1,
            'regexp_rules':[
                r'/^[1-9]$/','Нужно указать целое число'
            ]
        },
        {
            'description':'Кнопки',
            'name':'keyboard',
            'type':'1_to_m',
            'table':'bot_rules_keyboard_items',
            'table_id':'id',
            'foreign_key':'rule_id',
            'sort':1,
            #'view_type':'list',
            'cols':1,
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
                        {'v':'1','d':'переход по ссылке в web-app'},
                        {'v':'3','d':'переход по ссылке'},
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
      


