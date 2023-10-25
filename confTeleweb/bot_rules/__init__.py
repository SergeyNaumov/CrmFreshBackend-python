from .command import after_html as command_after_html
def url_before_code(form,field):
    #form.pre({'shop':form.shop})
    #field['description']=form.shop['domain']
    shop=form.s.shop
    #form.pre(shop)
    field['fields'][1]['values']=[
        {'d':'ссылка на каталог товаров','v':f'https://{shop["domain"]}/good-catalog'},
        {'d':'ссылка на каталог услуг','v':f'https://{shop["domain"]}/service-catalog'},
    ]
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
    'fields': [ 
        {
            'description':'Команда',
            'type':'text',
            'name':'command',
            'unique':1,
            'after_html':command_after_html,
            #'frontend':{'ajax':{'name':'url','timeout':600}},
            'filter_on':True
        },
        {
            'description':'Текстовое сообщение в ответ',
            'name':'message',
            'type':'textarea',
            'filter_on':True
        },
        {
            'description':'Тип клавиатуры',
            'name':'keyboard_type',
            'type':'select_values',
            'values':[
                {'v':1,'d':'webAppKeyboard'},
                {'v':2,'d':'webAppKeyboard'},
            ]
        },
        {
            'description':'Клавиатура',
            'name':'keyboard',
            'type':'1_to_m',
            'table':'bot_rules_webapp',
            'table_id':'id',
            'foreign_key':'rule_id',
            'sort':1,
            'before_code':url_before_code,
            'fields':[
                {
                    'description':'Текст кнопки',
                    'name':'header',
                    'type':'text',
                },
                {
                    'description':'Запросить контакт',
                    'type':'checkbox',
                    'name':'request_contact'
                },
                {
                    'description':'Ссылка на web-приложение (если нужно)',                
                    'name':'url',
                    'type':'text',
                },
            ]

        }

  ]  
    
}
      


