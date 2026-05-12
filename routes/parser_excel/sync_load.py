# sync_load.py

from db import get_db
from .load import check_before_load_values
from .load_parser_from_config import load_parser_from_config
from .go_parse import go_parse

import os
import traceback  # ✅ Добавлен импорт

# Импортируем ЕДИНСТВЕННЫЙ экземпляр celery_app
#from lib.celery_conf.config import celery_app


print("🟡 [DEBUG] МОДУЛЬ sync_load.py ЗАГРУЖАЕТСЯ...")
# Устанавливаем переменную окружения
os.environ['CELERY_WORKER_RUNNING'] = 'true'





async def _async_sync_load_task(config: str, fields: list, loaded_filename: str, data_line_number: int, before_load_values: dict = None):
    """
    Асинхронная логика задачи
    """
    db=get_db()
    try:
        config_folder = 'conf'  # или: sysconfig.get('config_folder') or 'conf'

        # ✅ Асинхронный вызов
        parser, errors = await load_parser_from_config(config_folder, config_folder, {'config': config})
        if errors:
            return {'success': False, 'errors': errors}

        # Проверяем before_load_values
        R = {'before_load_values': before_load_values}
        if err := check_before_load_values(errors, parser, R):
            return {'success': False, 'errors': [err]}

        # Подготовка hash_fields
        hash_fields = {}
        for f in fields:
            if selected := f.get('selected'):
                hash_fields[selected] = f.get('name')

        # Создаём loopback
        async def get_exists(data):
            where = []
            values = []
            unique_fields = parser.get('unique_fields', [])
            work_table_id = parser['work_table_id']

            for field_name in unique_fields:
                if field_name in data:  # ✅ Правильно: проверяем наличие в data
                    where.append(f"{field_name}=%s")
                    values.append(data[field_name])

            if where:
                if exists := await db.query(
                    query=f"SELECT {work_table_id} FROM {parser['work_table']} WHERE {' AND '.join(where)} LIMIT 1",
                    values=values,
                    onerow=1
                ):
                    return exists
            return None

        before_loopback_func = parser.get('before_loopback')

        async def loopback(data):
            if not data:
                return None

            if before_loopback_func:
                await before_loopback_func(data)

            if before_load_values:
                data.update(before_load_values)

            exists = await get_exists(data)
            if exists:
                pk = exists[parser['work_table_id']]
                await db.save(
                    table=parser['work_table'],
                    data=data,
                    update=1,
                    where=f"{parser['work_table_id']}=%s",
                    values=[pk]
                )
                return 'update'
            else:
                await db.save(
                    table=parser['work_table'],
                    data=data
                )
                return 'insert'

        result_text = []

        # ✅ Асинхронный вызов go_parse
        message = await go_parse(
            filename=loaded_filename,
            hash_fields=hash_fields,
            tmp_dir=parser['tmp_dir'],
            data_line_number=data_line_number,
            loopback=loopback,
            result_text=result_text
        )

        return {
            'success': True,
            'message': message,
            'result_text': '\n'.join(result_text)
        }

    except Exception as e:
        return {
            'success': False,
            'errors': [str(e)],
            'traceback': traceback.format_exc()
        }