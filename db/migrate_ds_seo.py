# Миграция: SEO-поля карточки у конструкторных сущностей (ds_*).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_seo
#
# Идемпотентна (ADD COLUMN IF NOT EXISTS). Добавляет в ds_news, ds_article,
# ds_good, ds_service и ds_catalog колонки:
#
#   promo_title        varchar(255) — <title> страницы (без «— orgname»);
#   promo_description  varchar(512) — <meta name="description">;
#   promo_keywords     varchar(512) — <meta name="keywords">.
#
# Редактируются в карточке сущности («Title/Description/Keywords (SEO)»,
# конфиги configs/svcmsmanager/ds_*). Читает движок сайта:
# sites/lib/dsengine/process_page.py::_set_seo (1. карточка → 2. таблица
# promo → 3. автогенерация из заголовка). Пустое значение = фолбэк.

import asyncio

from config import config
from db.freshdb import FreshDB

TABLES = ('ds_news', 'ds_article', 'ds_good', 'ds_service', 'ds_catalog')

# ADD COLUMN IF NOT EXISTS — поддерживается MariaDB 10.0+ (прод 11.8).
DDL = [
    "ALTER TABLE `%s` "
    "ADD COLUMN IF NOT EXISTS `promo_title` varchar(255) NOT NULL DEFAULT '' "
    "AFTER `anons`, "
    "ADD COLUMN IF NOT EXISTS `promo_description` varchar(512) NOT NULL DEFAULT '' "
    "AFTER `promo_title`, "
    "ADD COLUMN IF NOT EXISTS `promo_keywords` varchar(512) NOT NULL DEFAULT '' "
    "AFTER `promo_description`" % table
    for table in TABLES
]


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  for query in DDL:
    await db.query(query=query, values=[], errors=[])
  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_seo: {db.error_str}')
  print('ds_seo: ' + ', '.join(TABLES) + ': ok')


if __name__ == '__main__':
  asyncio.run(main())
