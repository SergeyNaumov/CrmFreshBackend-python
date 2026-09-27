# 01. Обзор: инструмент, скрипты, жизненный цикл

## Инструмент (config)

Инструмент — папка с `__init__.py`, в которой объявлен словарь `form`.
Имя папки = `config` в URL. Один инструмент может обслуживать несколько
экранов, потому что поведение зависит от **скрипта** (`script`), который
передаёт роут.

Минимальный конфиг:

```python
form = {
    'title': 'Товары',
    'work_table': 'struct_5830_good',  # иначе подставится имя папки
    'work_table_id': 'id',             # иначе 'id'
    'fields': [
        {'description': 'Название', 'type': 'text', 'name': 'header'},
    ],
}
```

## Скрипты и роуты

| `script` | Роут(ы) | Что делает | Файлы |
|---|---|---|---|
| `edit_form` | `GET/POST /edit-form/{config}[/{id}]` | карточка редактирования/создания | `routes/edit_form/process_edit_form.py` |
| `admin_table` | `GET/POST /get-filters/{config}`, `POST /get-result` | таблица списка + фильтры | `routes/get_filters_routes.py`, `routes/get_result_routes.py` |
| `find_objects` | `POST /get-result` | сам поиск/выдача списка | `routes/get_result_routes.py` |
| `admin_tree` | `GET/POST /admin-tree/{config}` | дерево/галерея | `routes/admin_tree/admin_tree_run.py` |
| `const` | `POST /get`, `POST /save_value` | страница констант (ключ-значение) | `routes/const_routes.py` |
| `ajax` | `GET/POST /ajax/{config}/{name}` | ajax-контроллер | `routes/ajax.py` |
| `multiaction` | `POST /{config}` | массовые действия над списком | `routes/multiaction_routes.py` |
| `documentation` | `GET /{config}` | дерево документации | `routes/documentation_routes.py` |
| `wysiwyg` | — | серверная обработка редактора | `routes/edit_form/wysiwyg_process.py` |
| `table`, `video_list` | — | табличные/видео экраны | — |

Один и тот же `fields` используется во всех скриптах. Отдельные ключи формы
имеют смысл только для конкретного скрипта (например `tree_use` — для
`admin_tree`, `filter_on` — для `admin_table`).

## Жизненный цикл `read_config`

`lib/all_configs.py:read_config` выполняет по шагам:

1. Загружает `form` из папки (project → config_folder → conf) через
   `importlib.import_module`, делает `deepcopy`.
2. Подтягивает `events.py` (если есть) в `form.events`.
3. Создаёт `Form(arg)` и делает `load_data(form_data)` — все ключи словаря
   становятся атрибутами объекта `form`.
4. Подтягивает `events_for_fields.py`: события из словаря переносятся прямо
   в поля (`field[event_name] = func`).
5. Проставляет `form.s`, `form.request`, `form.config`, `form.script`,
   `form.db` (`s.db_read` для `find_objects`/`admin_table`, иначе `s.db_write`).
6. Определяет `form.manager` (login с учётом ролей/прав).
7. `await form.run_event('permissions')` + `field['permissions']` для каждого поля.
8. `form.default_config_attr(arg)` — дефолты (`read_only`, `make_delete`, …).
9. `form.set_orig_types()` — нормализация типов (см. ниже).
10. `await form.get_values()` — значения записи из БД по `form.id`.
11. `await form.run_all_before_code()` — `before_code` формы и полей.
12. `await form.get_fields_values()` — догрузка значений `select_from_table`,
    `1_to_m` (вторым проходом).

Если `form.errors` не пуст после загрузки — роут обычно возвращает `success:0`.

### `set_orig_types` — подмена типов

Для полей с типами `select_from_table`, `select_values`,
`filter_extend_select_from_table`, `filter_extend_select_values` в
**edit_form** оригинальный тип сохраняется в `f['orig_type']`, а `f['type']`
становится `'select'`. На бэке логика (сохранение, поиск) смотрит на
`orig_type`, фронт — на `type`.

## form.db, form.request, form.s

| Что | Как правильно |
|---|---|
| База | `await form.db.query(...)`, `await form.db.get(...)`, `await form.db.save(...)`, `form.db.getrow(...)` |
| Engine | `form.request.state.engine` |
| project_id | `form.request.state.project['project_id']` |
| manager | `form.request.state.manager` (в конфиге обычно `form.manager`) |
| CGI-параметр | `form.param('name')` (читает `form.R['cgi_params']`) |
| Отладка | `form.pre(value)` (пишет в `form.log`), `'explain': True` |
| Ошибка | `form.errors.append('текст')` |

> В конфигах **нельзя** использовать `form.s` — это глобальный мутабельный
> engine, при параллельных запросах это общее состояние. См. [15-conventions.md](15-conventions.md).

## Ответы

Стандартный контракт (см. `agent-doc/06-response-contract.md`):

```json
{ "success": true,  "data": { }, "errors": [] }
{ "success": false, "errors": ["..."] }
```

На практике ответы скриптов содержат свои поля (`fields`, `tree`, `form`,
`results`, `list`, …) и всегда `success` + `errors`.
