# -*- coding: utf-8 -*-
"""Сервис «Текстовые блоки» (ds_text_block): двусторонняя синхронизация
текстовых params блоков конструктора (domain_page.blocks) с таблицей
ds_text_block.

Модель v2 — точечная, по галке блока:
  - у блока в конструкторе есть галка params.tb_admin («Администрировать
    текстовый блок в /manager») и техпараметр params.tb_id (стабильный id
    экземпляра, проставляет бэкенд при сохранении страницы — ensure_tb_ids);
  - запись ds_text_block ключуется по (project_id, tb_key=tb_id) — каждый
    помеченный экземпляр блока редактируется отдельно;
  - конструктор -> таблица: page_save -> ensure_tb_ids + upsert_from_doc
    (заодно GC: строки со снятой галкой/удалённым блоком удаляются);
  - таблица -> конструктор: after_save в conf/ds_text_block ->
    sync_row_to_pages (обновляется конкретный блок по tb_id).

Источник рендера сайта — JSON блоков (domain_page.blocks): движок сайта
не меняется. Реестр TEXT_BLOCK_MAP: какие типы блоков администрируются
и какие params кладём в header/body записи. При добавлении типа не забыть:
schema.json (параметр tb_admin), конфиг ds_text_block (select code),
контракт _shared/contract/blocks.json (params tb_admin/tb_id).
"""

import json
import secrets

TEXT_BLOCK_MAP = {
    'about': {
        'title': 'Блок «О компании»',
        'fields': {'header': 'title', 'body': 'text'},
    },
    'contact_form': {
        'title': 'Блок «Контакты + форма»',
        'fields': {'header': 'header', 'body': 'sub'},
    },
    'text': {
        'title': 'Текстовый блок',
        'fields': {'header': 'title', 'body': 'p1'},
    },
}


def _truthy(v):
    """tb_admin из JSON может быть bool/0/1/'1'/'true'."""
    return v is True or v in (1, '1', 'true', 'True')


def _flagged(block):
    """Блок помечен галкой и его тип администрируется?"""
    return (block.get('type') in TEXT_BLOCK_MAP
            and _truthy((block.get('params') or {}).get('tb_admin')))


def ensure_tb_ids(doc):
    """Проставить params.tb_id помеченным блокам без него. (doc, changed)."""
    changed = False
    for b in (doc or {}).get('blocks', []) or []:
        if _flagged(b) and not (b.get('params') or {}).get('tb_id'):
            b.setdefault('params', {})['tb_id'] = secrets.token_hex(4)
            changed = True
    return doc, changed


def extract_from_doc(doc):
    """{tb_id: {'code', 'header', 'body'}} — помеченные блоки страницы."""
    out = {}
    for b in (doc or {}).get('blocks', []) or []:
        if not _flagged(b):
            continue
        params = b.get('params') or {}
        tb_id = params.get('tb_id')
        if not tb_id:
            continue
        t = b['type']
        row = {'code': t}
        for col, pname in TEXT_BLOCK_MAP[t]['fields'].items():
            v = params.get(pname)
            if v is not None:
                row[col] = str(v)
        out[tb_id] = row
    return out


def apply_to_doc(doc, tb_id, values):
    """Проставить params из values в блок с этим tb_id. (doc, changed)."""
    changed = False
    for b in (doc or {}).get('blocks', []) or []:
        t = b.get('type')
        params = b.get('params') or {}
        if t not in TEXT_BLOCK_MAP or params.get('tb_id') != tb_id:
            continue
        for col, pname in TEXT_BLOCK_MAP[t]['fields'].items():
            v = values.get(col)
            if v is not None and params.get(pname) != v:
                params[pname] = v
                changed = True
    return doc, changed


def _parse_doc(raw):
    try:
        return json.loads(raw or '')
    except (TypeError, ValueError):
        return None


async def _project_pages(db, project_id):
    return await db.query(
        query='SELECT dp.id, dp.blocks FROM domain_page dp '
              'JOIN domain d ON d.domain_id=dp.domain_id WHERE d.project_id=%s',
        values=[project_id], errors=[],
    ) or []


async def upsert_from_doc(db, project_id, doc):
    """Конструктор -> таблица: upsert помеченных блоков страницы + GC.

    GC: строки проекта, чей tb_key больше не встречается ни на одной
    странице (галка снята или блок удалён), удаляются."""
    if not project_id:
        return
    for tb_id, vals in extract_from_doc(doc).items():
        header = vals.get('header', '')
        body = vals.get('body', '')
        code = vals.get('code', '')
        existing = await db.query(
            query='SELECT id, header, body FROM ds_text_block '
                  'WHERE project_id=%s AND tb_key=%s',
            values=[project_id, tb_id], onerow=1, errors=[],
        )
        if existing:
            if existing.get('header') != header or existing.get('body') != body:
                await db.query(
                    query='UPDATE ds_text_block SET header=%s, body=%s, code=%s '
                          'WHERE id=%s',
                    values=[header, body, code, existing['id']], errors=[],
                )
        else:
            await db.query(
                query='INSERT INTO ds_text_block(project_id, tb_key, code, header, body, enabled) '
                      'VALUES(%s,%s,%s,%s,%s,1)',
                values=[project_id, tb_id, code, header, body], errors=[],
            )

    # GC: живые tb_id по всем страницам проекта
    alive = set()
    for p in await _project_pages(db, project_id):
        d2 = _parse_doc(p.get('blocks'))
        if d2:
            alive |= set(extract_from_doc(d2).keys())
    rows = await db.query(
        query='SELECT id, tb_key FROM ds_text_block WHERE project_id=%s',
        values=[project_id], errors=[],
    ) or []
    for r in rows:
        if (r.get('tb_key') or '') not in alive:
            await db.query(
                query='DELETE FROM ds_text_block WHERE id=%s',
                values=[r['id']], errors=[],
            )


async def sync_row_to_pages(db, project_id, tb_key):
    """Таблица -> JSON страниц: значения строки tb_key — в её блок."""
    if not (project_id and tb_key):
        return
    row = await db.query(
        query='SELECT header, body, enabled FROM ds_text_block '
              'WHERE project_id=%s AND tb_key=%s',
        values=[project_id, tb_key], onerow=1, errors=[],
    )
    if not row or not row.get('enabled'):
        return
    values = {'header': row.get('header') or '', 'body': row.get('body') or ''}
    for p in await _project_pages(db, project_id):
        doc = _parse_doc(p.get('blocks'))
        if not doc:
            continue
        doc, changed = apply_to_doc(doc, tb_key, values)
        if changed:
            await db.query(
                query='UPDATE domain_page SET blocks=%s WHERE id=%s',
                values=[json.dumps(doc, ensure_ascii=False), p['id']], errors=[],
            )
