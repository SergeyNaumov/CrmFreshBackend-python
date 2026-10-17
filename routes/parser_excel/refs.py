"""Действия парсера xlsx для справочников (рубрики, бренды):
  check_refs  -- только чтение файла: какие значения ссылок не найдены в проекте
                 (до записи в БД), плюс id из другого проекта;
  create_refs -- создание отсутствующих значений по названию.

Набор ссылок и правило "id или название" задаются конфигом парсера ('refs',
см. lib/svcmsmanager/refs.py). Здесь только оркестрация: разбор файла и
форма ответа для фронта -- без привязки к конкретным таблицам.
"""

import re

from .go_parse import go_parse, build_hash_fields
from lib.svcmsmanager.refs import RefResolver

# защита от заливки огромного списка значений на создание
MAX_CREATE = 500


def _load_args(parser, R):
    fields = R.get('fields')
    loaded_filename = R.get('loaded_filename')
    data_line_number = R.get('data_line_number')
    errors = []
    if not (fields and isinstance(fields, list)):
        errors.append('fields не указано')
    if not (loaded_filename and re.match(r'^[a-zA-Z0-9_\-\.]+$', loaded_filename)):
        errors.append('loaded_filename не указан или указан не верно')
    return fields, loaded_filename, data_line_number, errors


def _make_resolvers(db, parser):
    resolvers = {}
    for ref in (parser.get('refs') or []):
        resolvers[ref['key']] = RefResolver(db, ref)
    return resolvers


async def check_refs(parser, R, db):
    refs = parser.get('refs') or []
    if not refs:
        return {'success': 1, 'refs': [], 'total_rows': 0}

    fields, loaded_filename, data_line_number, errors = _load_args(parser, R)
    if len(errors):
        return {'success': 0, 'errors': errors}

    hash_fields = build_hash_fields(fields)
    resolvers = _make_resolvers(db, parser)

    collected = {}
    for ref in refs:
        collected[ref['key']] = {'missing': set(), 'bad_ids': {}, 'no_ref': 0, 'unresolved': 0}
    total = [0]

    async def loopback(data):
        total[0] += 1
        for ref in refs:
            agg = collected[ref['key']]
            resolver = resolvers[ref['key']]
            id_field = ref['id_field']
            name_field = ref.get('name_field') or id_field
            id_v = data.get(id_field)
            name_v = data.get(name_field) if name_field != id_field else None
            res = await resolver.resolve(id_v, name_v)
            if res.get('bad_id'):
                agg['bad_ids'][res['bad_id']] = res.get('foreign_id', 0)
            if res.get('missing_name'):
                agg['missing'].add(res['missing_name'])
            if 'id' in res:
                continue
            if res.get('missing_name') or res.get('bad_id'):
                agg['unresolved'] += 1
            else:
                agg['no_ref'] += 1

    await go_parse(
        filename=loaded_filename,
        hash_fields=hash_fields,
        tmp_dir=parser['tmp_dir'],
        data_line_number=data_line_number,
        loopback=loopback)

    out_refs = []
    for ref in refs:
        agg = collected[ref['key']]
        out_refs.append({
            'key': ref['key'],
            'label': ref.get('label') or ref['key'],
            'missing': sorted(agg['missing']),
            'bad_ids': [
                {'id': rid, 'foreign': foreign}
                for rid, foreign in sorted(agg['bad_ids'].items())
            ],
            'unresolved': agg['unresolved'],
            'no_ref': agg['no_ref'],
        })

    return {'success': 1, 'refs': out_refs, 'total_rows': total[0]}


async def create_refs(parser, R, db):
    refs = {ref['key']: ref for ref in (parser.get('refs') or [])}
    key = R.get('ref')
    ref = refs.get(key)
    if not ref:
        return {'success': 0, 'errors': [f'неизвестная ссылка: {key}']}

    names = R.get('names') or []
    if not isinstance(names, list):
        return {'success': 0, 'errors': ['names должен быть списком']}
    if len(names) > MAX_CREATE:
        return {'success': 0, 'errors': [f'слишком много значений (>{MAX_CREATE})']}

    resolver = RefResolver(db, ref)
    created = 0
    skipped = 0
    errors = []
    ids = {}
    seen = set()
    for raw in names:
        name = str(raw or '').replace('\xa0', ' ').strip()
        if not name or name in seen or len(name) > 200:
            continue
        seen.add(name)
        try:
            rid = await resolver.create(name)
        except Exception as e:  # noqa: BLE001 -- показываем причину пользователю
            errors.append(f'{name}: {e}')
            continue
        if rid:
            ids[name] = rid
            created += 1
        else:
            skipped += 1

    result = {
        'success': (1, 0)[len(errors) > 0],
        'created': created,
        'skipped': skipped,
        'ids': ids,
    }
    if errors:
        result['errors'] = errors
    return result
