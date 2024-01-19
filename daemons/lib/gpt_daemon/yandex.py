import requests
import json
from pprint import pprint
from lib.gpt_daemon.sent_to_cms import sent_to_cms
def get_prompt(**argv):

    messages=[{"role":"system","text":argv.get('sys_text')}]




    # последнее сообщение от пользователя
    messages.append({"role":"user","text": argv.get('ask')})
    return {
        "modelUri": f"gpt://{argv.get('cat_id')}/yandexgpt-lite",
        "completationOptions": {
            "stream": False,
            "temperature":argv.get('temperature'), # [0..1] чем ближе к 1, тем оригинальнее ответ модели
            "maxTokens": "1000"
        },
        "messages": messages
    }
def parse_response(response):
    error=''
    result = response.text


    try:

        result = json.loads(result)
        if result.get('error'):
            error=f"Ошибка от сервера Yandex GPT: {result['error']}"

        else:
            result = result['result'].get('alternatives')
            if len(result):
                result = result[0]['message']['text']

            return error, result
    except Exception as e:
        #print(f"ошибка в yandex GPT exception {str(e)}")
        error=f"Ошибка при парсинге ответа от Yandex GPT: {str(e)}"
        return error,result

    return error, result

def process_yandexgpt(BaсkendBase:str, db, const:dict, item:dict):

    enable=const.get('yandexgpt-enable','')

    cat_id=const.get('yandexgpt-cat_id','')
    secret_key=const.get('yandexgpt-api-secret-key','')

    if enable=="1" and cat_id and secret_key:
        # Если YandexGPT включен и есть идентификатор каталога и secret_key

        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

        headers = {
            "Content-type": "application/json",
            "Authorization": f"Api-key {secret_key}"
        }

        temperature=item.get('temperature')
        sys_text=item.get('sys_text')

        #to_system=const.get('yandexgpt-to-system','')
        prompt=get_prompt(
            cat_id=cat_id,
            temperature=item.get(temperature),
            sys_text=item.get('sys_text'),
            ask=item.get('ask')
        )
        #Придумай описание для товара: sonyericsson k750
        #response = requests.post(url, headers=headers, json=prompt)
        #error, result = parse_response(response)
        error, result = ('', "9382982989282892892\ndkosjkjskljkljsjksjsjkj\nioshjsdhjkshjhsjhsjkhsjkhsjhsjkhsjsjhsjkshj")


        if error:
            db.query(
                query="UPDATE crm_gptassist set status=2, error=%s where id=%s",
                values=[error, item['id']]

            )
            # ошибка в cms
            sent_to_cms(BaсkendBase, {'task_id':item['task_id'], 'status':2,  'question': error} )
        elif result:
            print(result)
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