
import asyncio
import aiohttp
import telebot

from config import config, PRODUCTION
from lib.core import join_ids
from lib.html_to_markdown import html_to_markdown
from db import get_db
import vk_api
from vk_api.utils import get_random_id
API_TOKEN = config['telegram']['bot_token']
VK_API_TOKEN = config['vk']['bot_token']
bot = telebot.TeleBot(API_TOKEN)
vk_session = vk_api.VkApi(token=VK_API_TOKEN)
# Инициализация бота и диспетчера


async def send_mes_to_chat_id(chat_id, message):
    """Отправляет сообщение в Telegram и возвращает статус отправки"""
    if not(chat_id):
        return False
    try:
        url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
        payload = {
            'chat_id': int(chat_id),
            'text': message,
            'parse_mode': 'Markdown'
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('ok', False)
                    return False
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                print(f"Ошибка сети при отправке в chat_id {chat_id}: {str(e)}")
                return False
    except Exception as e:
        print(f"Неожиданная ошибка при отправке в chat_id {chat_id}: {str(e)}")
        return False

async def send_mes_tg_managers(ids, message):
    """Отправляет сообщение менеджерам и возвращает список ID, которым не удалось отправить"""
    if not ids:
        return []

    # Нормализация входных данных
    if isinstance(ids, (dict, set)):
        ids = list(ids)

    # Получаем данные менеджеров
    db = get_db()
    try:
        managers = await db.query(
            query=f"SELECT id, telegram_id, name FROM manager WHERE id IN ({join_ids(ids)}) AND telegram_id IS NOT NULL",
            # massive=1
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
        chat_id = m['telegram_id']
        manager_id = m['id']

        if PRODUCTION == 'TEST':
            continue  # Пропускаем отправку в тестовом режиме

        success = await send_mes_to_chat_id(chat_id, message)
        if not success:
            failed_ids.append(manager_id)

    # В тестовом режиме не отправляем, но считаем успешными
    if PRODUCTION == 'TEST':
        return []

    return failed_ids


async def send_mes_to_user_id(user_id, message):
    """Отправляет сообщение в VK и возвращает статус отправки"""
    if not(user_id):
        return False
    try:
        vk = vk_session.get_api()
        vk.messages.send(user_id=int(user_id), message=message, random_id=get_random_id())
    except Exception as e:
        print(f"Неожиданная ошибка при отправке в vk user_id {user_id}: {str(e)}")
        return False


async def send_mes_vk_managers(ids, message):
    """Отправляет сообщение менеджерам и возвращает список ID, которым не удалось отправить"""
    if not ids:
        return []

    # Нормализация входных данных
    if isinstance(ids, (dict, set)):
        ids = list(ids)

    # Получаем данные менеджеров
    db = get_db()
    try:
        managers = await db.query(query=f"SELECT id, vk_id, name FROM manager WHERE id IN ({join_ids(ids)}) AND vk_id IS NOT NULL AND vk_id <> ''")
    except Exception as e:
        print(f"Ошибка при получении данных менеджеров: {str(e)}")
        return ids  # Если ошибка БД, возвращаем все ID как неотправленные

    if not managers:
        return ids

    message = html_to_markdown(message)

    # Отправка сообщений с обработкой ошибок
    for m in managers:
        user_id = m['vk_id']
        if PRODUCTION == 'TEST':
            continue  # Пропускаем отправку в тестовом режиме
        await send_mes_to_user_id(user_id, message)


# async def send_mes_to_chat_id(chat_id, message):
#     try:

#         url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
#         payload = {
#             'chat_id': int(chat_id),
#             'text': message,
#             'parse_mode': 'Markdown'
#         }
#         headers = {
#             'Content-Type': 'application/json'
#         }
#         async with aiohttp.ClientSession() as session:
#             async with session.post(url, json=payload, headers=headers) as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     if data['ok']:
#                         print("Сообщение успешно отправлено")
#                     else:
#                         print(f"Ошибка при отправке сообщения: {data}")
#                 else:
#                     error_text = await response.text()
#                     print(f"Ошибка HTTP: {response.status} {error_text}")
#     except Exception as e:
#         print(f"Ошибка при отправке сообщения: {e}")
#     #finally:
#     #    await session.close()  # Явное закрытие сессии

# async def send_mes_tg_managers(ids, message):
#     print('ids:', ids)
#     """
#         ids - список id-шников менеджеров, которым нужно отправить сообщение в telegram
#         message - sended message (markdown)
#         Функция возвращает список тех id-шнико, по которым отправка невозможна
#     """
#     if isinstance(ids, (dict, set)):  # Проверяем, является ли объект словарём или множеством
#         ids = list(ids)  # Преобразуем в список по ключам (для словаря) или элементам (для множ

#     if not len(ids):
#         return ids

#     db=get_db()
#     managers = await db.query(
#         query=f"select id, telegram_id, name from manager WHERE id in ({join_ids(ids)}) and telegram_id is not null",
#         #massive=1
#     )

#     if len(managers):
#         message=html_to_markdown(message)
#         elements_to_remove_set=set()
#         for m in managers:
#             elements_to_remove_set.add(m['id'])
#             chat_id=m['telegram_id']
#             # отправляем сообщения
#             #print(f"telegram sending to: {m['name']} ({chat_id})")
#             #print(message)
#             old_message=message
#             if PRODUCTION=='TEST':
#                 return ids
#                 #chat_id=295470393
#                 #message+=f"\n\n{m['name']} ({chat_id})"

#             await send_mes_to_chat_id(chat_id,message)
#             message=old_message

#         #return [item for item in ids if item not in elements_to_remove_set]
#     return ids

    # ids=[...] список менеджеров, которым отправляем

    #
