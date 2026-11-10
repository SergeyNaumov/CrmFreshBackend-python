# Миграция: ds_text.full_width — текстовая страница «на всю ширину»
# (соглашения, регламенты: контент тянется на 100% ширины .container
# вместо узкой колонки .custom-page 820px).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_full_width
#
# Идемпотентна (проверка information_schema перед ADD COLUMN).
#
# Читает движок сайта: sites/lib/dsengine/__init__.py::get_text_page
# (SELECT full_width), рендер — templates/2026/ds-constructor/page/text_page.html
# (.custom-page--full). Поле карточки — конфиг configs/svcmsmanager/ds_text.

import asyncio

from config import config
from db.freshdb import FreshDB

TABLE = 'ds_text'
COLUMN = 'full_width'
DDL = "tinyint(1) NOT NULL DEFAULT 0"


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  rows = await db.query(
    query='SELECT column_name AS col FROM information_schema.columns '
          'WHERE table_schema=DATABASE() AND table_name=%s',
    values=[TABLE], errors=[],
  ) or []
  existing = {str(r['col']).lower() for r in rows}
  if COLUMN not in existing:
    await db.query(
      query='ALTER TABLE `%s` ADD COLUMN `%s` %s AFTER mode' % (TABLE, COLUMN, DDL),
      values=[], errors=[],
    )
  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_full_width: {db.error_str}')
  print('ds_full_width: %s.%s: ok' % (TABLE, COLUMN))


if __name__ == '__main__':
  asyncio.run(main())
