# Миграция v2: сервис «Текстовые блоки» — точечная модель по галке блока.
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_text_block_v2
#
# Идемпотентна. Делает:
#   1. ds_text_block: + колонка tb_key (varchar(64)); unique key
#      (project_id, tb_key) вместо (project_id, code).
#   2. Старые строки (модель «одна запись на код типа», tb_key пуст):
#      находим первый блок этого типа в страницах проекта, проставляем ему
#      params.tb_admin=1 + params.tb_id в JSON (domain_page.blocks), tb_id
#      пишем в tb_key строки. Без пары в страницах строка удаляется.
#
# Дальше блоки помечаются галкой в конструкторе (params.tb_admin), tb_id
# проставляет page_save (lib/svcmsmanager/text_blocks.py::ensure_tb_ids).

import asyncio
import json
import secrets

from db import FreshDB
from config import config

from lib.svcmsmanager.text_blocks import TEXT_BLOCK_MAP, _parse_doc


async def _has_column(db, table, column):
  rows = await db.query(
    query='SELECT column_name AS col FROM information_schema.columns '
          'WHERE table_schema=DATABASE() AND table_name=%s',
    values=[table], errors=[],
  ) or []
  return column in {str(r['col']).lower() for r in rows}


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  # 1. tb_key + новый unique
  if not await _has_column(db, 'ds_text_block', 'tb_key'):
    await db.query(
      query="ALTER TABLE `ds_text_block` "
            "ADD COLUMN `tb_key` varchar(64) NOT NULL DEFAULT '' AFTER `project_id`",
      values=[], errors=[],
    )
  keys = await db.query(
    query="SHOW INDEX FROM `ds_text_block`",
    values=[], errors=[],
  ) or []
  key_names = {r['Key_name'] for r in keys}
  if 'project_code' in key_names:
    await db.query(
      query='ALTER TABLE `ds_text_block` DROP INDEX `project_code`',
      values=[], errors=[],
    )
  if 'project_tb' not in key_names:
    await db.query(
      query='ALTER TABLE `ds_text_block` '
            'ADD UNIQUE KEY `project_tb` (`project_id`, `tb_key`)',
      values=[], errors=[],
    )

  # 2. Старые строки -> tb_id в JSON
  legacy = await db.query(
    query="SELECT id, project_id, code FROM ds_text_block WHERE tb_key=''",
    values=[], errors=[],
  ) or []
  migrated, dropped = 0, 0
  for row in legacy:
    pid, code = int(row['project_id']), row['code']
    pages = await db.query(
      query='SELECT dp.id, dp.blocks FROM domain_page dp '
            'JOIN domain d ON d.domain_id=dp.domain_id WHERE d.project_id=%s',
      values=[pid], errors=[],
    ) or []
    tb_id = None
    for p in pages:
      doc = _parse_doc(p.get('blocks'))
      if not doc:
        continue
      changed = False
      for b in doc.get('blocks', []) or []:
        if b.get('type') == code and code in TEXT_BLOCK_MAP and tb_id is None:
          tb_id = secrets.token_hex(4)
          params = b.setdefault('params', {})
          params['tb_admin'] = 1
          params['tb_id'] = tb_id
          changed = True
          break
      if changed:
        await db.query(
          query='UPDATE domain_page SET blocks=%s WHERE id=%s',
          values=[json.dumps(doc, ensure_ascii=False), p['id']], errors=[],
        )
        break
    if tb_id:
      await db.query(
        query='UPDATE ds_text_block SET tb_key=%s WHERE id=%s',
        values=[tb_id, row['id']], errors=[],
      )
      migrated += 1
    else:
      await db.query(
        query='DELETE FROM ds_text_block WHERE id=%s',
        values=[row['id']], errors=[],
      )
      dropped += 1

  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_text_block_v2: {db.error_str}')
  print(f'ds_text_block_v2: ok (legacy -> tb_key: {migrated}, без пары удалено: {dropped})')


if __name__ == '__main__':
  asyncio.run(main())
