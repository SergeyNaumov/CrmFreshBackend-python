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

# Транслитерация (как в legacy InExtUrl).
_TRANSLIT = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'cz', 'ш': 'sh', 'щ': 'scz', 'ъ': '',
    'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'u', 'я': 'ja',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E',
    'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M',
    'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
    'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'CZ', 'Ш': 'SH', 'Щ': 'SCH', 'Ъ': '',
    'Ы': 'y', 'Ь': '', 'Э': 'E', 'Ю': 'U', 'Я': 'YA',
}


def to_translate(s):
    s = str(s or '')
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
    if await check_exists(form, url, project_id, exclude_in_url):
        n = 1
        while await check_exists(form, url + '-' + str(n), project_id, exclude_in_url):
            n += 1
        url = url + '-' + str(n)
    return url


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
    """Вызывается из save_form: пишет ЧПУ по атрибутам конфига chpu_*."""
    in_url_tpl = getattr(form, 'chpu_in_url', '') or ''
    if not in_url_tpl or not getattr(form, 'id', None):
        return
    prefix = getattr(form, 'chpu_prefix', '') or ''
    dep = getattr(form, 'chpu_dependence_field', 'header') or 'header'
    project_id = getattr(form, 'foreign_key_value', None)

    header = None
    new_values = getattr(form, 'new_values', None)
    if isinstance(new_values, dict):
        header = new_values.get(dep)
    if not header and getattr(form, 'db', None) and getattr(form, 'work_table', ''):
        header = await form.db.query(
            query=f'SELECT {dep} FROM {form.work_table} WHERE {form.work_table_id}=%s',
            values=[form.id], onevalue=1, errors=[],
        )
    if not header:
        return

    in_url = in_url_tpl.replace('<%id%>', str(form.id))
    ext_url = await generate_ext_url(
        form, header, prefix=prefix, project_id=project_id, exclude_in_url=in_url)
    await save_chpu(form, in_url, ext_url, project_id)
