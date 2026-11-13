# Список иконок услуг для icon-picker в админке.
# Парсит svg-спрайт шаблона и добавляет фиксированный набор эмодзи.

import os
import re
from fastapi import APIRouter

router = APIRouter()

# Расположение svg-спрайта конструкторного шаблона.
SITE_TEMPLATE_DIR = os.environ.get(
    "SVCMS_TEMPLATE_DIR",
    "/var/www/svcms-async/sites/templates/2026/ds-constructor",
)
SPRITE_PATH = os.path.join(SITE_TEMPLATE_DIR, "block", "svg_sprite.html")

# Эмодзи-набор (визуально подходят под услуги, без дубликатов спрайта).
EMOJI_ICONS = [
    "🧰", "⚙️", "🏠", "♻️", "💼", "🛠", "🔧", "📦",
    "🎧", "📱", "💻", "🖨", "🔌", "🔑", "🛡", "📡",
    "🚚", "🧹", "🔒", "💡", "🪛", "⚡", "🧲", "📋",
]

# <symbol id="i-..." viewBox="0 0 24 24">...</symbol>
_SYMBOL_RE = re.compile(
    r'<symbol\s+id="(i-[a-z0-9-]+)"\s+viewBox="([^"]*)">(.*?)</symbol>',
    re.S,
)


@router.get("/list")
async def ds_services_icons_list():
    sprites = []
    if os.path.exists(SPRITE_PATH):
        try:
            with open(SPRITE_PATH, encoding="utf-8") as fh:
                src = fh.read()
            for sid, vb, inner in _SYMBOL_RE.findall(src):
                sprites.append({"id": sid, "viewBox": vb, "inner": inner.strip()})
        except Exception:
            pass

    return {
        "success": True,
        "result": {"sprites": sprites, "emoji": EMOJI_ICONS},
    }
