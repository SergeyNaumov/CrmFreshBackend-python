# Миграция: очередь фоновых задач (см. lib/background.py).
# Применяется вручную на каждой БД, где включены фоновые воркеры.
#
#   export config=config_svcms_manager
#   .venv/bin/python db/migrate_crm_background.py
#
# Идемпотентна (CREATE TABLE IF NOT EXISTS), данные не трогает.
import asyncio

from db import FreshDB
from config import config


DDL = '''
CREATE TABLE IF NOT EXISTS `crm_background` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `task_id` char(40) NOT NULL DEFAULT '' COMMENT 'публичный идентификатор задачи',
  `config` varchar(50) NOT NULL DEFAULT '' COMMENT 'имя конфигурации (например svcmsadmin)',
  `action` varchar(100) NOT NULL DEFAULT '' COMMENT 'обработчик задачи',
  `params` mediumtext COMMENT 'json параметров',
  `admin_id` int unsigned DEFAULT NULL,
  `project_id` int unsigned DEFAULT NULL,
  `status` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '0-new 1-running 2-done 3-error 4-canceled',
  `progress` tinyint unsigned NOT NULL DEFAULT '0' COMMENT 'процент выполнения 0-100',
  `message` varchar(512) NOT NULL DEFAULT '' COMMENT 'текущий шаг',
  `result` mediumtext COMMENT 'json результата',
  `error` varchar(512) NOT NULL DEFAULT '' COMMENT 'текст ошибки',
  `worker` varchar(64) NOT NULL DEFAULT '' COMMENT 'токен захвата задачи',
  `registered` datetime DEFAULT CURRENT_TIMESTAMP,
  `started` datetime DEFAULT NULL,
  `finished` datetime DEFAULT NULL,
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `heartbeat` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `status_id` (`status`,`id`),
  KEY `worker_status` (`worker`,`status`),
  KEY `admin_id` (`admin_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='Очередь фоновых задач'
'''


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  await db.query(query=DDL, values=[], errors=[])
  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'crm_background: {db.error_str}')
  print('crm_background: ok')


if __name__ == '__main__':
  asyncio.run(main())
