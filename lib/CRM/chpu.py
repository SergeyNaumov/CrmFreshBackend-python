"""Универсальный модуль ЧПУ (slug → in_ext_url).

Используется и edit-формой (save_form), и админ-деревом (add_branch_plain).
Конфиг задаёт атрибуты (верхний уровень form-dict):
  'chpu_in_url'          — шаблон внутреннего url, напр. '/catalog/<%id%>'
  'chpu_prefix'          — префикс внешнего url, напр. '/catalog/'
  'chpu_dependence_field'— поле-источник текста (по умолчанию 'header')
ЧПУ пишется в таблицу in_ext_url (project_id, in_url, ext_url), а не в ds_*.
"""

import re

from lib.core import exists_arg

# Транслитерация — ЗЕРКАЛО tools/export_to_mysql.py::TRANSLIT_MAP
# (репозиторий svcms-templates: dump_from_json.py, gen_chpu.py).
# Менять только вместе с ним: иначе slug, сгенерированный админкой при
# сохранении (например, при правке заголовка новости), разойдётся с уже
# проиндексированными ЧПУ из выгрузки и старые адреса начнут 404.
#   й→j, ц→ts, ч→ch, щ→sch, ю→ju, я→ja
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'ju', 'я': 'ja',
}


def to_translate(s):
    # Регистр не важен: slug всегда в нижнем регистре (как в gen_chpu.py).
    s = str(s or '').lower()
    for key, val in _TRANSLIT.items():
        s = s.replace(key, val)
    return s


def make_slug(header, prefix=''):
    s = to_translate(str(header or '').replace('/', '-'))
    s = re.sub(r'[^a-zA-Z0-9\-]+', '-', s)
    s = re.sub(r'-+', '-', s).strip('-').lower()
    if not s:
        return ''
    return (prefix or '') + s


async def check_exists(form, ext_url, project_id=None, exclude_in_url=''):
    where = 'ext_url=%s'
    values = [ext_url]
    if project_id not in (None, '', 0, '0'):
        where += ' AND project_id=%s'
        values.append(project_id)
    if exclude_in_url:
        where += ' AND in_url<>%s'
        values.append(exclude_in_url)
    cnt = await form.db.query(
        query=f'SELECT count(*) FROM in_ext_url WHERE {where}',
        values=values, onevalue=1, errors=[],
    )
    return cnt


async def generate_ext_url(form, header, prefix='', project_id=None, exclude_in_url=''):
    """slug + постфикс -1/-2/-3 при коллизии в рамках проекта."""
    url = make_slug(header, prefix)
    if not url:
        return ''
    return await unique_ext_url(form, url, project_id, exclude_in_url)


async def unique_ext_url(form, url, project_id=None, exclude_in_url=''):
    """Дедуп готового внешнего url: коллизия в проекте → -1/-2/-3."""
    if await check_exists(form, url, project_id, exclude_in_url):
        n = 1
        while await check_exists(form, url + '-' + str(n), project_id, exclude_in_url):
            n += 1
        url = url + '-' + str(n)
    return url


def normalize_ext_url(value, prefix=''):
    """Ручной ввод ЧПУ → канонический вид '/news/moj-slug'.

    Принимает 'slug', 'moj slug', '/news/moj-slug', '/news/мой-заголовок'.
    Каждый сегмент прогоняется через ту же транслитерацию, что и авто-slug.
    """
    text = str(value or '').strip()
    if not text:
        return ''
    if not text.startswith('/'):
        text = (prefix or '/') + text
    segments = [make_slug(seg) for seg in text.strip('/').split('/')]
    segments = [seg for seg in segments if seg]
    return '/' + '/'.join(segments) if segments else ''


async def save_chpu(form, in_url, ext_url, project_id):
    """Upsert ЧПУ в in_ext_url по (project_id, in_url)."""
    if not (in_url and ext_url):
        return
    exists = await form.db.query(
        query='SELECT count(*) FROM in_ext_url WHERE project_id=%s AND in_url=%s',
        values=[project_id, in_url], onevalue=1, errors=[],
    )
    if exists:
        await form.db.query(
            query='UPDATE in_ext_url SET ext_url=%s WHERE project_id=%s AND in_url=%s',
            values=[ext_url, project_id, in_url], errors=form.errors,
        )
    else:
        await form.db.query(
            query='INSERT INTO in_ext_url (project_id, in_url, ext_url) VALUES (%s, %s, %s)',
            values=[project_id, in_url, ext_url], errors=form.errors,
        )


async def save_chpu_for_form(form):
    """Вызывается из save_form: пишет ЧПУ по атрибутам конфига chpu_*.

    Правила:
      * поле `type=in_ext_url` есть и пользователь изменил значение →
        сохраняем введённый url (транслит/санитайз + дедуп);
      * поле очистили → возвращаем авто-slug из `chpu_dependence_field`;
      * url ещё нет (новая запись) → генерируем из `chpu_dependence_field`;
      * url уже есть и не менялся → НЕ трогаем: переименование заголовка не
        должно молча ломать проиндексированный адрес (меняется только руками
        или очисткой поля).
    """
    in_url_tpl = getattr(form, 'chpu_in_url', '') or ''
    if not in_url_tpl or not getattr(form, 'id', None):
        return
    prefix = getattr(form, 'chpu_prefix', '') or ''
    dep = getattr(form, 'chpu_dependence_field', 'header') or 'header'
    project_id = getattr(form, 'foreign_key_value', None)

    in_url = in_url_tpl.replace('<%id%>', str(form.id))
    new_values = getattr(form, 'new_values', None) or {}
    if not isinstance(new_values, dict):
        new_values = {}

    has_project = project_id not in (None, '', 0, '0')
    stored = await form.db.query(
        query='SELECT ext_url FROM in_ext_url WHERE in_url=%s'
              + (' AND project_id=%s' if has_project else ''),
        values=[in_url] + ([project_id] if has_project else []),
        onevalue=1, errors=[],
    )

    submitted = None
    for f in (getattr(form, 'fields', None) or []):
        if f.get('type') == 'in_ext_url' and f.get('name') in new_values:
            value = new_values.get(f.get('name'))
            submitted = '' if value is None else str(value).strip()
            break

    # Изменили url вручную — сохраняем как ввели.
    if submitted and submitted != (stored or ''):
        ext_url = normalize_ext_url(submitted, prefix)
        if ext_url:
            ext_url = await unique_ext_url(form, ext_url, project_id, in_url)
            await save_chpu(form, in_url, ext_url, project_id)
        return

    # Есть url и его не меняли (в т.ч. просто переименовали заголовок) — не трогаем.
    if stored and submitted is not None and submitted == stored:
        return

    header = new_values.get(dep)
    if not header and getattr(form, 'db', None) and getattr(form, 'work_table', ''):
        header = await form.db.query(
            query=f'SELECT {dep} FROM {form.work_table} WHERE {form.work_table_id}=%s',
            values=[form.id], onevalue=1, errors=[],
        )
    if not header:
        return

    ext_url = await generate_ext_url(
        form, header, prefix=prefix, project_id=project_id, exclude_in_url=in_url)
    await save_chpu(form, in_url, ext_url, project_id)
