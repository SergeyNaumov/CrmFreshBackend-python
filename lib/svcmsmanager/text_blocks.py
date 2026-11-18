# -*- coding: utf-8 -*-
"""Сервис «Текстовые блоки» (ds_text_block): двусторонняя синхронизация
блоков конструктора (domain_page.blocks) с таблицей ds_text_block.

Модель v3 — точечная, по галке блока, с двумя режимами записи:
  - у блока в конструкторе есть галка params.tb_admin («Администрировать
    текстовый блок в /manager») и техпараметр params.tb_id (стабильный id
    экземпляра, проставляет бэкенд при сохранении страницы — ensure_tb_ids);
  - запись ds_text_block ключуется по (project_id, tb_key=tb_id);
  - mode='text'   — в форме только заголовок и текст (колонки header/body);
  - mode='blocks' — в форме редактор блока (колонка blocks: JSON одного
    блока в конверте svcms.page_blocks v2), т.е. отдельно заголовок, фото,
    текст, кнопки, бейдж и преимущества; header/body при этом остаются
    зеркалами для списка и пересчитываются из blocks (after_save);
  - конструктор -> таблица: page_save -> ensure_tb_ids + upsert_from_doc
    (обновляет и зеркала, и blocks, заодно GC: строки со снятой галкой/
    удалённым блоком удаляются);
  - таблица -> конструктор: after_save в conf/ds_text_block ->
    sync_row_to_pages (обновляется конкретный блок по tb_id).

Источник рендера сайта — JSON блоков (domain_page.blocks): движок сайта
не меняется. Реестр TEXT_BLOCK_MAP: какие типы блоков администрируются,
какие params/items принадлежат сервису и что переносится в зеркала.
При добавлении типа не забыть: schema.json (параметр tb_admin), конфиг
ds_text_block (select code + allowed_types у поля blocks), контракт
_shared/contract/blocks.json (params tb_admin/tb_id).
"""

import json
import secrets

# Технические params, которые сервис никогда не перезаписывает: они
# принадлежат конструктору (раскладка/структура блока).
DEFAULT_LOCKED = ('tb_admin', 'tb_id')

TEXT_BLOCK_MAP = {
    'about': {
        'title': 'Блок «О компании»',
        # Зеркала (список, поиск, режим text): колонка -> param блока.
        'fields': {'header': 'title', 'body': 'text'},
        # Есть полноценный режим блоков (заголовок/фото/текст/кнопки/badge).
        'blocks_mode': True,
        # params блока, которыми владеет сервис в режиме блоков.
        'params': [
            'title', 'text', 'image',
            'badgeNum', 'badgeText',
            'btn1Text', 'btn1Url', 'btn2Text', 'btn2Url',
        ],
        # элементы блока: { text } — преимущества с галочкой.
        'items': ['text'],
        # Раскладка блока — только из конструктора.
        'locked': ['page_head', 'show_title'],
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

DOC_EMPTY = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': []}


def _truthy(v):
    """tb_admin из JSON может быть bool/0/1/'1'/'true'."""
    return v is True or v in (1, '1', 'true', 'True')


def _flagged(block):
    """Блок помечен галкой и его тип администрируется?"""
    return (block.get('type') in TEXT_BLOCK_MAP
            and _truthy((block.get('params') or {}).get('tb_admin')))


def default_mode(code):
    """Режим новой записи: blocks — если у типа есть полноценный редактор."""
    spec = TEXT_BLOCK_MAP.get(code) or {}
    return 'blocks' if spec.get('blocks_mode') else 'text'


def is_blocks_type(code):
    """У типа блока есть режим блоков (полный редактор)? """
    return bool((TEXT_BLOCK_MAP.get(code) or {}).get('blocks_mode'))


def doc_of_block(block):
    """Конверт svcms.page_blocks v2 с одним блоком (для колонки blocks)."""
    return {'schema': 'svcms.page_blocks', 'version': 2,
            'blocks': [json.loads(json.dumps(block, ensure_ascii=False))]}


def block_of(doc, tb_id):
    """Блок конверта с этим tb_id (копия) или None."""
    for b in (doc or {}).get('blocks', []) or []:
        if (b.get('params') or {}).get('tb_id') == tb_id:
            return json.loads(json.dumps(b, ensure_ascii=False))
    return None


def ensure_tb_ids(doc):
    """Проставить params.tb_id помеченным блокам без него. (doc, changed)."""
    changed = False
    for b in (doc or {}).get('blocks', []) or []:
        if _flagged(b) and not (b.get('params') or {}).get('tb_id'):
            b.setdefault('params', {})['tb_id'] = secrets.token_hex(4)
            changed = True
    return doc, changed


def mirrors_of(block):
    """header/body записи из блока (по реестру fields)."""
    out = {}
    for col, pname in (TEXT_BLOCK_MAP.get(block.get('type')) or {}).get('fields', {}).items():
        v = (block.get('params') or {}).get(pname)
        out[col] = '' if v is None else str(v)
    return out


def merge_mirrors_into_block(block, header, body):
    """Перенести header/body (режим «только текст») в params блока."""
    spec = (TEXT_BLOCK_MAP.get(block.get('type')) or {}).get('fields', {})
    params = block.setdefault('params', {})
    for col, val in (('header', header), ('body', body)):
        pname = spec.get(col)
        if pname and val is not None:
            params[pname] = val
    return block


def json_of_block(block):
    """JSON-строка колонки blocks для одного блока."""
    return json.dumps(doc_of_block(block), ensure_ascii=False)


def extract_from_doc(doc):
    """{tb_id: {code, mode, header, body, blocks}} — помеченные блоки страницы.

    blocks — JSON-строка конверта svcms.page_blocks с одним блоком (v3);
    для типов без режима блоков не заполняется (режим text).
    """
    out = {}
    for b in (doc or {}).get('blocks', []) or []:
        if not _flagged(b):
            continue
        params = b.get('params') or {}
        tb_id = params.get('tb_id')
        if not tb_id:
            continue
        t = b['type']
        row = {'code': t, 'mode': default_mode(t)}
        row.update(mirrors_of(b))
        if is_blocks_type(t):
            row['blocks'] = json.dumps(doc_of_block(b), ensure_ascii=False)
        out[tb_id] = row
    return out


def apply_to_doc(doc, tb_id, values):
    """Проставить значения записи в блок с этим tb_id. (doc, changed).

    values: {mode, header, body, block} — block приходит из колонки blocks
    (dict-конверт или один блок). В режиме blocks пишутся только params/items,
    принадлежащие сервису (реестр), технические params не трогаются.
    """
    changed = False
    for b in (doc or {}).get('blocks', []) or []:
        t = b.get('type')
        spec = TEXT_BLOCK_MAP.get(t)
        if not spec or (b.get('params') or {}).get('tb_id') != tb_id:
            continue

        if values.get('mode') == 'blocks' and spec.get('blocks_mode'):
            nb = values.get('block') or {}
            owned = spec.get('params') or []
            locked = set(spec.get('locked') or ()) | set(DEFAULT_LOCKED)
            cur = b.setdefault('params', {})
            newp = nb.get('params') or {}
            for k in owned:
                if k in locked:
                    continue
                if k in newp:
                    if cur.get(k) != newp[k]:
                        cur[k] = newp[k]
                        changed = True
                elif k in cur:
                    # параметр снят в редакторе — убираем и в блоке
                    cur.pop(k)
                    changed = True
            if spec.get('items') and 'items' in nb:
                items = nb.get('items') or []
                if b.get('items') != items:
                    b['items'] = items
                    changed = True
        else:
            for col, pname in spec.get('fields', {}).items():
                v = values.get(col)
                if v is not None and (b.get('params') or {}).get(pname) != v:
                    b.setdefault('params', {})[pname] = v
                    changed = True
    return doc, changed


def _parse_doc(raw):
    try:
        return json.loads(raw or '')
    except (TypeError, ValueError):
        return None


def parse_block(raw):
    """Колонка blocks -> один блок (dict) или None."""
    d = _parse_doc(raw) if isinstance(raw, str) else raw
    if isinstance(d, dict) and isinstance(d.get('blocks'), list) and d['blocks']:
        return d['blocks'][0]
    return None


def block_from_row(row):
    """Один блок из строки ds_text_block (колонка blocks) или None."""
    if not row:
        return None
    return parse_block(row.get('blocks'))


async def _project_pages(db, project_id):
    return await db.query(
        query='SELECT dp.id, dp.blocks FROM domain_page dp '
              'JOIN domain d ON d.domain_id=dp.domain_id WHERE d.project_id=%s',
        values=[project_id], errors=[],
    ) or []


async def doc_from_pages(db, project_id, tb_key):
    """Конверт с блоком tb_key из страниц проекта (для сидинга/бэкфилла)."""
    for p in await _project_pages(db, project_id):
        d2 = _parse_doc(p.get('blocks'))
        if not d2:
            continue
        b = block_of(d2, tb_key)
        if b:
            return doc_of_block(b)
    return None


async def upsert_from_doc(db, project_id, doc):
    """Конструктор -> таблица: upsert помеченных блоков страницы + GC.

    Обновляет и зеркала (header/body), и blocks (v3) — поэтому в таблице
    всегда актуальный блок: сохранение из менеджера не откатит правки
    конструктора. mode/enabled существующей строки не трогаем (это выбор
    администратора), у новой строки mode — по реестру типа.

    GC: строки проекта, чей tb_key больше не встречается ни на одной
    странице (галка снята или блок удалён), удаляются."""
    if not project_id:
        return
    for tb_id, vals in extract_from_doc(doc).items():
        header = vals.get('header', '')
        body = vals.get('body', '')
        code = vals.get('code', '')
        blocks = vals.get('blocks')
        existing = await db.query(
            query='SELECT id, header, body, blocks FROM ds_text_block '
                  'WHERE project_id=%s AND tb_key=%s',
            values=[project_id, tb_id], onerow=1, errors=[],
        )
        if existing:
            if (existing.get('header') != header
                    or existing.get('body') != body
                    or (existing.get('blocks') or '') != (blocks or '')):
                await db.query(
                    query='UPDATE ds_text_block SET header=%s, body=%s, code=%s, '
                          'blocks=%s WHERE id=%s',
                    values=[header, body, code, blocks, existing['id']], errors=[],
                )
        else:
            await db.query(
                query='INSERT INTO ds_text_block(project_id, tb_key, code, header, '
                      'body, blocks, mode, enabled) VALUES(%s,%s,%s,%s,%s,%s,%s,1)',
                values=[project_id, tb_id, code, header, body, blocks,
                        vals.get('mode') or default_mode(code)], errors=[],
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


async def get_row(db, project_id, tb_key):
    """Строка сервиса по ключу блока (или None)."""
    return await db.query(
        query='SELECT id, project_id, tb_key, code, header, body, blocks, '
              'mode, enabled FROM ds_text_block '
              'WHERE project_id=%s AND tb_key=%s',
        values=[project_id, tb_key], onerow=1, errors=[],
    )


def values_of_row(row):
    """Значения записи для apply_to_doc."""
    mode = (row.get('mode') or 'text')
    code = row.get('code') or ''
    values = {
        'mode': mode,
        'header': row.get('header') or '',
        'body': row.get('body') or '',
    }
    if mode == 'blocks' and is_blocks_type(code):
        values['block'] = block_from_row(row) or {
            'type': code, 'params': {}, 'items': [],
        }
    return values


async def sync_row_to_pages(db, project_id, tb_key):
    """Таблица -> JSON страниц: значения строки tb_key — в её блок."""
    if not (project_id and tb_key):
        return
    row = await get_row(db, project_id, tb_key)
    if not row or not row.get('enabled'):
        return
    values = values_of_row(row)
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


async def refresh_mirrors(db, project_id, row_id):
    """Пересчитать header/body строки из её blocks (режим блоков).

    Вызывается из after_save: список/поиск всегда показывают актуальные
    заголовок и текст. Пустой/битый blocks не трогаем (не затираем зеркала).
    """
    row = await db.query(
        query='SELECT id, code, mode, blocks FROM ds_text_block '
              'WHERE id=%s AND project_id=%s',
        values=[row_id, project_id], onerow=1, errors=[],
    )
    if not row or row.get('mode') != 'blocks':
        return False
    block = block_from_row(row)
    if not block or not block.get('params'):
        return False
    m = mirrors_of(block)
    if not m:
        return False
    await db.query(
        query='UPDATE ds_text_block SET header=%s, body=%s WHERE id=%s',
        values=[m.get('header', ''), m.get('body', ''), row['id']], errors=[],
    )
    return True
