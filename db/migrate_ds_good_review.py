# Миграция: отзывы на товар (ds_good_review) — страница /good/{id}.
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_good_review
#
# Идемпотентна. Таблица по образцу ds_reviews/ds_good_faq: отзывы привязаны
# к товару (good_id), проходят модерацию (enabled), порядок — sort.
# Менеджер: поле 1_to_m «Отзывы товара» в карточке ds_good; сайт — блок
# «Отзывы» на странице товара + форма F-04 (пишет сюда при наличии good_id).

import asyncio

from db import FreshDB
from config import config


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  await db.query(
    query='CREATE TABLE IF NOT EXISTS `ds_good_review` ('
          '`id` int(10) unsigned NOT NULL AUTO_INCREMENT,'
          '`project_id` int(10) unsigned NOT NULL DEFAULT 0,'
          '`good_id` int(10) unsigned NOT NULL,'
          "`name` varchar(200) NOT NULL DEFAULT '',"
          '`registered` date DEFAULT NULL,'
          '`rate` tinyint(3) unsigned NOT NULL DEFAULT 5,'
          '`body` text,'
          '`enabled` tinyint(1) NOT NULL DEFAULT 1,'
          '`sort` int(11) NOT NULL DEFAULT 0,'
          'PRIMARY KEY (`id`),'
          'KEY `project_good` (`project_id`,`good_id`)'
          ') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4',
    values=[], errors=[],
  )

  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'migrate_ds_good_review: {db.error_str}')
  print('migrate_ds_good_review: ok (ds_good_review готов)')


if __name__ == '__main__':
  asyncio.run(main())
