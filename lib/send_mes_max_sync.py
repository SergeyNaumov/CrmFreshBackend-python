from config import config, PRODUCTION
from lib.core import join_ids
import requests
from lib.html_to_markdown import html_to_markdown
from db import get_db  # предположим, что есть синхронная версия get_db

API_TOKEN = config['max']['bot_token']


def send_mes_to_max_id(user_id, message):
    """Отправляет текстовое сообщение в мессенджер Max и возвращает статус отправки (синхронная версия)"""
    if not user_id:
        return False

    try:
        url = f'https://platform-api.max.ru/messages?user_id={user_id}'
        headers = {
            'Authorization': API_TOKEN,
            'Content-Type': 'application/json'
        }
        payload = {
            'text': message,
            'format': 'markdown'
        }

        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=10
            )

            # Max API может возвращать разный формат ответа,
            # поэтому проверяем как статус, так и содержимое
            if response.status_code in (200, 201, 202):
                try:
                    data = response.json()
                    # Если API возвращает поле 'ok' или 'success' — используем его
                    return data.get('ok', data.get('success', True))
                except:
                    # Если ответ не JSON, но статус успешный — считаем отправку успешной
                    return True
            return False

        except (requests.RequestException, requests.Timeout) as e:
            print(f"Ошибка сети при отправке пользователю {user_id}: {str(e)}")
            return False

    except Exception as e:
        print(f"Неожиданная ошибка при отправке пользователю {user_id}: {str(e)}")
        return False


def send_mes_max_managers(ids, message):
    """Отправляет сообщение менеджерам и возвращает список ID, которым не удалось отправить (синхронная версия)"""
    if not ids:
        return []

    # Нормализация входных данных
    if isinstance(ids, (dict, set)):
        ids = list(ids)

    # Получаем данные менеджеров
    db = get_db(sync=1)  # используем синхронную версию
    try:
        managers = db.query(
            query=f"SELECT id, max_id, name FROM manager WHERE id IN ({join_ids(ids)}) AND max_id IS NOT NULL",
            # massive=1  # раскомментируйте если нужно
        )
    except Exception as e:
        print(f"Ошибка при получении данных менеджеров: {str(e)}")
        return ids  # Если ошибка БД, возвращаем все ID как неотправленные

    if not managers:
        return ids

    message = html_to_markdown(message)
    failed_ids = []

    # Отправка сообщений с обработкой ошибок
    for m in managers:

        user_id = m['max_id']
        print('m: ',m, 'user_id: ',user_id)
        manager_id = m['id']

        if PRODUCTION == 'TEST':
            continue  # Пропускаем отправку в тестовом режиме

        success = send_mes_to_max_id(user_id, message)
        if not success:
            failed_ids.append(manager_id)

    # В тестовом режиме не отправляем, но считаем успешными
    if PRODUCTION == 'TEST':
        return []

    return failed_ids