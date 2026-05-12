import requests
import json
from config import config
import os
def send_sync(manager_id:int, message:str):
    # Синхронная отправка сообщений в messenger
    print('send_sync: ',manager_id, message)

    messenger_url=os.getenv('MESSENGER_URL') or config['messenger_url']
    print('url:' ,messenger_url)
    response = requests.post(
        messenger_url,
        data=json.dumps({"user_id": manager_id, "message": message}),
        headers={"Content-Type": "application/json"},
        timeout=10  # таймаут 10 секунд
    )

    response.raise_for_status()  # выбросит исключение для 4xx/5xx статусов

    print(f"Успех! Status Code: {response.status_code}")
    #return response.json()




