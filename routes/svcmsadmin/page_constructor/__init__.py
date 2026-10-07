import json
import os
import re
from typing import Any

from fastapi import APIRouter, Request, Response, File, Form, UploadFile
from pydantic import BaseModel

from config import config as sysconfig


router = APIRouter()

BLOCKS_EMPTY = '{"schema": "svcms.page_blocks", "version": 2, "blocks": []}'

# Транслит для имён загружаемых картинок (рус. → латиница).
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}


def _slugify_filename(name):
    """Имя файла: латиница/цифры/.-_, пробелы и кириллица → транслит/дефис."""
    name = (name or '').strip()
    base, dot, ext = name.rpartition('.')
    if not dot:
        base, ext = name, ''
    out = []
    for ch in base.lower():
        if ch in _TRANSLIT:
            out.append(_TRANSLIT[ch])
        elif re.match(r'[a-z0-9._-]', ch):
            out.append(ch)
        else:
            out.append('-')
    slug = re.sub(r'-+', '-', ''.join(out)).strip('-') or 'file'
    return slug + ('.' + ext.lower() if ext else '')


class InitIn(BaseModel):
    domain_id: int


class BasePagesIn(BaseModel):
    domain_id: int
    set_id: int | None = None
    overwrite: bool = False


class BaseSetCreateIn(BaseModel):
    name: str
    domain_id: int | None = None


class BaseSetRenameIn(BaseModel):
    set_id: int
    name: str


class BaseSetDomainIn(BaseModel):
    set_id: int
    domain_id: int


class BaseSetIdIn(BaseModel):
    set_id: int


class ThemeSaveIn(BaseModel):
    domain_id: int
    axis: str
    name: str = ''
    css: str = ''
    scope: str = 'domain'


class PageSaveIn(BaseModel):
    id: int | None = None
    domain_id: int
    url: str = ''
    header: str = ''
    blocks: str = BLOCKS_EMPTY


class StructureSaveIn(BaseModel):
    domain_id: int
    header: Any = None
    footer: Any = None


def _paths():
    return sysconfig.get('paths') or {}


def _engine_files():
    return _paths().get('engine_files') or '/var/www/svcms-async/sites/files'


def _engine_files_url():
    return (_paths().get('engine_files_url') or '/files').rstrip('/')


async def _project_id_for_domain(db, domain_id):
    row = await db.query(
        query='SELECT project_id FROM domain WHERE domain_id=%s',
        values=[domain_id], onerow=1, errors=[],
    )
    return (row or {}).get('project_id')


def _folder_slug(folder):
    """Санитайз подпапки block-images: только [a-z0-9_-]."""
    return re.sub(r'[^a-z0-9_-]', '', (folder or '').lower()).strip('-_')


def _block_images_dir(project_id, folder=''):
    d = os.path.join(_engine_files(), 'project_%s' % project_id, 'block-images')
    sub = _folder_slug(folder)
    if sub:
        d = os.path.join(d, sub)
    os.makedirs(d, exist_ok=True)
    return d


_RASTER_EXT = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tif', 'tiff'}


def _optimize_to_webp(content):
    """Растровую картинку → webp: exif-поворот, альфа, даунскейл, качество."""
    import io
    from PIL import Image, ImageOps
    img = Image.open(io.BytesIO(content))
    try:
        img = ImageOps.exif_transpose(img)
    except Exception:
        pass
    has_alpha = img.mode in ('RGBA', 'LA') or (
        img.mode == 'P' and 'transparency' in img.info)
    img = img.convert('RGBA' if has_alpha else 'RGB')
    max_side = int(_paths().get('block_images_max_side') or 1920)
    quality = int(_paths().get('block_images_quality') or 82)
    w, h = img.size
    m = max(w, h)
    if max_side and m > max_side:  # только уменьшаем
        scale = max_side / float(m)
        img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, 'WEBP', quality=quality, method=6)
    return buf.getvalue()


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


def _blocks_error(raw):
    """Текст ошибки разбора blocks (None — JSON валиден).

    Битый JSON раньше молча превращался в пустой документ, и страница в
    конструкторе выглядела пустой без объяснения. Теперь such случай
    отдаётся наверх (page_get -> page.blocks_error), чтобы редактор показал
    сообщение и предложил починить JSON вручную.
    """
    if not raw or not str(raw).strip():
        return None
    try:
        json.loads(raw)
        return None
    except Exception as e:
        return f'JSON блоков страницы повреждён: {e}. Откройте JSON-редактор и исправьте его вручную.'


# ---------- шапка/подвал на уровень домена ----------

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


async def _structure_from_pages(db, domain_id):
    """Запасной источник структуры: первая найденная шапка/подвал среди страниц."""
    rows = await db.query(
        query='SELECT blocks FROM domain_page WHERE domain_id=%s ORDER BY id',
        values=[domain_id],
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


async def _structure_get(db, domain_id):
    row = await db.query(
        query='SELECT header_blocks, footer_blocks FROM domain_constructor WHERE domain_id=%s',
        values=[domain_id],
        onerow=1,
        errors=[],
    ) or {}
    header = _first_block(_doc_from_raw(row.get('header_blocks')), 'header')
    footer = _first_block(_doc_from_raw(row.get('footer_blocks')), 'footer')
    if header is None and footer is None:
        page_header, page_footer = await _structure_from_pages(db, domain_id)
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


async def _structure_store(db, domain_id, header, footer):
    h = json.dumps(header, ensure_ascii=False) if header else None
    f = json.dumps(footer, ensure_ascii=False) if footer else None
    exists = await db.query(
        query='SELECT domain_id FROM domain_constructor WHERE domain_id=%s',
        values=[domain_id],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query='UPDATE domain_constructor SET header_blocks=%s, footer_blocks=%s WHERE domain_id=%s',
            values=[h, f, domain_id],
            errors=[],
        )
    else:
        await db.query(
            query='INSERT INTO domain_constructor(domain_id, header_blocks, footer_blocks) VALUES(%s,%s,%s)',
            values=[domain_id, h, f],
            errors=[],
        )


async def _structure_fanout(db, domain_id, header, footer):
    """Раскладывает шапку/подвал по всем страницам домена (пока сайт читает blocks)."""
    rows = await db.query(
        query='SELECT id, blocks FROM domain_page WHERE domain_id=%s',
        values=[domain_id],
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
            query='UPDATE domain_page SET blocks=%s WHERE id=%s',
            values=[json.dumps(out, ensure_ascii=False), row['id']],
            errors=[],
        )


async def _apply_structure(db, domain_id, doc):
    """Вставляет канонические шапку/подвал в документ страницы перед сохранением."""
    st = await _structure_get(db, domain_id)
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
# Порядок сборки CSS = порядок каскада: style после layout (декор стиля
# перекрывает оформление пресета компоновки). См. sites/lib/theme.py.
THEME_ORDER = ('color', 'layout', 'style', 'font')
THEME_DEFAULTS = {'color': 'digitalstrateg', 'style': 'soft', 'layout': 'standard', 'font': 'inter'}
THEME_TABLES = {
    'color': 'domain_theme_color',
    'style': 'domain_theme_style',
    'layout': 'domain_theme_layout',
    'font': 'domain_theme_font',
}

# Схема домена: domain_id=0 — общий пресет, >0 — индивидуальный схема домена.
async def _scheme_find(db, axis, domain_id, name):
    """Ищет схему: сначала индивидуальную домена, затем общую."""
    tbl = THEME_TABLES.get(axis)
    if not tbl or not name:
        return None
    row = await db.query(
        query=f'SELECT * FROM {tbl} WHERE domain_id=%s AND header=%s',
        values=[domain_id, name],
        onerow=1,
        errors=[],
    )
    if row:
        return row
    return await db.query(
        query=f'SELECT * FROM {tbl} WHERE domain_id=0 AND header=%s',
        values=[name],
        onerow=1,
        errors=[],
    )


async def _scheme_upsert(db, axis, domain_id, name, css, scope='domain'):
    """Пишет схему. scope='shared' — общую (domain_id=0), иначе индивидуальную домена.
    Общую схему индивидуальный домен не перетирает — создаёт свою копию."""
    tbl = THEME_TABLES[axis]
    own = 0 if scope == 'shared' else domain_id
    exists = await db.query(
        query=f'SELECT domain_id FROM {tbl} WHERE domain_id=%s AND header=%s',
        values=[own, name],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query=f'UPDATE {tbl} SET css=%s, is_custom=1 WHERE domain_id=%s AND header=%s',
            values=[css, own, name],
            errors=[],
        )
    else:
        label = name
        if own:
            base = await db.query(
                query=f'SELECT label FROM {tbl} WHERE domain_id=0 AND header=%s',
                values=[name],
                onerow=1,
                errors=[],
            )
            if base and base.get('label'):
                label = base['label']
        await db.query(
            query=f'INSERT INTO {tbl}(domain_id,header,label,css,is_custom) VALUES(%s,%s,%s,%s,1)',
            values=[own, name, label, css],
            errors=[],
        )
    return own


async def _scheme_css_db(db, axis, name, custom, domain_id):
    if custom:
        return custom
    row = await _scheme_find(db, axis, domain_id, name)
    return (row or {}).get('css') or ''


async def _theme_row(db, domain_id):
    row = await db.query(
        query='SELECT * FROM domain_constructor WHERE domain_id=%s',
        values=[domain_id],
        onerow=1,
        errors=[],
    )
    if row:
        return row
    out = {'domain_id': domain_id}
    out.update(THEME_DEFAULTS)
    return out


async def _theme_json_db(db, row, domain_id):
    out = {}
    for axis in THEME_AXES:
        name = row.get(axis) or THEME_DEFAULTS[axis]
        css = row.get(axis + '_css') or ''
        custom = bool(css)
        if not css:
            srow = await _scheme_find(db, axis, domain_id, name)
            if srow:
                css = srow.get('css') or ''
                custom = bool(srow.get('is_custom'))
        out[axis] = {'name': name, 'custom': custom, 'css': css}
    return out


@router.post('/init')
async def page_constructor_init(request: Request, r: InitIn):
    db = request.state.engine.db_read
    d = await db.query(
        query=(
            'SELECT d.domain_id, d.domain, d.template_id, d.project_id, t.header, t.folder'
            ' FROM domain d JOIN template t ON t.template_id=d.template_id'
            ' WHERE d.domain_id=%s'
        ),
        values=[r.domain_id],
        onerow=1,
        errors=[],
    )
    if not d:
        return {'success': False, 'errors': ['домен не найден']}

    pages = await db.query(
        query='SELECT id, url, header FROM domain_page WHERE domain_id=%s ORDER BY header',
        values=[r.domain_id],
        errors=[],
    )
    theme_row = await _theme_row(db, r.domain_id)
    theme = await _theme_json_db(db, theme_row, r.domain_id)
    structure = await _structure_get(db, r.domain_id)
    base_sets = await _base_sets_list(db)
    config = _preview_config(d['folder'])
    # Базовый URL картинок проекта для превью (block-images конструктора).
    config['filesBase'] = '%s/project_%s/' % (_engine_files_url(), d.get('project_id'))
    for axis in THEME_AXES:
        config[axis] = theme[axis]['name']
    return {
        'success': True,
        'errors': [],
        'domain': {
            'id': d['domain_id'],
            'domain': d['domain'],
            'template_id': d['template_id'],
            'header': d['header'],
            'folder': d['folder'],
        },
        'templateBase': _template_base(d['folder']),
        'config': config,
        'theme': theme,
        'structure': structure,
        'base_set_id': theme_row.get('base_set_id'),
        'base_sets': base_sets,
        'pages': pages or [],
    }


@router.get('/page/{page_id}')
async def page_get(request: Request, page_id: int):
    db = request.state.engine.db_read
    p = await db.query(
        query='SELECT id, domain_id, url, header, blocks FROM domain_page WHERE id=%s',
        values=[page_id],
        onerow=1,
        errors=[],
    )
    if not p:
        return {'success': False, 'errors': ['страница не найдена']}
    raw_blocks = p.get('blocks')
    err = _blocks_error(raw_blocks)
    p['blocks'] = _parse_blocks(raw_blocks)
    p['blocks_raw'] = raw_blocks if err else None
    p['blocks_error'] = err
    return {'success': True, 'errors': [err] if err else [], 'page': p}


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
    doc = await _apply_structure(db, r.domain_id, doc)
    blocks = json.dumps(doc, ensure_ascii=False)

    if r.id:
        await db.query(
            query='UPDATE domain_page SET url=%s, header=%s, blocks=%s WHERE id=%s',
            values=[url, r.header, blocks, r.id],
            errors=[],
        )
        return {'success': True, 'errors': [], 'id': r.id}

    dup = await db.query(
        query='SELECT id FROM domain_page WHERE domain_id=%s AND url=%s',
        values=[r.domain_id, url],
        onerow=1,
        errors=[],
    )
    if dup:
        return {'success': False, 'errors': ['страница с таким url уже есть у этого домена']}

    await db.query(
        query='INSERT INTO domain_page(domain_id,url,header,blocks) VALUES(%s,%s,%s,%s)',
        values=[r.domain_id, url, r.header, blocks],
        errors=[],
    )
    row = await db.query(
        query='SELECT id FROM domain_page WHERE domain_id=%s AND url=%s',
        values=[r.domain_id, url],
        onerow=1,
        errors=[],
    )
    return {'success': True, 'errors': [], 'id': row['id'] if row else None}


@router.post('/page/{page_id}/delete')
async def page_delete(request: Request, page_id: int):
    db = request.state.engine.db_write
    await db.query(query='DELETE FROM domain_page WHERE id=%s', values=[page_id], errors=[])
    return {'success': True, 'errors': []}


# ---------- шапка/подвал на уровень домена ----------

@router.get('/structure/{domain_id}')
async def structure_get(request: Request, domain_id: int):
    db = request.state.engine.db_read
    return {'success': True, 'errors': [], 'structure': await _structure_get(db, domain_id)}


@router.post('/structure/save')
async def structure_save(request: Request, r: StructureSaveIn):
    db = request.state.engine.db_write
    header = _structure_payload(r.header, 'header')
    footer = _structure_payload(r.footer, 'footer')
    await _structure_store(db, r.domain_id, header, footer)
    await _structure_fanout(db, r.domain_id, header, footer)
    return {'success': True, 'errors': [], 'structure': {'header': header, 'footer': footer}}


# ---------- базовый набор страниц ----------

async def _base_sets_list(db):
    return await db.query(
        query='SELECT s.id, s.name, s.sort, s.is_default, count(b.id) pages '
              'FROM base_pages_set s '
              'LEFT JOIN template_pages_base b ON b.set_id=s.id '
              'GROUP BY s.id, s.name, s.sort, s.is_default '
              'ORDER BY s.is_default DESC, s.sort, s.name',
        errors=[],
    ) or []


async def _default_set_id(db):
    row = await db.query(
        query='SELECT id FROM base_pages_set ORDER BY is_default DESC, sort, id LIMIT 1',
        onerow=1,
        errors=[],
    )
    return row['id'] if row else None


async def _remember_base_set(db, domain_id, set_id):
    await db.query(
        query='INSERT INTO domain_constructor(domain_id, base_set_id) VALUES(%s,%s) '
              'ON DUPLICATE KEY UPDATE base_set_id=VALUES(base_set_id)',
        values=[domain_id, set_id],
        errors=[],
    )


async def _copy_domain_pages_to_set(db, domain_id, set_id):
    rows = await db.query(
        query='SELECT url, header, blocks FROM domain_page WHERE domain_id=%s ORDER BY id',
        values=[domain_id],
        errors=[],
    ) or []
    count = 0
    for i, page in enumerate(rows):
        url = (page.get('url') or '').strip()
        if not url:
            continue
        await db.query(
            query='INSERT INTO template_pages_base(set_id, url, header, blocks, sort) '
                  'VALUES(%s,%s,%s,%s,%s)',
            values=[set_id, url, page.get('header') or '', _normalize_blocks(page.get('blocks')), i],
            errors=[],
        )
        count += 1
    return count


@router.post('/base-pages')
async def base_pages(request: Request, r: BasePagesIn):
    db = request.state.engine.db_write
    set_id = r.set_id or await _default_set_id(db)
    if not set_id:
        return {'success': False, 'errors': ['не найдено ни одного набора страниц']}
    st = await db.query(
        query='SELECT id, name FROM base_pages_set WHERE id=%s',
        values=[set_id],
        onerow=1,
        errors=[],
    )
    if not st:
        return {'success': False, 'errors': ['набор не найден']}

    rows = await db.query(
        query='SELECT url, header, blocks FROM template_pages_base WHERE set_id=%s ORDER BY sort, url',
        values=[set_id],
        errors=[],
    ) or []

    created, updated, skipped = [], [], []
    for page in rows:
        url = (page.get('url') or '').strip()
        if not url:
            continue
        doc = _normalize_blocks(page.get('blocks'))
        exists = await db.query(
            query='SELECT id FROM domain_page WHERE domain_id=%s AND url=%s',
            values=[r.domain_id, url],
            onerow=1,
            errors=[],
        )
        if exists:
            if r.overwrite:
                await db.query(
                    query='UPDATE domain_page SET header=%s, blocks=%s WHERE id=%s',
                    values=[page.get('header') or '', doc, exists['id']],
                    errors=[],
                )
                updated.append(url)
            else:
                skipped.append(url)
            continue
        await db.query(
            query='INSERT INTO domain_page(domain_id,url,header,blocks) VALUES(%s,%s,%s,%s)',
            values=[r.domain_id, url, page.get('header') or '', doc],
            errors=[],
        )
        created.append(url)

    await _remember_base_set(db, r.domain_id, set_id)
    return {
        'success': True,
        'errors': [],
        'set_id': set_id,
        'set_name': st.get('name'),
        'created': created,
        'updated': updated,
        'skipped': skipped,
    }


@router.get('/base-sets')
async def base_sets_list(request: Request):
    db = request.state.engine.db_read
    return {
        'success': True,
        'errors': [],
        'sets': await _base_sets_list(db),
        'default_set_id': await _default_set_id(db),
    }


@router.post('/base-sets/create')
async def base_set_create(request: Request, r: BaseSetCreateIn):
    db = request.state.engine.db_write
    name = (r.name or '').strip()
    if not name:
        return {'success': False, 'errors': ['укажите имя набора']}
    dup = await db.query(
        query='SELECT id FROM base_pages_set WHERE name=%s',
        values=[name],
        onerow=1,
        errors=[],
    )
    if dup:
        return {'success': False, 'errors': ['набор с таким именем уже есть']}
    errors = []
    set_id = await db.save(table='base_pages_set', data={'name': name}, errors=errors)
    if errors or not set_id:
        return {'success': False, 'errors': errors or ['не удалось создать набор']}
    pages = await _copy_domain_pages_to_set(db, r.domain_id, set_id) if r.domain_id else 0
    return {'success': True, 'errors': [], 'set': {'id': set_id, 'name': name, 'pages': pages}}


@router.post('/base-sets/rename')
async def base_set_rename(request: Request, r: BaseSetRenameIn):
    db = request.state.engine.db_write
    name = (r.name or '').strip()
    if not name:
        return {'success': False, 'errors': ['укажите имя набора']}
    dup = await db.query(
        query='SELECT id FROM base_pages_set WHERE name=%s AND id<>%s',
        values=[name, r.set_id],
        onerow=1,
        errors=[],
    )
    if dup:
        return {'success': False, 'errors': ['набор с таким именем уже есть']}
    await db.query(
        query='UPDATE base_pages_set SET name=%s WHERE id=%s',
        values=[name, r.set_id],
        errors=[],
    )
    return {'success': True, 'errors': []}


@router.post('/base-sets/update-from-domain')
async def base_set_update_from_domain(request: Request, r: BaseSetDomainIn):
    db = request.state.engine.db_write
    st = await db.query(
        query='SELECT id, name FROM base_pages_set WHERE id=%s',
        values=[r.set_id],
        onerow=1,
        errors=[],
    )
    if not st:
        return {'success': False, 'errors': ['набор не найден']}
    await db.query(
        query='DELETE FROM template_pages_base WHERE set_id=%s',
        values=[r.set_id],
        errors=[],
    )
    pages = await _copy_domain_pages_to_set(db, r.domain_id, r.set_id)
    return {'success': True, 'errors': [], 'set_id': r.set_id, 'set_name': st.get('name'), 'pages': pages}


@router.post('/base-sets/delete')
async def base_set_delete(request: Request, r: BaseSetIdIn):
    db = request.state.engine.db_write
    st = await db.query(
        query='SELECT id, name, is_default FROM base_pages_set WHERE id=%s',
        values=[r.set_id],
        onerow=1,
        errors=[],
    )
    if not st:
        return {'success': False, 'errors': ['набор не найден']}
    if int(st.get('is_default') or 0) == 1:
        return {'success': False, 'errors': ['нельзя удалить набор по умолчанию']}
    total = await db.query(
        query='SELECT count(*) FROM base_pages_set',
        onevalue=1,
        errors=[],
    ) or 0
    if total <= 1:
        return {'success': False, 'errors': ['нельзя удалить последний набор']}
    await db.query(
        query='DELETE FROM base_pages_set WHERE id=%s',
        values=[r.set_id],
        errors=[],
    )
    return {'success': True, 'errors': []}


# ---------- тема домена (конструкторы стилей) ----------

@router.get('/theme/{domain_id}')
async def theme_get(request: Request, domain_id: int):
    db = request.state.engine.db_read
    row = await _theme_row(db, domain_id)
    return {'success': True, 'errors': [], 'theme': await _theme_json_db(db, row, domain_id)}


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
        await _scheme_upsert(db, r.axis, r.domain_id, name, css, r.scope)
    exists = await db.query(
        query='SELECT domain_id FROM domain_constructor WHERE domain_id=%s',
        values=[r.domain_id],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query=f'UPDATE domain_constructor SET {col}=%s, {csscol}=NULL WHERE domain_id=%s',
            values=[name, r.domain_id],
            errors=[],
        )
    else:
        await db.query(
            query=f'INSERT INTO domain_constructor(domain_id, {col}) VALUES(%s,%s)',
            values=[r.domain_id, name],
            errors=[],
        )
    return {'success': True, 'errors': [], 'name': name, 'custom': bool(css)}


@router.get('/theme/{domain_id}/styles.css')
async def theme_css(request: Request, domain_id: int):
    db = request.state.engine.db_read
    row = await _theme_row(db, domain_id)
    parts = []
    for axis in THEME_ORDER:
        name = row.get(axis) or THEME_DEFAULTS[axis]
        css = await _scheme_css_db(db, axis, name, row.get(axis + '_css'), domain_id)
        if css:
            parts.append('/* ===== %s: %s ===== */\n%s' % (axis, name, css))
    body = '\n\n'.join(parts) or '/* тема не задана */\n'
    return Response(content=body, media_type='text/css')


# ---------- картинки блоков проекта (block-images) ----------

@router.get('/block-images')
async def block_images_list(request: Request, domain_id: int = 0, folder: str = ''):
    """Список картинок проекта из /files/project_<id>/block-images[/<folder>]/."""
    db = request.state.engine.db_read
    pid = await _project_id_for_domain(db, domain_id)
    if not pid:
        return {'success': False, 'errors': ['проект не найден'], 'files': []}
    sub = _folder_slug(folder)
    d = _block_images_dir(pid, sub)
    prefix = 'block-images/' + (sub + '/' if sub else '')
    base = '%s/project_%s/%s' % (_engine_files_url(), pid, prefix)
    files = []
    for name in sorted(os.listdir(d)):
        if name.startswith('.') or not os.path.isfile(os.path.join(d, name)):
            continue
        files.append({'name': name, 'path': prefix + name, 'url': base + name})
    return {
        'success': True, 'errors': [],
        'filesBase': '%s/project_%s/' % (_engine_files_url(), pid),
        'folder': sub,
        'files': files,
    }


@router.post('/block-images/upload')
async def block_images_upload(request: Request,
                              domain_id: int = Form(...),
                              folder: str = Form(''),
                              file: UploadFile = File(...)):
    """Загрузка картинки в /files/project_<id>/block-images[/<folder>]/.

    Растровые конвертируются в webp с оптимизацией (даунскейл по длинной
    стороне до block_images_max_side, качество block_images_quality);
    svg сохраняется как есть. Имя — транслит.
    """
    db = request.state.engine.db_read
    pid = await _project_id_for_domain(db, domain_id)
    if not pid:
        return {'success': False, 'errors': ['проект не найден']}

    orig = file.filename or 'file'
    ext = orig.rsplit('.', 1)[-1].lower() if '.' in orig else ''
    raw = await file.read()

    if ext == 'svg':
        content, out_ext = raw, 'svg'
    elif ext in _RASTER_EXT:
        try:
            content, out_ext = _optimize_to_webp(raw), 'webp'
        except Exception:
            return {'success': False, 'errors': ['не удалось обработать изображение']}
    else:
        return {'success': False,
                'errors': ['поддерживаются jpg, png, webp, gif, bmp, svg']}

    sub = _folder_slug(folder)
    d = _block_images_dir(pid, sub)
    base_name = _slugify_filename(orig).rsplit('.', 1)[0] or 'image'
    target = os.path.join(d, base_name + '.' + out_ext)
    i = 1
    while os.path.exists(target):
        target = os.path.join(d, '%s-%d.%s' % (base_name, i, out_ext))
        i += 1

    with open(target, 'wb') as f:
        f.write(content)

    fname = os.path.basename(target)
    prefix = 'block-images/' + (sub + '/' if sub else '')
    return {
        'success': True, 'errors': [],
        'name': fname,
        'path': prefix + fname,
        'url': '%s/project_%s/%s%s' % (_engine_files_url(), pid, prefix, fname),
    }


# ---------- схемы темы (БД) ----------

class SchemeSaveIn(BaseModel):
    axis: str
    name: str
    label: str = ''
    short: str = ''
    descr: str = ''
    css: str = ''
    scope: str = 'domain'
    domain_id: int = 0


@router.get('/theme-schemes/{axis}')
async def schemes_list(request: Request, axis: str, domain_id: int = 0):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_read
    tbl = THEME_TABLES[axis]
    scope = int(domain_id or 0)
    if scope > 0:
        # общие + индивидуальные домена; одноимённая индивидуальная перекрывает общую
        rows = await db.query(
            query=(
                f'SELECT header, label, short, descr, is_default, is_custom, domain_id FROM {tbl}'
                ' WHERE domain_id IN (0, %s)'
                ' ORDER BY (domain_id=0) DESC, sort, header'
            ),
            values=[scope],
            errors=[],
        ) or []
        merged = {}
        for row in rows:
            merged.setdefault(row['header'], row)
        rows = list(merged.values())
    else:
        rows = await db.query(
            query=f'SELECT header, label, short, descr, is_default, is_custom, domain_id FROM {tbl}'
                   ' WHERE domain_id=0 ORDER BY sort, header',
            errors=[],
        ) or []
    return {'success': True, 'errors': [], 'axis': axis, 'schemes': rows}


@router.get('/theme-schemes/{axis}/{name}')
async def scheme_get(request: Request, axis: str, name: str, domain_id: int = 0):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    db = request.state.engine.db_read
    row = await _scheme_find(db, axis, int(domain_id or 0), name)
    if not row:
        return {'success': False, 'errors': ['схема не найдена']}
    return {'success': True, 'errors': [], 'scheme': row}


@router.get('/theme-schemes/{axis}/{name}/file.css')
async def scheme_css(request: Request, axis: str, name: str, domain_id: int = 0):
    if axis not in THEME_TABLES:
        return Response(content='/* неизвестная ось */\n', media_type='text/css')
    db = request.state.engine.db_read
    row = await _scheme_find(db, axis, int(domain_id or 0), name)
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
    own = 0 if r.scope == 'shared' else r.domain_id
    exists = await db.query(
        query=f'SELECT domain_id FROM {tbl} WHERE domain_id=%s AND header=%s',
        values=[own, name],
        onerow=1,
        errors=[],
    )
    if exists:
        await db.query(
            query=f'UPDATE {tbl} SET label=%s, short=%s, descr=%s, css=%s WHERE domain_id=%s AND header=%s',
            values=[r.label, r.short, r.descr, r.css, own, name],
            errors=[],
        )
    else:
        await db.query(
            query=f'INSERT INTO {tbl}(domain_id,header,label,short,descr,css,is_custom) VALUES(%s,%s,%s,%s,%s,%s,1)',
            values=[own, name, r.label, r.short, r.descr, r.css],
            errors=[],
        )
    return {'success': True, 'errors': [], 'name': name}


@router.post('/theme-schemes/{axis}/{name}/delete')
async def scheme_delete(request: Request, axis: str, name: str, domain_id: int = 0):
    if axis not in THEME_TABLES:
        return {'success': False, 'errors': ['неизвестная ось темы']}
    scope = int(domain_id or 0)
    db = request.state.engine.db_write
    tbl = THEME_TABLES[axis]
    row = await db.query(
        query=f'SELECT header, label, is_custom FROM {tbl} WHERE domain_id=%s AND header=%s',
        values=[scope, name],
        onerow=1,
        errors=[],
    )
    if not row:
        return {'success': False, 'errors': ['схема не найдена']}
    if int(row.get('is_custom') or 0) != 1:
        return {'success': False, 'errors': ['системную схему удалить нельзя']}
    # Нельзя удалять схему, выбранную у домена (общая схема — у любого домена).
    if scope > 0:
        used = await db.query(
            query=f'SELECT count(*) FROM domain_constructor WHERE domain_id=%s AND {axis}=%s',
            values=[scope, name],
            onevalue=1,
            errors=[],
        ) or 0
    else:
        used = await db.query(
            query=f'SELECT count(*) FROM domain_constructor WHERE {axis}=%s',
            values=[name],
            onevalue=1,
            errors=[],
        ) or 0
    if used:
        return {'success': False, 'errors': ['схема используется в %s домене(ах), удаление запрещено' % used]}
    await db.query(
        query=f'DELETE FROM {tbl} WHERE domain_id=%s AND header=%s',
        values=[scope, name],
        errors=[],
    )
    return {'success': True, 'errors': [], 'deleted': True}
