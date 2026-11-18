# Миграция v3: сервис «Текстовые блоки» — режим блоков (заголовок/фото/
# текст/кнопки/бейдж/преимущества) поверх точечной модели v2.
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_text_block_v3
#
# Идемпотентна. Делает:
#   1. ds_text_block: + колонка mode enum('text','blocks') DEFAULT 'text',
#      + колонка blocks mediumtext NULL (JSON одного блока svcms.page_blocks v2).
#   2. По всем проектам, у которых есть администрируемые блоки: проставляет
#      params.tb_id (ensure_tb_ids) помеченным блокам без него и обновляет
#      строки сервиса (upsert_from_doc: зеркала header/body + blocks).
#   3. Блокам about ставит mode='blocks' (полный редактор) и заполняет
#      blocks, если колонка пустая.
#
# Дальше: правки страницы в конструкторе обновляют таблицу (upsert_from_doc),
# правки в сервисе пишутся в domain_page.blocks (after_save -> sync_row_to_pages).

import asyncio
import json

from db import FreshDB
from config import config

from lib.svcmsmanager.text_blocks import (
  doc_of_block, ensure_tb_ids, is_blocks_type,
  _parse_doc, _flagged, upsert_from_doc,
)


async def _has_column(db, table, column):
  rows = await db.query(
    query='SELECT column_name AS col FROM information_schema.columns '
          'WHERE table_schema=DATABASE() AND table_name=%s',
    values=[table], errors=[],
  ) or []
  return column in {str(r['col']).lower() for r in rows}


async def _project_ids(db):
  """Проекты: со строками сервиса + со страницами, где есть помеченные блоки."""
  ids = set()
  rows = await db.query(
    query='SELECT DISTINCT project_id FROM ds_text_block',
    values=[], errors=[],
  ) or []
  for r in rows:
    if r.get('project_id'):
      ids.add(int(r['project_id']))

  pages = await db.query(
    query='SELECT dp.id, dp.blocks, d.project_id '
          'FROM domain_page dp JOIN domain d ON d.domain_id=dp.domain_id',
    values=[], errors=[],
  ) or []
  by_project = {}
  for p in pages:
    doc = _parse_doc(p.get('blocks'))
    if not doc:
      continue
    if any(_flagged(b) for b in doc.get('blocks', []) or []):
      by_project.setdefault(int(p['project_id']), []).append(p)
  return ids, by_project


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  # 1. Колонки
  if not await _has_column(db, 'ds_text_block', 'mode'):
    await db.query(
      query="ALTER TABLE `ds_text_block` ADD COLUMN `mode` "
            "enum('text','blocks') NOT NULL DEFAULT 'text' AFTER `body`",
      values=[], errors=[],
    )
  if not await _has_column(db, 'ds_text_block', 'blocks'):
    await db.query(
      query="ALTER TABLE `ds_text_block` ADD COLUMN `blocks` mediumtext NULL "
            "AFTER `mode`",
      values=[], errors=[],
    )

  # 2. tb_id помеченным блокам + upsert строк (зеркала + blocks)
  ids, by_project = await _project_ids(db)
  assigned = 0
  for pid, pages in sorted(by_project.items()):
    for p in pages:
      doc = _parse_doc(p.get('blocks'))
      if not doc:
        continue
      doc, changed = ensure_tb_ids(doc)
      if changed:
        await db.query(
          query='UPDATE domain_page SET blocks=%s WHERE id=%s',
          values=[json.dumps(doc, ensure_ascii=False), p['id']], errors=[],
        )
        assigned += 1
      await upsert_from_doc(db, pid, doc)

  # 3. about -> режим блоков + заполнение blocks
  rows = await db.query(
    query='SELECT id, project_id, tb_key, code, mode, blocks '
          'FROM ds_text_block',
    values=[], errors=[],
  ) or []
  blocks_mode, filled = 0, 0
  for row in rows:
    code = row.get('code') or ''
    if not is_blocks_type(code):
      continue
    pid, tb_key = int(row['project_id']), row.get('tb_key') or ''
    if not tb_key:
      continue
    if row.get('mode') != 'blocks':
      await db.query(
        query="UPDATE ds_text_block SET mode='blocks' WHERE id=%s",
        values=[row['id']], errors=[],
      )
      blocks_mode += 1
    if not (row.get('blocks') or '').strip():
      # blocks пуст — берём блок из страниц проекта
      doc = None
      for p in by_project.get(pid, []):
        d2 = _parse_doc(p.get('blocks'))
        for b in (d2 or {}).get('blocks', []) or []:
          if _flagged(b) and (b.get('params') or {}).get('tb_id') == tb_key:
            doc = doc_of_block(b)
            break
        if doc:
          break
      if doc:
        await db.query(
          query='UPDATE ds_text_block SET blocks=%s WHERE id=%s',
          values=[json.dumps(doc, ensure_ascii=False), row['id']], errors=[],
        )
        filled += 1

  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_text_block_v3: {db.error_str}')
  print(f'ds_text_block_v3: ok (tb_id проставлен на страницах: {assigned}, '
        f'mode=blocks: {blocks_mode}, blocks заполнено: {filled})')


if __name__ == '__main__':
  asyncio.run(main())
