# Правила для системы
rules={
    #'WS':'ws://localhost:3010/gpt-assist/ws', # для вебсокета
    # заполняются в функции gptassist_rules:
    'gpt_list':[],
    'engines':{ }
}

"""
1 - YandexGPT
2 - GigaChat

Example:
rules={
    'get_socket_name':get_socket_name,
    'configs':{
        'good':{
            'fields':[ # Настройка полей для GPT
                {'name':'anons', 'description':'Анонс'},
                {'name':'body', 'description':'Подробное описание'},
            ]
        }
    },
    # заполняются в функции gptassist_rules:
    'gpt_list':[{v:1,d:'YandexGPT'}],
    'engines':{
        'YandexGPT':
    }
}
"""


async def get_cnst(project_id:int, db):
    # получение GPT-констант
    cnst={}
    for c in await db.query( query="select name,value from const where project_id=%s and (name like %s or name like %s)", values=[project_id, 'yandexgpt%', 'gigachat%']) or []:
        cnst[c['name']]=c['value']
    return cnst

def initYandexGPT(rules: dict, cnst: dict):
    YandexGPT={}
    label='YandexGPT'
    #print('cnst:',cnst)
    if cnst.get('yandexgpt-enable')=='1':
        #print('Yandex Enable')
        # YandexGPT
        cat_id=cnst.get('yandexgpt-cat_id')
        secret_key=cnst.get('yandexgpt-api-secret-key')
        #print(f'cat_id: {cat_id}')
        if cat_id and secret_key:
            rules['gpt_list'].append({'v': 1, 'd':label}) # зазвание в списке у пользователя
            rules['engines']['YandexGPT']={
                'on':True,'cat_id': cat_id, 'secret_key':secret_key
            }
        else:
            rules['engines']['YandexGPT']={
                'on':False, 'cat_id': '', 'secret_key':''
            }

    return YandexGPT

def initGigachat(rules: dict, cnst: dict):
    result={}
    label='GigaChat'
    #print('cnst:',cnst)
    if cnst.get('gigachat-enable')=='1':
        print('Giga Enable')
        # YandexGPT

        secret_key=cnst.get('gigachat-api-secret-key')
        #print(f'cat_id: {cat_id}')
        if secret_key:
            rules['gpt_list'].append({'v': 2, 'd':label}) # зазвание в списке у пользователя
            rules['engines']['GigaChat']={
                'on':True, 'secret_key':secret_key
            }
        else:
            rules['engines']['GigaChat']={
                'on':False, 'secret_key':secret_key
            }
    else:
        print('Giga Disable')
    return result

# Правила поведения для GPT
async def gptassist_rules(request):
    project=request.state.project['project_id'] ; db=request.state.engine.db
    domain=await db.query(
        query="select domain from domain where project_id=%s",
        values=[project],
        onevalue=1

    )
    print('domain:',domain)
    if domain:
        rules['WS']=f'wss://{domain}/manager/backend/gpt-assist/ws'
    else:
        rules['WS']=f'wss://digitalstrateg.ru/backend/gpt-assist/ws'

    cnst=await get_cnst(project, db)

    rules['gpt_list']=[]
    initYandexGPT(rules, cnst)
    initGigachat(rules, cnst)
    #print('rules:',rules)
    return rules







