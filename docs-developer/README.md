# Документация для разработчиков конфигов

Это руководство о том, **как писать конфиги (инструменты) на бэкенде**:
структура `form = {...}`, все ключи формы и полей, все типы полей, связи,
файлы, валидация, зависимости, события, ajax, списки/фильтры, дерево и галерея,
а также каталог «хитростей».

Документация ориентирована на людей. Для агентов/краткого обзора проекта есть
отдельная папка `agent-doc/` (в частности `agent-doc/12-configs.md`).

## Где лежат конфиги

Инструмент — это папка с обязательным `__init__.py`, где объявлен словарь `form`.
Поиск инструмента (`lib/all_configs.py:read_config`):

1. `./conf_projects/project_<project_id>/<config>` — приоритет (проектные конфиги).
2. `config_folder` деплоя (`configs/<tenant>`, для svcms_manager обычно `configs/svcmsmanager`).
3. `conf` — по умолчанию.

`project_id` берётся из `request.state.project`. Один и тот же `config` в URL
может резолвиться в разные папки у разных проектов/тенантов.

Эталонные примеры: `conf_projects/project_5830/<инструмент>/`.

## Файлы внутри папки инструмента

| Файл | Обязателен | Назначение |
|---|---|---|
| `__init__.py` | да | `form = {...}` — основной конфиг |
| `events.py` | нет | `events = {...}` — события уровня формы |
| `events_for_fields.py` | нет | `events = {'<поле>': {...}}` — события уровня поля |
| `ajax.py` | нет | `ajax = {...}` — контроллеры `/ajax/<config>/<name>` |
| `*.html` | нет | шаблоны для `form.template(filename, **values)` (Jinja2) |
| `fields.py` | нет | вспомогательный модуль, если конфиг импортирует куски (часто в старых конфигах) |

Инструмент доступен по имени папки (`config`) в URL: `/edit-form/<config>`,
`/get-result`, `/get-filters/<config>`, `/admin-tree/<config>`,
`/ajax/<config>/<name>` и т.д.

## Как читать документацию

| Файл | О чём |
|---|---|
| [01-overview.md](01-overview.md) | модель инструмента, скрипты, жизненный цикл `read_config` |
| [02-form-keys.md](02-form-keys.md) | все ключи `form = {...}` |
| [03-fields-common.md](03-fields-common.md) | обязательные и общие атрибуты поля, layout-флаги |
| [04-field-types.md](04-field-types.md) | каталог всех типов полей (кратко) |
| [field-types/](field-types/README.md) | **по одному документу на каждый тип поля** (атрибуты, примеры, особенности) |
| [05-relations.md](05-relations.md) | select/select_from_table/select_values, 1_to_m, multiconnect, 1_to_1 |
| [06-files-wysiwyg.md](06-files-wysiwyg.md) | file (resize/crops/preview), wysiwyg |
| [07-validation-deps.md](07-validation-deps.md) | regexp_rules, replace_rules, зависимость полей, frontend/ajax |
| [08-events.md](08-events.md) | события формы и полей, порядок вызова |
| [09-ajax.md](09-ajax.md) | ajax.py и `form.ajax` |
| [10-lists-filters.md](10-lists-filters.md) | admin_table: списки, фильтры, поиск |
| [11-tree-gallery.md](11-tree-gallery.md) | admin_tree: дерево и галерея |
| [12-layout-frontend.md](12-layout-frontend.md) | как форма/поле рендерится на фронте |
| [13-tricks.md](13-tricks.md) | каталог приёмов и «хитростей» |
| [14-examples.md](14-examples.md) | готовые рецепты целиком |
| [15-conventions.md](15-conventions.md) | соглашения, безопасность, чеклист ревью |
| [16-field-types-backend.md](16-field-types-backend.md) | обработка типов полей бэкендом (матрица этапов) |
| [17-frontend-contract.md](17-frontend-contract.md) | контракт с фронтендом (AdminTable/AdminTree/EditForm/меню) |
| [18-svcms-admin.md](18-svcms-admin.md) | панель SV-CMS admin (`config_svcms_admin`) |
| [19-known-gaps.md](19-known-gaps.md) | известные расхождения и дефекты |

## HTML-версия

Документация собирается в статические HTML-страницы (MkDocs + Material) в папку
`docs-html/` — их можно открыть в браузере без сервера:

```bash
./build_docs.sh                        # собрать docs-html/
.venv/bin/mkdocs serve                 # предпросмотр с поиском
python -m http.server -d docs-html     # раздать готовую папку
```

## Быстрый старт

```python
# conf_projects/project_5830/my_tool/__init__.py
form = {
    'title': 'Мой инструмент',
    'work_table': 'struct_5830_my_tool',   # если не указать — возьмётся имя папки
    'work_table_id': 'id',
    'header_field': 'header',              # по умолчанию и так 'header'
    'fields': [
        {'description': 'Заголовок', 'type': 'text', 'name': 'header'},
        {'description': 'Включен',  'type': 'checkbox', 'name': 'enabled'},
    ],
}
```

Открыть карточку списка: `/edit_form/my_tool`, таблицу: `/admin_table/my_tool`.

## Соглашения (кратко)

- Поля: обязательны `description`, `type`, `name` (для большинства типов).
- Все события — `async def`.
- В конфигах **нельзя** обращаться к `form.s` (глобальный engine). Только
  `form.request.state.engine`, `form.db`, `form.request.state.manager`.
- `form.db` выставляется автоматически (`read` или `write` в зависимости от скрипта).

Подробности — [15-conventions.md](15-conventions.md).
