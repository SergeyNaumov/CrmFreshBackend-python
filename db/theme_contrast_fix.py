# Контраст палитр тем: доводит ключевые токены до WCAG AA (4.5:1).
#
#   --primary        — текст-ссылка на светлом/тёмном фоне темы (--light)
#   --link-color     — если задан литеральным цветом
#   --catalog-plate  — заливка плашки каталога под --catalog-plate-text
#   --gradient       — если это не градиент, а литеральный цвет (фон кнопок)
#   --muted          — подписи (уже синхронизировали, здесь идемпотентно)
#
#   export config=config_svcms_manager
#   PYTHONPATH=. .venv/bin/python /tmp/opencode/theme_contrast_fix.py [--apply]

import asyncio
import re
import sys
from datetime import datetime

from config import config
from db.freshdb import FreshDB

TARGET = 4.6
APPLY = '--apply' in sys.argv
HEX_RE = re.compile(r'^#[0-9a-fA-F]{6}$')


def _lum(hex_color):
    h = hex_color.lstrip('#')
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def fit(color, bg, target=TARGET):
    """Затемняет/осветляет цвет, пока контраст с bg не станет >= target."""
    if not HEX_RE.match(color or '') or not HEX_RE.match(bg or ''):
        return color
    r, g, b = (int(color.lstrip('#')[i:i + 2], 16) for i in (0, 2, 4))
    bg_lum = _lum(bg)
    step = -1 if bg_lum > 0.5 else 1
    cur = color
    for _ in range(80):
        if contrast(cur, bg) >= target:
            return cur
        vals = []
        for channel in (r, g, b):
            vals.append(max(0, min(255, channel + step * 4)))
        r, g, b = vals
        cur = '#%02x%02x%02x' % (r, g, b)
        if cur in ('#000000', '#ffffff'):
            return cur
    return cur


def tokens(css):
    """{token: (value, start, end)} для простых `--name: value;` (без вложенных ;)."""
    out = {}
    for match in re.finditer(r'(--[a-z0-9-]+)\s*:\s*([^;{}]+);', css or ''):
        out[match.group(1)] = (match.group(2).strip(), match.start(2), match.end(2))
    return out


def resolve(name, toks, depth=2):
    value = (toks.get(name) or ('',))[0]
    for _ in range(depth):
        m = re.fullmatch(r'var\(\s*(--[a-z0-9-]+)\s*\)', value or '')
        if not m:
            break
        value = (toks.get(m.group(1)) or ('',))[0]
    return value


def replace_token(css, toks, name, value):
    cur, start, end = toks[name]
    return css[:start] + value + css[end:]


def fix_scheme(css):
    toks = tokens(css)
    if not toks:
        return css, []
    light = resolve('--light', toks) or resolve('--body-bg', toks)
    primary = resolve('--primary', toks)
    on_primary = resolve('--on-primary', toks) or '#ffffff'
    changes = []

    # 1) primary как текст на фоне темы + текст на заливке primary.
    if HEX_RE.match(primary) and HEX_RE.match(light):
        new_primary = fit(primary, light, TARGET)
        if contrast(new_primary, on_primary) < 4.5:
            new_primary = fit(new_primary, on_primary, 4.5)
        if new_primary != primary:
            changes.append(('--primary', primary, new_primary))
            css = replace_token(css, toks, '--primary', new_primary)
            toks = tokens(css)
            # rgb-компонент держим в синхроне: на нём построены оверлеи
            # rgba(var(--primary-rgb), …) — иначе контраст плашек не меняется.
            if '--primary-rgb' in toks:
                rgb = ', '.join(str(int(new_primary.lstrip('#')[i:i + 2], 16))
                                for i in (0, 2, 4))
                css = replace_token(css, toks, '--primary-rgb', rgb)
                toks = tokens(css)
            primary = new_primary

    # 2) link-color, если литерал (иначе наследует primary).
    link = resolve('--link-color', toks)
    if HEX_RE.match(link) and HEX_RE.match(light):
        new_link = fit(link, light, TARGET)
        if new_link != link:
            changes.append(('--link-color', link, new_link))
            css = replace_token(css, toks, '--link-color', new_link)
            toks = tokens(css)

    # 3) плашка каталога под своим текстом.
    plate = resolve('--catalog-plate', toks)
    plate_text = resolve('--catalog-plate-text', toks) or on_primary
    if HEX_RE.match(plate) and HEX_RE.match(plate_text):
        new_plate = fit(plate, plate_text, 4.5)
        if new_plate != plate:
            changes.append(('--catalog-plate', plate, new_plate))
            css = replace_token(css, toks, '--catalog-plate', new_plate)
            toks = tokens(css)

    # 4) gradient-литерал (фон кнопок) — контраст с текстом on-primary.
    grad = (toks.get('--gradient') or ('',))[0]
    if HEX_RE.match(grad) and HEX_RE.match(on_primary):
        new_grad = fit(grad, on_primary, 4.5)
        if new_grad != grad:
            changes.append(('--gradient', grad, new_grad))
            css = replace_token(css, toks, '--gradient', new_grad)
            toks = tokens(css)

    # 5) кнопка «В корзину»: текст на --btn-cart.
    btn = resolve('--btn-cart', toks)
    btn_text = resolve('--on-btn-cart', toks) or '#ffffff'
    if HEX_RE.match(btn) and HEX_RE.match(btn_text):
        new_btn = fit(btn, btn_text, 4.5)
        if new_btn != btn:
            changes.append(('--btn-cart', btn, new_btn))
            css = replace_token(css, toks, '--btn-cart', new_btn)
            toks = tokens(css)

    # 5) muted (идемпотентно: обычно уже в норме).
    muted = resolve('--muted', toks)
    if HEX_RE.match(muted) and HEX_RE.match(light):
        new_muted = fit(muted, light, TARGET)
        if new_muted != muted:
            changes.append(('--muted', muted, new_muted))
            css = replace_token(css, toks, '--muted', new_muted)

    return css, changes


async def main():
    db = FreshDB(config['connects']['crm_write'])
    await db.create_pool()
    rows = await db.query(query='SELECT domain_id, header, css FROM domain_theme_color',
                          values=[], errors=[]) or []

    updated = 0
    for row in rows:
        css, changes = fix_scheme(row.get('css') or '')
        if not changes:
            continue
        updated += 1
        label = '%s/%s' % (row['domain_id'], row['header'])
        print(label, ' | '.join('%s %s→%s' % c for c in changes))
        if APPLY:
            await db.query(
                query='UPDATE domain_theme_color SET css=%s, updated=%s '
                      'WHERE domain_id=%s AND header=%s',
                values=[css, datetime.now(), row['domain_id'], row['header']], errors=[])
    print('схем с правками:', updated, '(apply=%s)' % APPLY)
    await db.close_pool()


asyncio.run(main())
