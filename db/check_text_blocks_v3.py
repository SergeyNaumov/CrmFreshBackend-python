# Проверка v3-синхронизации «Текстовые блоки» <-> domain_page.blocks.
# Прогон на локальной БД с откатом в конце (снимок строк/страниц до теста).

import asyncio
import json

from db import FreshDB
from config import config
from lib.svcmsmanager import text_blocks as tb

PROJECT = 5837
TB_KEY = '0993340b'


async def _pages(db, project_id):
  return await db.query(
    query='SELECT dp.id, dp.blocks FROM domain_page dp '
          'JOIN domain d ON d.domain_id=dp.domain_id WHERE d.project_id=%s',
    values=[project_id], errors=[],
  ) or []


def _find(doc, tb_id):
  for b in doc.get('blocks') or []:
    if (b.get('params') or {}).get('tb_id') == tb_id:
      return b
  return None


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  pages = await _pages(db, PROJECT)
  page = next(p for p in pages if _find(json.loads(p['blocks']), TB_KEY))
  snap_page = page['blocks']

  row = await tb.get_row(db, PROJECT, TB_KEY)
  snap_row = dict(row)
  assert row and row['mode'] == 'blocks', row

  block = tb.block_from_row(row)
  locked = {k: (block['params'].get(k)) for k in ('page_head', 'show_title', 'tb_admin', 'tb_id')}
  variant = block.get('variant')

  # --- 1. менеджер -> страница (режим блоков) ---
  block['params']['title'] = 'ТЕСТ: заголовок из менеджера'
  block['params']['text'] = 'ТЕСТ: текст из менеджера'
  block['params']['image'] = 'block-images/test-about.webp'
  block['params']['btn1Text'] = 'Кнопка 1'
  block['params']['btn1Url'] = '/test1'
  block['params'].pop('btn2Text', None)
  block['items'] = [{'text': 'Тест-преимущество'}]
  await db.query(
    query='UPDATE ds_text_block SET blocks=%s WHERE id=%s',
    values=[json.dumps(tb.doc_of_block(block), ensure_ascii=False), row['id']],
    errors=[],
  )
  await tb.refresh_mirrors(db, PROJECT, row['id'])
  await tb.sync_row_to_pages(db, PROJECT, TB_KEY)

  page2 = next(p for p in await _pages(db, PROJECT) if p['id'] == page['id'])
  b2 = _find(json.loads(page2['blocks']), TB_KEY)
  assert b2['params']['title'] == 'ТЕСТ: заголовок из менеджера', b2['params']
  assert b2['params']['image'] == 'block-images/test-about.webp'
  assert b2['params']['btn1Url'] == '/test1'
  assert 'btn2Text' not in b2['params'], b2['params']
  assert b2['items'] == [{'text': 'Тест-преимущество'}], b2.get('items')
  assert {k: b2['params'].get(k) for k in locked} == locked, 'технические params изменены!'
  assert b2.get('variant') == variant
  row2 = await tb.get_row(db, PROJECT, TB_KEY)
  assert row2['header'] == 'ТЕСТ: заголовок из менеджера', row2['header']
  assert row2['body'] == 'ТЕСТ: текст из менеджера'
  print('1. менеджер -> страница: OK')

  # --- 2. страница -> менеджер (конструктор) ---
  doc = json.loads(page2['blocks'])
  b3 = _find(doc, TB_KEY)
  b3['params']['btn2Text'] = 'Из конструктора'
  b3['params']['btn2Url'] = '/from-constructor'
  b3['params']['title'] = 'ТЕСТ: заголовок из конструктора'
  await db.query(
    query='UPDATE domain_page SET blocks=%s WHERE id=%s',
    values=[json.dumps(doc, ensure_ascii=False), page['id']], errors=[],
  )
  await tb.upsert_from_doc(db, PROJECT, doc)
  row3 = await tb.get_row(db, PROJECT, TB_KEY)
  blk3 = tb.block_from_row(row3)
  assert row3['header'] == 'ТЕСТ: заголовок из конструктора', row3['header']
  assert blk3['params']['btn2Text'] == 'Из конструктора'
  assert row3['mode'] == 'blocks', 'режим не должен сбрасываться'
  print('2. страница -> менеджер: OK')

  # --- 3. text-режим (contact_form) ---
  cf = await db.query(
    query="SELECT * FROM ds_text_block WHERE project_id=%s AND code='contact_form'",
    values=[PROJECT], onerow=1, errors=[],
  )
  cf_page = next(p for p in await _pages(db, PROJECT)
                 if _find(json.loads(p['blocks']), cf['tb_key']))
  snap_cf_page = cf_page['blocks']
  await db.query(
    query='UPDATE ds_text_block SET header=%s, body=%s WHERE id=%s',
    values=['ТЕСТ: контакты', 'ТЕСТ: подзаголовок', cf['id']], errors=[],
  )
  await tb.sync_row_to_pages(db, PROJECT, cf['tb_key'])
  cfp2 = next(p for p in await _pages(db, PROJECT) if p['id'] == cf_page['id'])
  cb = _find(json.loads(cfp2['blocks']), cf['tb_key'])
  assert cb['params']['header'] == 'ТЕСТ: контакты', cb['params']
  assert cb['params']['sub'] == 'ТЕСТ: подзаголовок'
  print('3. text-режим: OK')

  # --- 4. выключенный блок не синхронизируется ---
  await db.query(query='UPDATE ds_text_block SET enabled=0 WHERE id=%s',
                 values=[cf['id']], errors=[])
  await db.query(query='UPDATE ds_text_block SET header=%s WHERE id=%s',
                 values=['ТЕСТ: выключено', cf['id']], errors=[])
  await tb.sync_row_to_pages(db, PROJECT, cf['tb_key'])
  cfp3 = next(p for p in await _pages(db, PROJECT) if p['id'] == cf_page['id'])
  assert _find(json.loads(cfp3['blocks']), cf['tb_key'])['params']['header'] == 'ТЕСТ: контакты'
  print('4. enabled=0: OK')

  # --- откат ---
  await db.query(query='UPDATE domain_page SET blocks=%s WHERE id=%s',
                 values=[snap_page, page['id']], errors=[])
  await db.query(query='UPDATE domain_page SET blocks=%s WHERE id=%s',
                 values=[snap_cf_page, cf_page['id']], errors=[])
  await db.query(
    query='UPDATE ds_text_block SET header=%s, body=%s, blocks=%s, enabled=%s '
          'WHERE id=%s',
    values=[snap_row['header'], snap_row['body'], snap_row.get('blocks'),
            snap_row['enabled'], snap_row['id']], errors=[])
  await db.query(
    query='UPDATE ds_text_block SET header=%s, body=%s, enabled=%s WHERE id=%s',
    values=[cf['header'], cf['body'], cf['enabled'], cf['id']], errors=[])

  await db.close_pool()
  if db.error_str:
    raise SystemExit('db errors: %s' % db.error_str)
  print('откат выполнен')


if __name__ == '__main__':
  asyncio.run(main())
