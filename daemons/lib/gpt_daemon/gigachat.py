import requests, json, time
from lib.gpt_daemon.sent_to_cms import sent_to_cms

requests.packages.urllib3.disable_warnings()




gpt_id=2
# access_token будет хранится в этой переменной
time_last_get_token=0; access_token=''

def get_prompt(**argv):

    messages=[{"role":"system","content":argv.get('sys_text')}]
    messages.append({"role":"user","content": argv.get('ask')})

    return {
        "n":1,
        "max_tokens":1000,
        "repetition_penalty": 1.0, # количество повторений слов. при значении >1 будет стараться не повторять слова
        "model": "GigaChat:latest",
        "messages": messages,
        "temperature": argv.get('temperature') or 0.7
    }

    return messages

def get_token(secret_key):
    global time_last_get_token
    global access_token
    if time_last_get_token>int(time.time())+600:
        return False

    headers={
        "Authorization": f"Basic {secret_key}",
        'RqUID': '98df6959-9273-4e7a-a40f-a5dab247d969',
        'Content-type': 'application/x-www-form-urlencoded'
    }
    params = {
        'scope': 'GIGACHAT_API_PERS',
        'grant_type': 'client_credentials',
    }
    time_last_get_token=int(time.time())
    response = requests.request("POST", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth", headers=headers, data=params, verify=False)
    if response.status_code == 200:

        r=json.loads(response.text)
        if 'access_token' in r:
             access_token=r['access_token']

    return False

def get_message(secret_key:str, prompt:dict, try_cnt:int=0):
    global access_token

    if try_cnt>3:
        return '', 'не удалось получить сообщение, кол-во попыток исчерпано'

    if not(access_token):
        # если нет токена -- получаем его
        get_token(secret_key)
        if not(access_token):
            return '', 'Ошибка при получении токена'

    headers={
        "Authorization": f"Bearer {access_token}",
        'Content-type': 'application/json'
    }



    response = requests.request("POST", "https://gigachat.devices.sberbank.ru/api/v1/chat/completions", headers=headers, json=prompt, verify=False)

    if response.status_code == 200:
        r=json.loads(response.text)
        if r:
            result=''
            for c in r['choices']:
                if message:=c.get('message',''):
                    if content:=message.get('content'):
                        result+=content+"\n"

            return result, ''

    elif response.status_code == 401:
        # ошибка авторизации, пробуем получить новый токен
        #print('401')
        get_token(secret_key)
        return get_message(secret_key,prompt, 1)


    else:
        return '',f"status_code: {response.status_code} {response.text}"

def process_gigachat(BaсkendBase:str, db, const:dict, item:dict):

    enable=const.get('gigachat-enable','')
    print('const:',const)

    secret_key=const.get('gigachat-api-secret-key','')

    if enable=="1" and secret_key:
        # Если Giga включен и есть secret_key


        print('item:',item)
        temperature=item.get('temperature')
        if temperature:
            temperature=float(temperature)
        sys_text=item.get('sys_text')

        #to_system=const.get('yandexgpt-to-system','')
        prompt=get_prompt(
            temperature=temperature,
            sys_text=item.get('sys_text'),
            ask=item.get('ask')
        )

        print('prompt:',prompt)
        result, error=get_message(secret_key, prompt)



        if error:
            db.query(
                query="UPDATE crm_gptassist set status=2, error=%s where id=%s",
                values=[error, item['id']]

            )
            # ошибка в cms
            sent_to_cms(BaсkendBase, {'task_id':item['task_id'], 'status':2,  'question': error} )
        elif result:
            #print(result)
            db.query(
                query="UPDATE crm_gptassist set status=1, question=%s, error='' where id=%s",
                values=[result, item['id']]
            )
            # ответ в cms
            sent_to_cms(BaсkendBase, {'task_id':item['task_id'],'status':1, 'question':result} );

            # записываем последнее сообщение, адресованное этому юзеру
            # db.save(
            #     table='last_message_to_user_from_gpt',
            #     replace=1,
            #     data={
            #         'shop_id':shop_id,
            #         'chat_id':chat_id,
            #         'ask': cur_mes,
            #         'question':result,
            #         'gpt_id':gpt_id
            #     }
            # )
            # bot.send_message( chat_id,
            #     result
            # )
            # return True
        else:
            # нет ошибки и нет результата
            # странно
            print('нет ни ошибки ни результата')
        print('result: ',result)

    return False