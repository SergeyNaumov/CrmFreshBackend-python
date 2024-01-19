# Правила для системы
rules={
    'WS':'ws://localhost:5000/gpt-assist/ws', # для вебсокета
    'configs':{
        'good':{
            'fields':[ # Настройка полей для GPT
                {'name':'anons', 'description':'Анонс'},
                {'name':'body', 'description':'Подробное описание','type':'wysiwyg'},
            ]
        }
    },
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


def get_cnst(shop_id:int, db):
    # получение GPT-констант
    cnst={}
    for c in db.query( query="select name,value from const where shop_id=%s and name like %s", values=[shop_id, 'yandexgpt%']):
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

# Правила поведения для GPT
def gptassist_rules(s):
    shop_id=s.shop_id ; db=s.db
    cnst=get_cnst(shop_id, db)



    initYandexGPT(rules, cnst)
    return rules







