# Как составляются конфиги

Инструмент CRM = папка с `__init__.py`, где экспортируется словарь `form`.
Эталон для svcms_manager — **`conf_projects/project_5830/<инструмент>/`**.

## Где лежит и как выбирается

`read_config` (`lib/all_configs.py`) ищет инструмент в таком порядке:

1. `./conf_projects/project_<project_id>/<config>` (project_id из
   `request.state.project`) — приоритет.
2. `config_folder` деплоя (`configs/svcmsmanager`) — fallback.
3. По умолчанию `config_folder='conf'`.

Внутри папки:

| Файл | Роль |
|---|---|
| `__init__.py` | обязательно: `form = {...}` |
| `events.py` | необязательно: `events = {...}` — form-level хуки |
| `events_for_fields.py` | необязательно: `events = {'поле': {...}}` — хуки полей |
| `ajax.py` | необязательно: `ajax = {...}` — контроллеры `/ajax/<config>/<имя>` |
| `.html` | опционально, шаблоны для `form.template()` |

Загрузка — `lib/all_configs.py:load_form_from_dir` через
`importlib.import_module`. Каждый инструмент доступен по имени `config` в URL:
`/edit-form/<config>`, `/get-result`, `/admin-tree/<config>`,
`/get-filters/<config>`, `/ajax/<config>/<name>` и т.д.

## Структура `form = {...}`

Минимально:

```python
form = {
  'title': 'Товары',
  'work_table': 'struct_5830_good',   # если не задать -- возьмётся имя инструмента
  'work_table_id': 'id',
  'header_field': 'header',
  'fields': [
    {'description': 'Заголовок', 'type': 'text', 'name': 'header'},
  ],
}
```

Частые ключи формы:

| Ключ | Смысл |
|---|---|
| `title` | заголовок экрана |
| `work_table`, `work_table_id` | таблица и PK (по умолчанию `id`) |
| `fields` | список полей (см. ниже) |
| `header_field` | поле-заголовок (по умолчанию `header`) |
| `sort`, `sort_field` | сортировка списка |
| `tree_use`, `tree_select_header_query`, `max_level` | дерево (`parent_id`) |
| `search_on_load` | запускать поиск при открытии списка |
| `default_find_filter` | фильтр по умолчанию |
| `cols`, `tabs` | раскладка карточки по колонкам/вкладкам |
| `perpage`, `not_perpage` | пагинация |
| `read_only`, `not_create`, `make_delete`, `not_edit` | права на операции |
| `foreign_key`, `foreign_key_value` | связь/скоуп записей |
| `work_table_foreign_key`, `work_table_foreign_key_value` | доп. проверка родителя |
| `card_format` | формат карточки (`vue`) |
| `QUERY_SEARCH_TABLES` | JOIN-ы для списка (см. `04-db.md`) |
| `explain` | выводить SQL поиска (отладка) |

## Поля

Обязательны `name`, `type`, `description`. Тип без `type` — ошибка загрузки
(`set_orig_types`).

Частые атрибуты:

| Атрибут | Смысл |
|---|---|
| `value` | значение по умолчанию для `new` |
| `values` | список `{'v':..,'d':..}` для select/checkbox |
| `filter_on` | показывать поле в фильтрах списка |
| `filter_code` | `async def(form,field,row)` — как выводить значение в списке |
| `before_code` | `async def(form,field)` — модификация поля перед отрисовкой |
| `after_html` | HTML после поля (строка) |
| `read_only`, `hide`, `wide`, `full_str`, `tab` | отображение |
| `required` | обязательность при сохранении |
| `unique` | проверка уникальности |
| `regexp_rules`, `replace_rules` | валидация/нормализация (`lib/check_field.py`) |
| `db_name` | имя колонки, если отличается от `name` |
| `table`, `tablename`, `header_field`, `value_field`, `where`, `order` | для select/связей |
| `filedir` | папка файла для `file`/`wysiwyg` |
| `1_to_m`-поля | `table`, `table_id`, `foreign_key`, `sort`, `view_type`, `fields` |

### Основные типы

| `type` | Назначение |
|---|---|
| `text`, `textarea`, `wysiwyg` | текст; `wysiwyg` — редактор с файлами |
| `checkbox`, `select_values`, `select` | булево/выбор из `values` |
| `select_from_table`, `filter_extend_select_from_table` | выбор из таблицы (в форме `type` подменяется на `select`, а исходный — в `orig_type`) |
| `filter_extend_select_values`, `filter_extend_text` | расширенные фильтры списка |
| `date`, `datetime`, `time`, `daymon` | дата/время |
| `password` | при выводе значение скрывается |
| `file` | загрузка файла в `filedir` |
| `1_to_m` | дочерние записи («слайды»), данные — `lib/get_1_to_m_data.py` |
| `multiconnect` | many-to-many через таблицу связи |
| `1_to_1_text/_select_values/_checkbox/_wysiwyg` | поле из отдельной таблицы (`save_table`, `foreign_key`) |
| `header`, `code` | декоративные / формируемые кодом |
| `memo` | заметки-комментарии (`routes/memo.py`) |

## События

- **Form-level** — `events.py` → `events = {'имя': func | [func, ...]}`.
- **Field-level** — `events_for_fields.py` → `events = {'<field>': {'имя': func}}`.

Поддерживаемые имена (field-level, `lib/all_configs.py`): `permissions`,
`before_code`, `before_insert`, `before_update`, `before_save`,
`before_insert_code`, `before_update_code`, `before_save_code`,
`before_delete_code`, `after_add`, `after_insert`, `after_update`, `after_save`,
`after_insert_code`, `after_update_code`, `after_save_code`, `after_delete_code`,
`code`, `slide_code`, `filter_code`.

Порядок для карточки:

1. `read_config` → `permissions` (форма, затем поля), `before_code`.
2. `insert/update`: `before_insert`/`before_update` → `before_save` → запись в БД
   (`save_form` → `after_insert`/`after_update` → `after_save`).
3. `delete`: `before_delete` → SQL → `after_delete` (+ `after_delete` по полям).
4. Список (`get-result`): `before_search_tables` → `before_search` →
   `before_search_mysql` → SQL → `after_search`.

**Все хуки — `async def`.** `run_event` вызывает их через `await`; sync-функция
даст `TypeError`/500. Внутри — только `await form.db.*`.

## `form.s` не использовать

В конфигах запрещено `form.s` (глобальный Engine). Правильные обращения:

| Было | Стало |
|---|---|
| `form.s` | `form.request.state.engine` |
| `form.s.project_id` | `form.request.state.project['project_id']` |
| `form.s.manager` | `form.request.state.manager` |
| `form.manager` | `form.request.state.manager` |
| `s.db` | `form.db` или `form.request.state.engine.db` |

`form.db` выставляется `read_config` автоматически (read или write).

## Добавление нового инструмента

1. Определись с проектом: `conf_projects/project_5830/<инструмент>/` (для
   svcms_manager) или `configs/svcmsmanager/<инструмент>/` (общий).
2. Создай `__init__.py` с `form = {...}` (скопируй соседний похожий —
   `good`, `catalog`, `news`, `text_page`).
3. При необходимости добавь `events.py`, `events_for_fields.py`, `ajax.py`.
4. Вызови со фронта по имени папки (`config`): `/get-result`,
   `/edit-form/<config>`, `/get-filters/<config>` и т.д.
5. Проверь: `export config=config_svcms_manager && .venv/bin/uvicorn --reload
   --port=5000 --workers 1 main:app`, затем `curl`. Тестов нет.
