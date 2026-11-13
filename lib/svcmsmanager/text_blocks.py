# -*- coding: utf-8 -*-
"""Сервис «Текстовые блоки» (ds_text_block): двусторонняя синхронизация
текстовых params блоков конструктора (domain_page.blocks) с таблицей
ds_text_block.

Источник рендера сайта — JSON блоков (domain_page.blocks): движок сайта
не меняется. Таблица — редакторский агрегат:
  - конструктор страниц при сохранении страницы upsert'ит тексты блоков
    в таблицу (routes/svcmsadmin/page_constructor -> upsert_from_doc);
  - сервис в /manager (конфиг ds_text_block) при сохранении записи пишет
    значения обратно в JSON страниц проекта (conf/ds_text_block/events.py
    -> sync_row_to_pages).

Реестр TEXT_BLOCK_MAP: code блока -> какие params кладём в header/body
записи. При добавлении блока не забыть конфиг ds_text_block (select code)
и миграцию db/migrate_ds_text_block.py (backfill).
"""

import json

TEXT_BLOCK_MAP = {
    'about': {
        'title': 'Блок «О компании»',
        'fields': {'header': 'title', 'body': 'text'},
    },
    'contact_form': {
        'title': 'Блок «Контакты + форма»',
        'fields': {'header': 'header', 'body': 'sub'},
    },
}


def extract_from_doc(doc):
    """{code: {'header':…,'body':…}} из документа страницы (первая встреча блока)."""
    out = {}
    for b in (doc or {}).get('blocks', []) or []:
        t = b.get('type')
        if t in TEXT_BLOCK_MAP and t not in out:
            params = b.get('params') or {}
            row = {}
            for col, pname in TEXT_BLOCK_MAP[t]['fields'].items():
                v = params.get(pname)
                if v is not None:
                    row[col] = str(v)
            if row:
                out[t] = row
    return out


def apply_to_doc(doc, code, values):
    """Проставить params из values во ВСЕ блоки типа code документа.

    Возвращает (doc, changed)."""
    spec = TEXT_BLOCK_MAP.get(code)
    if not spec:
        return doc, False
    changed = False
    for b in (doc or {}).get('blocks', []) or []:
        if b.get('type') != code:
            continue
        params = b.setdefault('params', {})
        for col, pname in spec['fields'].items():
            v = values.get(col)
            if v is not None and params.get(pname) != v:
                params[pname] = v
                changed = True
    return doc, changed


async def upsert_from_doc(db, project_id, doc):
    """Конструктор -> таблица: upsert извлечённых текстовых блоков проекта."""
    if not project_id:
        return
    for code, vals in extract_from_doc(doc).items():
        header = vals.get('header', '')
        body = vals.get('body', '')
        existing = await db.query(
            query='SELECT id, header, body FROM ds_text_block '
                  'WHERE project_id=%s AND code=%s',
            values=[project_id, code], onerow=1, errors=[],
        )
        if existing:
            if existing.get('header') != header or existing.get('body') != body:
                await db.query(
                    query='UPDATE ds_text_block SET header=%s, body=%s WHERE id=%s',
                    values=[header, body, existing['id']], errors=[],
                )
        else:
            await db.query(
                query='INSERT INTO ds_text_block(project_id, code, header, body, enabled) '
                      'VALUES(%s,%s,%s,%s,1)',
                values=[project_id, code, header, body], errors=[],
            )


async def sync_row_to_pages(db, project_id, code):
    """Таблица -> JSON страниц: значения строки code — во все страницы проекта."""
    if not (project_id and code in TEXT_BLOCK_MAP):
        return
    row = await db.query(
        query='SELECT header, body, enabled FROM ds_text_block '
              'WHERE project_id=%s AND code=%s',
        values=[project_id, code], onerow=1, errors=[],
    )
    if not row or not row.get('enabled'):
        return
    values = {'header': row.get('header') or '', 'body': row.get('body') or ''}
    pages = await db.query(
        query='SELECT dp.id, dp.blocks FROM domain_page dp '
              'JOIN domain d ON d.domain_id=dp.domain_id WHERE d.project_id=%s',
        values=[project_id], errors=[],
    ) or []
    for p in pages:
        try:
            doc = json.loads(p.get('blocks') or '')
        except (TypeError, ValueError):
            continue
        doc, changed = apply_to_doc(doc, code, values)
        if changed:
            await db.query(
                query='UPDATE domain_page SET blocks=%s WHERE id=%s',
                values=[json.dumps(doc, ensure_ascii=False), p['id']], errors=[],
            )
