# Миграция: статистика и аудит API управления контентом DS-сайта.
# Применяется вручную на каждой БД, где включён API (см. sites/lib/api).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_api
#
# Идемпотентна (CREATE TABLE IF NOT EXISTS), данные не трогает.
#
#   ds_api_stat -- сводная статистика: агрегат по (проект, день, метод,
#                 сущность, маска ключа). Используется в админке
#                 («API и интеграции» -> Статистика) и для суточного лимита.
#   ds_api_log  -- журнал запросов (аудит). Чистится по сроку отдельной
#                 задачей; по умолчанию хранится 90 дней.
import asyncio

from db import FreshDB
from config import config


DDL = '''
CREATE TABLE IF NOT EXISTS `ds_api_stat` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL DEFAULT '0',
  `day` date NOT NULL,
  `operation` varchar(20) NOT NULL DEFAULT '' COMMENT 'метод API: select/insert/...',
  `entity` varchar(50) NOT NULL DEFAULT '' COMMENT 'сущность (good, catalog, ...)',
  `key_mask` varchar(50) NOT NULL DEFAULT '' COMMENT 'маска ключа: 9f4c…71d2',
  `requests` int unsigned NOT NULL DEFAULT '0',
  `errors` int unsigned NOT NULL DEFAULT '0',
  `rows_affected` int unsigned NOT NULL DEFAULT '0',
  `bytes_in` bigint unsigned NOT NULL DEFAULT '0',
  `bytes_out` bigint unsigned NOT NULL DEFAULT '0',
  `last_ip` varchar(45) NOT NULL DEFAULT '',
  `last_request` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_stat` (`project_id`,`day`,`operation`,`entity`,`key_mask`),
  KEY `project_day` (`project_id`,`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Статистика API управления контентом (агрегат по дням)'
'''

DDL_LOG = '''
CREATE TABLE IF NOT EXISTS `ds_api_log` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL DEFAULT '0',
  `registered` datetime NOT NULL,
  `ip` varchar(45) NOT NULL DEFAULT '' COMMENT 'IP клиента (как пришёл)',
  `ip_hash` char(16) NOT NULL DEFAULT '' COMMENT 'sha256(ip)[:16] для приватности',
  `key_mask` varchar(50) NOT NULL DEFAULT '',
  `operation` varchar(20) NOT NULL DEFAULT '',
  `entity` varchar(50) NOT NULL DEFAULT '',
  `request` mediumtext COMMENT 'тело запроса (усечено)',
  `ok` tinyint unsigned NOT NULL DEFAULT '0',
  `error_code` varchar(50) NOT NULL DEFAULT '',
  `error_message` varchar(500) NOT NULL DEFAULT '',
  `ms` int unsigned NOT NULL DEFAULT '0' COMMENT 'время обработки, мс',
  `rows_affected` int unsigned NOT NULL DEFAULT '0',
  `bytes_in` bigint unsigned NOT NULL DEFAULT '0',
  `bytes_out` bigint unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `project_registered` (`project_id`,`registered`),
  KEY `registered` (`registered`),
  KEY `operation` (`operation`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci
  COMMENT='Журнал запросов API управления контентом'
'''


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  await db.query(query=DDL, values=[], errors=[])
  await db.query(query=DDL_LOG, values=[], errors=[])
  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_api: {db.error_str}')
  print('ds_api_stat, ds_api_log: ok')


if __name__ == '__main__':
  asyncio.run(main())
