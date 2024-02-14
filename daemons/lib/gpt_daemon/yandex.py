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

        error=''
        result="""
"But I must explain to you how all this mistaken idea of denouncing pleasure and praising pain was born and I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes, or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but because occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?"

Абзац 1.10.33 "de Finibus Bonorum et Malorum", написанный Цицероном в 45 году н.э.
"At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti atque corrupti quos dolores et quas molestias excepturi sint occaecati cupiditate non provident, similique sunt in culpa qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat."

Английский перевод 1914 года, H. Rackham
"On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains."
        """
        #error, result = parse_response(response)



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