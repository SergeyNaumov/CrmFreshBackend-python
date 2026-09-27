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

## `parser_excel`

`routes/parser_excel/`. `POST /parser-excel/{config}` с action `init` /
`preload` / `load`. Логика — `load_parser_from_config`, `preload`, `load`,
`go_parse`.

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
