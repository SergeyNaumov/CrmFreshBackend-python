# Миграция: сервис «Текстовые блоки» (ds_text_block).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_text_block
#
# Идемпотентна. Делает:
#   1. CREATE TABLE IF NOT EXISTS ds_text_block (code -> header/body,
#      unique project_id+code) — тексты блоков конструктора (about,
#      contact_form), редактируемые и из /manager, и из конструктора.
#   2. Опция ds_options «Текстовые блоки» (config ds_text_block, после
#      «Статичных страниц») + включение всем проектам, у которых включён
#      ds_text.
#   3. Backfill: тексты блоков из domain_page.blocks всех проектов —
#      в таблицу (lib/svcmsmanager/text_blocks.py::upsert_from_doc).
#
# Движок сайта таблицу не читает (рендер — JSON блоков), синхронизация:
# lib/svcmsmanager/text_blocks.py.

import asyncio
import json

from db import FreshDB
from config import config

from lib.svcmsmanager.text_blocks import TEXT_BLOCK_MAP, upsert_from_doc

DDL = '''
CREATE TABLE IF NOT EXISTS `ds_text_block` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `project_id` int unsigned NOT NULL DEFAULT 0,
  `code` varchar(50) NOT NULL DEFAULT '',
  `header` varchar(255) NOT NULL DEFAULT '',
  `body` text,
  `enabled` tinyint(1) NOT NULL DEFAULT 1,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_code` (`project_id`, `code`),
  KEY `project_id` (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
'''

OPTION = dict(
  header='Текстовые блоки', name='text_block', sort=211,
  tool='admin-table', type='vue', config='ds_text_block',
)


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  # 1. Таблица
  await db.query(query=DDL, values=[], errors=[])

  # 2. Опция + раздача проектам
  opt = await db.query(
    query='SELECT id FROM ds_options WHERE config=%s',
    values=[OPTION['config']], onerow=1, errors=[],
  )
  if opt:
    option_id = int(opt['id'])
  else:
    await db.query(
      query='INSERT INTO ds_options(header,name,sort,tool,type,config,is_menu) '
            'VALUES(%s,%s,%s,%s,%s,%s,1)',
      values=[OPTION['header'], OPTION['name'], OPTION['sort'],
              OPTION['tool'], OPTION['type'], OPTION['config']],
      errors=[],
    )
    option_id = int(await db.query(
      query='SELECT id FROM ds_options WHERE config=%s',
      values=[OPTION['config']], onevalue=1, errors=[],
    ))

  projects = await db.query(
    query='SELECT DISTINCT project_id FROM ds_options_project',
    values=[], errors=[],
  ) or []
  for p in projects:
    pid = int(p['project_id'])
    on = await db.query(
      query='SELECT COUNT(*) FROM ds_options_project WHERE project_id=%s AND option_id=%s',
      values=[pid, option_id], onevalue=1, errors=[],
    )
    if not on:
      await db.query(
        query='INSERT INTO ds_options_project(project_id, option_id) VALUES(%s,%s)',
        values=[pid, option_id], errors=[],
      )

  # 3. Backfill из JSON страниц
  pages = await db.query(
    query='SELECT dp.blocks, d.project_id FROM domain_page dp '
          'JOIN domain d ON d.domain_id=dp.domain_id',
    values=[], errors=[],
  ) or []
  filled = 0
  for row in pages:
    try:
      doc = json.loads(row.get('blocks') or '')
    except (TypeError, ValueError):
      continue
    before = await db.query(
      query='SELECT COUNT(*) FROM ds_text_block WHERE project_id=%s',
      values=[int(row['project_id'])], onevalue=1, errors=[],
    )
    await upsert_from_doc(db, int(row['project_id']), doc)
    after = await db.query(
      query='SELECT COUNT(*) FROM ds_text_block WHERE project_id=%s',
      values=[int(row['project_id'])], onevalue=1, errors=[],
    )
    filled += max(0, int(after or 0) - int(before or 0))

  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_text_block: {db.error_str}')
  print(f'ds_text_block: ok (опция {OPTION["config"]}, коды: {", ".join(TEXT_BLOCK_MAP)}; '
        f'backfill +{filled} строк)')


if __name__ == '__main__':
  asyncio.run(main())
