def add_gpt_fields(form):
    form.tabs.append(
        {'name':'bot','description':'Настройки бота'},
    )
    add_fields=[
        {
            'description':'Общие настройки',
            'type':'header'
        },
        {
            'description':'Какой GPT-ассистента использовать для вопросов пользователей?',
            'type':'select',
            'name':'gpt_in_bot',
            'values':[
                {'v':'','d':'Никакой'},
                {'v':'1','d':'Использовать YandexGPT'},
                {'v':'2','d':'Использовать GigaChat'},
            ]
        },
        {
            'description':'Пересылать администратору бота диалог между GPT-ассистентом и клиентом',
            'full_str':1,
            'type':'checkbox',
            'name':'gpt_resend_to_adm'
        },
        {
            'description':'Пересылать администратору сообщения от клиента (если GPT-ассистент не смог ответить)',
            'full_str':1,
            'type':'checkbox',
            'name':'resend_usermes_to_adm'
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
        f['tab']='bot'
        form.fields.append(f)