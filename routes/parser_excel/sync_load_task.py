# routes/parser_excel/sync_load_task.py

from celery import current_app as celery_app
from .sync_load import _async_sync_load_task
import asyncio
import traceback
from contextlib import contextmanager

from db import get_db


@contextmanager
def db_connection():
    """
    Контекстный менеджер для синхронного подключения к БД
    """
    db = get_db(sync=1)
    try:
        yield db
    finally:
        if hasattr(db, 'close'):
            db.close()


@celery_app.task(bind=True)
def sync_load_task(self, config: str, fields: list, loaded_filename: str, data_line_number: int, before_load_values: dict = None):
    """
    Celery-задача: запускает асинхронную обработку Excel
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    db=get_db(sync=1)

    try:

        
        result = loop.run_until_complete(
            _async_sync_load_task(
                config=config,
                fields=fields,
                loaded_filename=loaded_filename,
                data_line_number=data_line_number,
                before_load_values=before_load_values
            )
        )
        return result

    except Exception as e:
        return {
            'success': False,
            'errors': [str(e)],
            'traceback': traceback.format_exc()
        }
    finally:
        loop.close()