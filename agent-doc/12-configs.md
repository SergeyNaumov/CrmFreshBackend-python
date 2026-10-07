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
| `resize` | для `file`: `[{'file':'<%filename_without_ext%>_miniN.<%ext%>','size':'WxH','quality':..}]`; бэкенд добавляет каждому `loaded` (URL миниатюры) |
| `preview` | размер из `resize` (напр. `'400x300'`), который показывать миниатюрой; фронт сам берёт `resize[].loaded` |
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

### Файловые поля и превью

- `file` с `resize` задаёт варианты миниатюр (для сеток/карточек сайта).
  Бэкенд в `edit_form_process_fields` кладёт URL каждого варианта в
  `r['loaded']`; в 1_to_m дополнительно считается `preview_img`
  (`lib/get_1_to_m_data.py`).
- `preview` (у `file` **и** у файлового поля внутри `1_to_m`) — строка-размер
  из `resize`. Фронт показывает одну миниатюру сразу: берёт вариант с
  `size == preview` (`resize[].loaded`), иначе первый `resize`, иначе базовый
  файл. Поля без `resize` показывают базовый файл.
- `crops` (bool) — включает ручную обрезку: фронт строит по одному
  `Cropper`-кропу на каждый `resize` и требует подтвердить все до сохранения
  (`file.vue`). Бэкенд использует присланные кропы как миниатюры
  (`upload_file.py`). Без `crops` картинка просто ресайзится из оригинала
  (центрирование), без подтверждения.
- `video` (ds_video): отдельной колонки `rutube_id` нет — id ролика парсится из
  поля `url` в движке сайта (`sites/lib/dsengine/page.py::_rutube_id_from_url`),
  шаблон строит эмбед/постер из `v.id`.

## Конструкторные проекты (5830/5837 и др.)

Общие (не проектные) конфиги конструктора — `ds_*` — живут в
`configs/svcmsmanager/`; в репозитории это **симлинки**, а канон-файлы физически
лежат в `/var/www/svcms-async/manager/backend/conf/ds_*/` — именно их читает
движок сайта. Дублировать `ds_*` в `conf_projects/project_<id>/` **нельзя**:
project-папка в `read_config` имеет приоритет и затенит общий конфиг.

Эталонный конфиг конструкторного проекта (см. `conf_projects/project_5830/`,
а также каноны `conf/ds_*/` в движке сайта):

- `work_table` — **чистое имя таблицы** (не подзапрос). Привязка к проекту —
  через `events.py` → async `permissions`.
- `work_table_id` — **один столбец** (`id`/`content_id`). Для
  `ds_params_good` — суррогатный `id` (миграция 2026-10: PK=id + UNIQUE(param_id, good_id)).
- `events.py` (шаблон):

```python
async def permissions(form):
    project_id = form.project['project_id']
    if not project_id:
        form.errors.append('Доступ запрещён!')
        return
    form.foreign_key = 'project_id'
    form.foreign_key_value = project_id
```

`foreign_key`/`foreign_key_value` дают: автоматический `WHERE wt.project_id=...`
в списках/поиске (`get_search_where`) и `SET project_id=...` при save.

- **Вычисляемые поля** (`date`, `url` у новостей/статей): атрибут
  `'sql': "..."` с алиасом `wt.` (например `concat('/news/', wt.id)` и
  `CONCAT(DAY(wt.registered), ...)`). `sql`-поля автоматически пропускаются
  при сохранении (`save_form`) и не строят фильтры.
- **`name` = реальная колонка таблицы.** Не «человеческое» имя с `db_name`:
  шаблоны сайта, белый список `block_query` и детальные страницы движка читают
  именно колонки (`header`, `body`, `name`, `rate`, `position`, `description`).
  Переименовал колонку — правь и `name`, и шаблоны
  `sites/templates/2026/ds-constructor/block/*.html`. (`db_name` движок
  поддерживает — им пользуются другие конфиги, напр. `configs/svcmsadmin/*`, —
  но в `ds_*` его быть не должно.)
- **`select_from_table`** для справочников: `table`, `header_field`,
  `value_field`, `tablename` (алиас JOIN в `QUERY_SEARCH_TABLES`), `tree_use:1`
  (выбор `parent_id`, порядок по `parent_id`), `where` — скоуп. Плейсхолдер
  `[project_id]` в `where` НЕ подставляется — ставь его в `events.py`
  (`f['where']=f'project_id={project_id}'` по select-полям).
- Чекбоксы-переключатели — `'type':'checkbox'`. Справочник брендов —
  `ds_brands` (`name` конфига обязан совпадать с именем таблицы).
- Левое меню — `left_menu.py` в корне проекта: плоский список
  `{description, value: 'admin-table'|'admin-tree', type:'vue', icon, params:{config}}`.
- **Правило выбора `value`:** короткие сортируемые списки (преимущества,
  команда, слайдер, сертификаты, клиенты, отзывы, видео, галерея) — всегда
  `admin-tree` (тягается мышью, порядок в колонке `sort`). `admin-table` — там,
  где нужен поиск по фильтрам (новости, статьи, товары, бренды, параметры,
  заказы, заявки, документы, статические страницы).
- **`admin-tree` и `header_field`:** поле-заголовок обязано существовать в
  таблице. Ошибка `в таблице ds_X отсутствует поле header` = в конфиге
  `header_field` указывает на несуществующую колонку (или задан под
  «человеческое» имя). Для `ds_reviews` заголовок — `name`, для остальных —
  `header`.
- Названия конфигов соответствуют таблицам: `ds_news`, `ds_article`, `ds_brands`
  и т.д. (в отличие от старых `content`, `top_menu_tree`).

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
