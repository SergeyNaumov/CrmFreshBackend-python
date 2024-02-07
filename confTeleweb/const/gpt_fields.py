def add_gpt_fields(form):
    add_fields=[
        {
            'description':'Использовать GPT для ответов в боте',
            'type':'select',
            'name':'gpt_in_bot',
            'values':[
                {'v':'','d':'Не использовать'},
                {'v':'1','d':'Использовать YandexGPT'},
                {'v':'2','d':'Использовать GigaChat'},
            ]
        },
        {
            'description':'YandexGPT',
            'type':'header'
        },
        {
            'description':'Включить YandexGPT',
            'type':'checkbox',
            'name':'yandexgpt-enable'
        },
        {
            'description':'ID-каталога',
            'type':'text',
            'name':'yandexgpt-cat_id'
        },
        {
            'description':'Yandex API secret key',
            'type':'text',
            'name':'yandexgpt-api-secret-key'
        },
        {
            'description':'Текст для предварительного обучения',
            'type':'textarea',
            'name':'yandexgpt-to-system'
        },
        {
            'description':'GigaChat',
            'type':'header'
        },
        {
            'description':'Включить GigaChat',
            'type':'checkbox',
            'name':'gigachat-enable'
        },
        {
            'description':'GigaChat API secret key',
            'type':'text',
            'name':'gigachat-api-secret-key'
        },
        {
            'description':'Текст для предварительного обучения',
            'type':'textarea',
            'name':'gigachat-to-system'
        },
    ]

    for f in add_fields:
        f['tab']='gpt'
        form.fields.append(f)