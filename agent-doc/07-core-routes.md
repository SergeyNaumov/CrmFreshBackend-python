# Ключевые роуты (детали)

## `edit_form` — карточка

`routes/edit_form_routes.py`:

- `POST /edit-form/{config}` — new/insert (action берётся из `R['action']`).
- `PUT /edit-form/{config}/{id}` — update.
- `POST /edit-form/{config}/{id}` — edit/любое действие из `R['action']`.
- `GET /delete-element/{config}/{id}` — удаление.
- `POST /multiconnect/{config}/{field_name}` — связи.

Вся логика — `routes/edit_form/process_edit_form.py`. Порядок: `read_config`
(script `edit_form`) → если `form.response` задан, вернуть его → `form.check()`
для insert/update → `form_update_or_insert()` (вызывает `before_update`/
`before_insert`/`before_save`, затем `form.save()`) → иначе
`form.edit_form_process_fields()` и отдача полей/вкладок.

Спец-действия: `delete_file` → `form.DeleteFile()`, `upload_file` →
`form.UploadFile()`.

## `get_result` — список/поиск

`routes/get_result_routes.py`, script `find_objects`. Обёрнут в `try/except`
(но в `except` использует `form`, который может быть не определён).

Порядок: `read_config` → события `before_search_tables` / `before_search` /
`before_search_mysql` → `form.get_search_tables` + `form.get_search_where`
(собирают `form.query_search['TABLES'/'WHERE'/'VALUES']`) →
`gen_query_search(form)` (в `routes/get_result/`) → count-запрос →
`form.db.query(query, values)` → `process_result_list(form, R, result_list)` →
событие `after_search` → конверт с `results: form.SEARCH_RESULT`.

Настройки: `form.perpage`, `form.page`, `form.not_perpage`, `form.priority_sort`,
`form.GROUP_BY`, `form.explain`.

## WYSIWYG

`routes/wysiwyg_routes.py`, вложен в `edit_form_routes` (префикс `/wysiwyg`).
Операции над файлами/папками внутри поля, `init_options` (опции редактора,
шаблоны), `load-template`. Логика — `routes/edit_form/wysiwyg_process.py`.
Файлы проекта — в `manager['files_dir']`/`files_dir_web` (см. `09-svcms-manager.md`).

## `one_to_m` — дочерние записи

`routes/one_to_m_routes.py` + `routes/edit_form/one_to_m_routine/`. Слайдовые
связи: данные (`GET`), `insert`/`update`/`update_field`/`sort`, `delete`,
`upload_file`, `delete_file`. Каждое действие — отдельный путь `/1_to_m/...`.

## `admin_tree`

`routes/admin_tree_routes.py` + `routes/admin_tree/`. Дерево разделов:
построение веток, сортировка, добавление/удаление, `move` ветки.

## `docpack` — пакет документов

`routes/docpack_routes/`. `POST /docpack/{config}/{field_name}` — диспетчер
действий (`list`, `create_docpack`, `create_bill`, `create_act`, `create_app`,
`get_bills`, `get_acts`, `link_sr`, `unlink_sr`, `save_summ_bill` и др.),
`GET /docpack/load-*` — отдача файлов (`FileResponse`). Логика в `create_*`,
`load_*`, `list.py`, `link_sr.py`.

## `parser_excel` — импорт Excel/CSV

`routes/parser_excel/`. `POST /parser-excel/{config}`. Конфиг парсера — папка
инструмента, где `get_parser(arg)` (async) возвращает словарь (см.
`conf/ds_good_import/`). `arg` — `{config, project_id, admin_id}` из
`request.state`. Actions:

| action | Файл | Назначение |
|---|---|---|
| `init` | `__init__.py` | отдать конфиг парсера (поля, `refs`, `require_any_of`, ...) |
| `preload` | `preload.py` | base64 → временный файл в `tmp_dir`, вернуть первые строки для сопоставления колонок |
| `load` | `load.py` | разобрать файл и upsert в `work_table` (события `before_loopback`/`after_item`/`after_load`) |
| `check_refs` | `refs.py` | **только чтение**: каких значений справочников нет в проекте |
| `create_refs` | `refs.py` | создать отсутствующие значения справочников по названию |

Разбор файла — `go_parse.py` (`.xls` — xlrd, `.xlsx` — openpyxl; пустые
строки пропускаются). `build_hash_fields(fields)` строит `{индекс колонки:
имя поля}` (индекс `0` — валидная колонка, `-1` = не выбрано).

### Ключи конфига парсера

- `work_table`, `work_table_id`, `foreign_key`, `unique_fields` — как в `load`.
- `const_values` — серверные значения (напр. `project_id`), перекрывают файл.
- `fields` — список `{description, name, type, required}`. `description`
  совпадает с заголовком колонки файла → автосопоставление на фронте
  (`autofill_preload`). `required:0` — колонка необязательна.
- `require_any_of` — группы имён полей, из которых должна быть выбрана **хотя
  бы одна** колонка (иначе `load` вернёт ошибку «не выбрана колонка: ...»).
  Проверка — `load.py::_check_require_any_of` и фронт (`all_fields_selected`).
- `before_loopback(data, db)`, `after_item(data, record_id, db, errors)`,
  `after_load(db, ctx)` — async-хуки (см. ниже).
- `refs` — справочники «id или название» (см. ниже).

### Справочники `refs` — значения по id **или** названию

Конфиг может объявлять `refs` — список справочников, значения которых в файле
приходят либо id, либо названием, строго **в рамках текущего проекта**.
Дескриптор (резолвер — `lib/svcmsmanager/refs.py`, класс `RefResolver`):

```python
{
  'key':'rubric', 'label':'рубрики', 'one':'рубрика',
  'table':'ds_catalog', 'name_col':'header',
  'id_field':'rubricator_id', 'name_field':'rubricator_name',
  'scope':{'project_id':project_id},          # принадлежность проекту
  'allow_zero':0,                              # 0 — допустимое значение (бренд)
  'create':{'path':'','anons':'',...},         # значения для INSERT
  'chpu':{'in_url':'/catalog/<%id%>','prefix':'/catalog/'},  # опц. ЧПУ
}
```

Правило одно (`RefResolver.resolve`), им пользуются и `check_refs`, и
`before_loopback` при `load`: числовой id проверяется на принадлежность
`scope` (прежде всего `project_id`); не прошёл — пробуется название; чужой/
несуществующий id и ненайденное название в БД **не пишутся**, а сообщаются
(`bad_id`/`missing_name`, `foreign:0|1` — есть ли id в БД у другого проекта).
Колонки-названия не являются полями `work_table` — хук их вырезает.

- `check_refs` (read-only) — по маппингу колонок собирает для каждого `ref`:
  `missing` (нет названий в проекте), `bad_ids` (`{id,foreign}`), `unresolved`/
  `no_ref`. Ничего не создаёт — вызывается фронтом **до** записи в БД.
- `create_refs` — `{ref, names:[...]}`: идемпотентно создаёт отсутствующие
  (привязка `scope`), для рубрики дополнительно пишет ЧПУ в `in_ext_url`
  (`lib/CRM/chpu.py::generate_ext_url`/`save_chpu`).
- `build_hash_fields` в `load.py`/`refs.py` общий — проверка и загрузка видят
  одинаковый маппинг.

**Пример (товары):** экспорт — `conf/ds_good/plugins.py` (выгрузка всех товаров
в xlsx, кнопки через `form.search_plugin`); импорт — `conf/ds_good_import/`
(справочники `ds_catalog`/`ds_brands`, `require_any_of` для рубрики, фоновая
обработка фото — `lib/svcmsmanager/ds_good_photos.py`). Детали — `12-configs.md`.

Скачивание сформированных файлов — `GET /download_tmp/{filename}`
(`routes/download_tmp.py`, каталог `files/tmp`).

## `ajax` — универсальный диспетчер

`routes/ajax.py`. `GET/POST /ajax/{config}/{ajax_name}` — вызывает функцию
`ajax_name` из конфига инструмента. `POST` дублирует `GET` (два декоратора).

## `autocomplete`

`routes/autocomplete.py`. `POST /autocomplete/{config}` — подгрузка значений
select-полей по `term` и зависимым фильтрам.

## `mainpage`

`routes/mainpage/__init__.py` — главная: данные менеджера, новости,
уведомления (`/notifications/...`), дни рождения, «загрузка менеджера».
Есть исторические обращения к глобалам — см. `10-known-issues.md`.

## `gptassist`

`routes/gptassist/__init__.py`. `GET /gpt-assist/init`, `POST /send-task`,
`POST /daemon-result`, `WS /ws/{task_id}`. rules — `config['gptassist_rules']`
(для svcms_manager — `configs/svcmsmanager/gptassist_rules.py`).

## `messenger`

`routes/messenger.py`. WebSocket `/messenger/ws/{socket_name}` + REST.
Работает через `config['messenger_rules']`; при `{}` часть эндпоинтов отдаёт
нейтральные ответы.

## Прочие

- `register.py` / `password.py` — регистрация, восстановление и смена пароля.
- `get_filters_routes.py` — фильтры списка.
- `const_routes.py` — экран констант (`/const/get`, `/const/save_value`).
- `multiaction_routes.py` — массовые операции.
- `transfere_cards/` — перенос карточек.
- `table_routes.py`, `page_routes.py`, `documentation_routes.py`,
  `video_routes.py`, `news_routes.py` — простые экраны (у части забыт `await
  read_config`, см. `10-known-issues.md`).
- `extend_routes.py` — `/extend/KLADR`.
