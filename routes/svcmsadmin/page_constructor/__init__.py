import json
import os
from typing import Any

from fastapi import APIRouter, Request, Response
from pydantic import BaseModel

from config import config as sysconfig


router = APIRouter()

BLOCKS_EMPTY = '{"schema": "svcms.page_blocks", "version": 2, "blocks": []}'


class InitIn(BaseModel):
    template_id: int


class ThemeSaveIn(BaseModel):
    template_id: int
    axis: str
    name: str = ''
    css: str = ''


class PageSaveIn(BaseModel):
    id: int | None = None
    template_id: int
    url: str = ''
    header: str = ''
    blocks: str = BLOCKS_EMPTY


class StructureSaveIn(BaseModel):
    template_id: int
    header: Any = None
    footer: Any = None


def _paths():
    return sysconfig.get('paths') or {}


def _template_base(folder):
    # Пока отдаём локальный file://-путь; на бэке путь меняется в одном месте.
    root = _paths().get('templates', '/var/www/sv-cms/htdocs/templates')
    name = (folder or '').replace('\\', '/').strip()
    for pref in ('./templates/', '/templates/', 'templates/', './'):
        if name.startswith(pref):
            name = name[len(pref):]
            break
    name = name.strip('/')
    return 'file://' + os.path.join(root, name) + '/'


def _preview_config(folder):
    return {
        'templateBase': _template_base(folder),
        'color': 'digitalstrateg',
        'style': 'soft',
        'layout': 'standard',
        'font': 'inter',
        'engine': True,
    }


def _normalize_blocks(raw):
    if raw is None or raw == '':
        return BLOCKS_EMPTY
    if isinstance(raw, (dict, list)):
        data = raw
    else:
        data = json.loads(raw)
    if isinstance(data, list):
        data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': data}
    elif isinstance(data, dict) and 'blocks' not in data:
        data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': []}
    return json.dumps(data, ensure_ascii=False)


def _parse_blocks(raw):
    try:
        return json.loads(raw) if raw else json.loads(BLOCKS_EMPTY)
    except Exception:
        return json.loads(BLOCKS_EMPTY)


# ---------- шапка/подвал на уровень шаблона ----------

def _doc_from_raw(raw):
    """Приводит блок/список/документ к формату v2 или None."""
    if raw is None or raw == '':
        return None
    if isinstance(raw, (dict, list)):
        data = raw
    else:
        try:
            data = json.loads(raw)
        except Exception:
            return None
    if isinstance(data, list):
        data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': data}
    elif isinstance(data, dict) and 'blocks' not in data:
        if 'type' in data:
            data = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': [data]}
        else:
            return None
    if not data.get('blocks'):
        return None
    return data


def _first_block(doc, btype):
    for b in (doc or {}).get('blocks', []):
        if b.get('type') == btype:
            return b
    return None


async def _structure_from_pages(db, template_id):
    """Запасной источник структуры: первая найденная шапка/подвал среди страниц."""
    rows = await db.query(
        query='SELECT blocks FROM template_page WHERE template_id=%s ORDER BY id',
        values=[template_id],
        errors=[],
    ) or []
    header = footer = None
    for row in rows:
        doc = _doc_from_raw(row.get('blocks'))
        if doc is None:
            continue
        if header is None:
            header = _first_block(doc, 'header')
        if footer is None:
            footer = _first_block(doc, 'footer')
        if header is not None and footer is not None:
            break
    return header, footer


async def _structure_get(db, template_id):
    row = await db.query(
        query='SELECT header_blocks, footer_blocks FROM template_constructor WHERE template_id=%s',
        values=[template_id],
        onerow=1,
        errors=[],
    ) or {}
    header = _first_block(_doc_from_raw(row.get('header_blocks')), 'header')
    footer = _first_block(_doc_from_raw(row.get('footer_blocks')), 'footer')
    if header is None and footer is None:
        page_header, page_footer = await _structure_from_pages(db, template_id)
        header = header if header is not None else page_header
        footer = footer if footer is not None else page_footer
    return {'header': header, 'footer': footer}


def _structure_payload(raw, btype):
    """Достаёт нужный блок из присланного документа/блока, нормализует."""
    if raw is None:
        return None
    if isinstance(raw, dict) and raw.get('type') == btype:
        return raw
    doc = _doc_from_raw(raw)
    return _first_block(doc, btype)


async def _structure_store(db, template_id, header, footer):
    h = json.dumps(header, ensure_ascii=False) if header else None
    f = json.dumps(footer, ensure_ascii=False) if footer else None
    exists = await db.query(
        query='SELECT template_id FROM template_constructor WHERE template_id=%s',
        values=[template_id],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query='UPDATE template_constructor SET header_blocks=%s, footer_blocks=%s WHERE template_id=%s',
            values=[h, f, template_id],
            errors=[],
        )
    else:
        await db.query(
            query='INSERT INTO template_constructor(template_id, header_blocks, footer_blocks) VALUES(%s,%s,%s)',
            values=[template_id, h, f],
            errors=[],
        )


async def _structure_fanout(db, template_id, header, footer):
    """Раскладывает шапку/подвал по всем страницам шаблона (пока сайт читает blocks)."""
    rows = await db.query(
        query='SELECT id, blocks FROM template_page WHERE template_id=%s',
        values=[template_id],
        errors=[],
    ) or []
    for row in rows:
        doc = _doc_from_raw(row.get('blocks'))
        rest = [b for b in (doc or {}).get('blocks', []) if b.get('type') not in ('header', 'footer')]
        blocks = []
        if header:
            blocks.append(header)
        blocks += rest
        if footer:
            blocks.append(footer)
        out = {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': blocks}
        await db.query(
            query='UPDATE template_page SET blocks=%s WHERE id=%s',
            values=[json.dumps(out, ensure_ascii=False), row['id']],
            errors=[],
        )


async def _apply_structure(db, template_id, doc):
    """Вставляет канонические шапку/подвал в документ страницы перед сохранением."""
    st = await _structure_get(db, template_id)
    header, footer = st.get('header'), st.get('footer')
    if header is None and footer is None:
        return doc
    rest = [b for b in (doc or {}).get('blocks', []) if b.get('type') not in ('header', 'footer')]
    blocks = []
    if header is not None:
        blocks.append(header)
    blocks += rest
    if footer is not None:
        blocks.append(footer)
    return {'schema': 'svcms.page_blocks', 'version': 2, 'blocks': blocks}


THEME_AXES = ('color', 'style', 'layout', 'font')
THEME_DEFAULTS = {'color': 'digitalstrateg', 'style': 'soft', 'layout': 'standard', 'font': 'inter'}
THEME_TABLES = {
    'color': 'template_theme_color',
    'style': 'template_theme_style',
    'layout': 'template_theme_layout',
    'font': 'template_theme_font',
}


def _template_dir(folder):
    root = _paths().get('templates', '/var/www/sv-cms/htdocs/templates')
    name = (folder or '').replace('\\', '/').strip()
    for pref in ('./templates/', '/templates/', 'templates/', './'):
        if name.startswith(pref):
            name = name[len(pref):]
            break
    return os.path.join(root, name.strip('/'))


async def _scheme_css_db(db, axis, name, custom):
    if custom:
        return custom
    tbl = THEME_TABLES.get(axis)
    if not tbl or not name:
        return ''
    row = await db.query(
        query=f'SELECT css FROM {tbl} WHERE name=%s',
        values=[name],
        onerow=1,
        errors=[],
    )
    return (row or {}).get('css') or ''


async def _theme_row(db, template_id):
    row = await db.query(
        query='SELECT * FROM template_constructor WHERE template_id=%s',
        values=[template_id],
        onerow=1,
        errors=[],
    )
    if row:
        return row
    out = {'template_id': template_id}
    out.update(THEME_DEFAULTS)
    return out


async def _theme_json_db(db, row):
    out = {}
    for axis in THEME_AXES:
        name = row.get(axis) or THEME_DEFAULTS[axis]
        css = row.get(axis + '_css') or ''
        custom = bool(css)
        if not css:
            srow = await db.query(
                query=f'SELECT css, is_custom FROM {THEME_TABLES[axis]} WHERE name=%s',
                values=[name],
                onerow=1,
                errors=[],
            )
            if srow:
                css = srow.get('css') or ''
                custom = bool(srow.get('is_custom'))
        out[axis] = {'name': name, 'custom': custom, 'css': css}
    return out



@router.post('/init')
async def page_constructor_init(request: Request, r: InitIn):
    db = request.state.engine.db_read
    t = await db.query(
        query='SELECT template_id, header, folder FROM template WHERE template_id=%s',
        values=[r.template_id],
        onerow=1,
        errors=[],
    )
    if not t:
        return {'success': False, 'errors': ['шаблон не найден']}

    pages = await db.query(
        query='SELECT id, url, header FROM template_page WHERE template_id=%s ORDER BY header',
        values=[r.template_id],
        errors=[],
    )
    theme = await _theme_json_db(db, await _theme_row(db, r.template_id))
    structure = await _structure_get(db, r.template_id)
    config = _preview_config(t['folder'])
    for axis in THEME_AXES:
        config[axis] = theme[axis]['name']
    return {
        'success': True,
        'errors': [],
        'template': {'id': t['template_id'], 'header': t['header'], 'folder': t['folder']},
        'templateBase': _template_base(t['folder']),
        'config': config,
        'theme': theme,
        'structure': structure,
        'pages': pages or [],
    }


@router.get('/page/{page_id}')
async def page_get(request: Request, page_id: int):
    db = request.state.engine.db_read
    p = await db.query(
        query='SELECT id, template_id, url, header, blocks FROM template_page WHERE id=%s',
        values=[page_id],
        onerow=1,
        errors=[],
    )
    if not p:
        return {'success': False, 'errors': ['страница не найдена']}
    p['blocks'] = _parse_blocks(p.get('blocks'))
    return {'success': True, 'errors': [], 'page': p}


@router.post('/page/save')
async def page_save(request: Request, r: PageSaveIn):
    db = request.state.engine.db_write
    url = (r.url or '').strip()
    if not url:
        return {'success': False, 'errors': ['укажите url страницы']}
    try:
        doc = _doc_from_raw(r.blocks) or json.loads(BLOCKS_EMPTY)
    except Exception:
        return {'success': False, 'errors': ['некорректный JSON блоков']}
    doc = await _apply_structure(db, r.template_id, doc)
    blocks = json.dumps(doc, ensure_ascii=False)

    if r.id:
        await db.query(
            query='UPDATE template_page SET url=%s, header=%s, blocks=%s WHERE id=%s',
            values=[url, r.header, blocks, r.id],
            errors=[],
        )
        return {'success': True, 'errors': [], 'id': r.id}

    dup = await db.query(
        query='SELECT id FROM template_page WHERE template_id=%s AND url=%s',
        values=[r.template_id, url],
        onerow=1,
        errors=[],
    )
    if dup:
        return {'success': False, 'errors': ['страница с таким url уже есть у этого шаблона']}

    await db.query(
        query='INSERT INTO template_page(template_id,url,header,blocks) VALUES(%s,%s,%s,%s)',
        values=[r.template_id, url, r.header, blocks],
        errors=[],
    )
    row = await db.query(
        query='SELECT id FROM template_page WHERE template_id=%s AND url=%s',
        values=[r.template_id, url],
        onerow=1,
        errors=[],
    )
    return {'success': True, 'errors': [], 'id': row['id'] if row else None}


@router.post('/page/{page_id}/delete')
async def page_delete(request: Request, page_id: int):
    db = request.state.engine.db_write
    await db.query(query='DELETE FROM template_page WHERE id=%s', values=[page_id], errors=[])
    return {'success': True, 'errors': []}


# ---------- шапка/подвал на уровень шаблона ----------

@router.get('/structure/{template_id}')
async def structure_get(request: Request, template_id: int):
    db = request.state.engine.db_read
    return {'success': True, 'errors': [], 'structure': await _structure_get(db, template_id)}


@router.post('/structure/save')
async def structure_save(request: Request, r: StructureSaveIn):
    db = request.state.engine.db_write
    header = _structure_payload(r.header, 'header')
    footer = _structure_payload(r.footer, 'footer')
    await _structure_store(db, r.template_id, header, footer)
    await _structure_fanout(db, r.template_id, header, footer)
    return {'success': True, 'errors': [], 'structure': {'header': header, 'footer': footer}}


# ---------- базовый набор страниц ----------

@router.post('/base-pages')
async def base_pages(request: Request, r: InitIn):
    db = request.state.engine.db_write
    rows = await db.query(
        query='SELECT url, header, blocks FROM template_pages_base ORDER BY sort, url',
        errors=[],
    ) or []

    created, skipped = [], []
    for page in rows:
        url = (page.get('url') or '').strip()
        if not url:
            continue
        exists = await db.query(
            query='SELECT id FROM template_page WHERE template_id=%s AND url=%s',
            values=[r.template_id, url],
            onerow=1,
            errors=[],
        )
        if exists:
            skipped.append(url)
            continue
        doc = _normalize_blocks(page.get('blocks'))
        await db.query(
            query='INSERT INTO template_page(template_id,url,header,blocks) VALUES(%s,%s,%s,%s)',
            values=[r.template_id, url, page.get('header') or '', doc],
            errors=[],
        )
        created.append(url)

    return {'success': True, 'errors': [], 'created': created, 'skipped': skipped}



# ---------- тема шаблона (конструкторы стилей) ----------

@router.get('/theme/{template_id}')
async def theme_get(request: Request, template_id: int):
    db = request.state.engine.db_read
    row = await _theme_row(db, template_id)
    return {'success': True, 'errors': [], 'theme': await _theme_json_db(db, row)}


@router.post('/theme/save')
async def theme_save(request: Request, r: ThemeSaveIn):
    if r.axis not in THEME_AXES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_write
    name = (r.name or '').strip() or THEME_DEFAULTS[r.axis]
    css = r.css or ''
    col = r.axis
    csscol = r.axis + '_css'
    if css:
        tbl = THEME_TABLES[r.axis]
        srow = await db.query(
            query=f'SELECT name FROM {tbl} WHERE name=%s',
            values=[name],
            onerow=1,
            errors=[],
        )
        if srow:
            await db.query(
                query=f'UPDATE {tbl} SET css=%s, is_custom=1 WHERE name=%s',
                values=[css, name],
                errors=[],
            )
        else:
            await db.query(
                query=f'INSERT INTO {tbl}(name,label,css,is_custom) VALUES(%s,%s,%s,1)',
                values=[name, name, css],
                errors=[],
            )
    exists = await db.query(
        query='SELECT template_id FROM template_constructor WHERE template_id=%s',
        values=[r.template_id],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query=f'UPDATE template_constructor SET {col}=%s, {csscol}=NULL WHERE template_id=%s',
            values=[name, r.template_id],
            errors=[],
        )
    else:
        await db.query(
            query=f'INSERT INTO template_constructor(template_id, {col}) VALUES(%s,%s)',
            values=[r.template_id, name],
            errors=[],
        )
    return {'success': True, 'errors': [], 'name': name, 'custom': bool(css)}


@router.get('/theme/{template_id}/styles.css')
async def theme_css(request: Request, template_id: int):
    db = request.state.engine.db_read
    row = await _theme_row(db, template_id)
    parts = []
    for axis in THEME_AXES:
        name = row.get(axis) or THEME_DEFAULTS[axis]
        css = await _scheme_css_db(db, axis, name, row.get(axis + '_css'))
        if css:
            parts.append('/* ===== %s: %s ===== */\n%s' % (axis, name, css))
    body = '\n\n'.join(parts) or '/* тема не задана */\n'
    return Response(content=body, media_type='text/css')


# ---------- схемы темы (БД) ----------

class SchemeSaveIn(BaseModel):
    axis: str
    name: str
    label: str = ''
    short: str = ''
    descr: str = ''
    css: str = ''


@router.get('/theme-schemes/{axis}')
async def schemes_list(request: Request, axis: str):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_read
    rows = await db.query(
        query=f'SELECT name, label, short, descr, is_default, is_custom FROM {THEME_TABLES[axis]} ORDER BY sort, name',
        errors=[],
    ) or []
    return {'success': True, 'errors': [], 'axis': axis, 'schemes': rows}


@router.get('/theme-schemes/{axis}/{name}')
async def scheme_get(request: Request, axis: str, name: str):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_read
    row = await db.query(
        query=f'SELECT name, label, short, descr, css, is_default, is_custom FROM {THEME_TABLES[axis]} WHERE name=%s',
        values=[name],
        onerow=1,
        errors=[],
    )
    if not row:
        return {'success': False, 'errors': ['схема не найдена']}
    return {'success': True, 'errors': [], 'scheme': row}


@router.get('/theme-schemes/{axis}/{name}/file.css')
async def scheme_css(request: Request, axis: str, name: str):
    if axis not in THEME_TABLES:
        return Response(content='/* неизвестная ось */\n', media_type='text/css')
    db = request.state.engine.db_read
    row = await db.query(
        query=f'SELECT css FROM {THEME_TABLES[axis]} WHERE name=%s',
        values=[name],
        onerow=1,
        errors=[],
    )
    body = (row or {}).get('css') or '/* схема не найдена */\n'
    return Response(content=body, media_type='text/css')


@router.post('/theme-schemes/save')
async def scheme_save(request: Request, r: SchemeSaveIn):
    if r.axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    name = (r.name or '').strip()
    if not name:
        return {'success': False, 'errors': ['укажите имя схемы']}
    db = request.state.engine.db_write
    tbl = THEME_TABLES[r.axis]
    exists = await db.query(
        query=f'SELECT name FROM {tbl} WHERE name=%s',
        values=[name],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query=f'UPDATE {tbl} SET label=%s, short=%s, descr=%s, css=%s WHERE name=%s',
            values=[r.label, r.short, r.descr, r.css, name],
            errors=[],
        )
    else:
        await db.query(
            query=f'INSERT INTO {tbl}(name,label,short,descr,css,is_custom) VALUES(%s,%s,%s,%s,%s,1)',
            values=[name, r.label, r.short, r.descr, r.css],
            errors=[],
        )
    return {'success': True, 'errors': [], 'name': name}


@router.post('/theme-schemes/{axis}/{name}/delete')
async def scheme_delete(request: Request, axis: str, name: str):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_write
    await db.query(
        query=f'DELETE FROM {THEME_TABLES[axis]} WHERE name=%s AND is_custom=1',
        values=[name],
        errors=[],
    )
    return {'success': True, 'errors': []}
