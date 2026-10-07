#!/usr/bin/env python3
"""Пути к каноническому конструктору страниц (компонент админки CRM).

Конструктор переехал из этого репозитория в CrmFreshFront:
    CrmFreshFront/src/components/svcmsAdmin/page_constructor/
Локальный page_constructor/ — замороженный снимок и не используется.

Путь к компоненту можно переопределить переменной окружения
SVCMS_CONSTRUCTOR_DIR.
"""

import os
from pathlib import Path

DEFAULT_CONSTRUCTOR_DIR = (
    Path.home() / "projects" / "CrmFreshFront" / "src" / "components"
    / "svcmsAdmin" / "page_constructor"
)

CONSTRUCTOR_DIR = Path(
    os.environ.get("SVCMS_CONSTRUCTOR_DIR", str(DEFAULT_CONSTRUCTOR_DIR))
).expanduser().resolve()

SCHEMA_JSON = CONSTRUCTOR_DIR / "data" / "schema.json"
SCHEMA_JS = CONSTRUCTOR_DIR / "data" / "schema.js"
RENDER_JS = CONSTRUCTOR_DIR / "engine" / "render.js"
MAP_JS = CONSTRUCTOR_DIR / "engine" / "map.js"
PREVIEW_JS = CONSTRUCTOR_DIR / "engine" / "preview.js"
SEARCH_JS = CONSTRUCTOR_DIR / "engine" / "search.js"
EXPORT_JS = CONSTRUCTOR_DIR / "engine" / "export.js"
DEMO_DIR = CONSTRUCTOR_DIR / "data" / "demo"
TEMPLATE_DIR = CONSTRUCTOR_DIR / "data" / "template"
EDITOR_VUE = CONSTRUCTOR_DIR / "editor" / "BlockEditor.vue"


def require(path: Path) -> Path:
    """Вернуть path или завершить работу с понятной ошибкой."""
    if not path.exists():
        raise SystemExit(
            f"Не найден канонический конструктор: {path}\n"
            f"Ожидался компонент админки: {CONSTRUCTOR_DIR}\n"
            "Задай путь через переменную окружения SVCMS_CONSTRUCTOR_DIR."
        )
    return path
