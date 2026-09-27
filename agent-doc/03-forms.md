# Конфиги инструментов и `Form`

> Как писать сами конфиги (структура `form`, типы полей, события, добавление
> инструмента) — см. `12-configs.md`. Здесь — механика загрузки и `Form`.

## `read_config` — входная точка

`lib/all_configs.py:148`. Асинхронная. Вызывается из роутов:

```python
form = await read_config(
  request=request, R=R, config=R['config'], script='find_objects'
)
```

Порядок загрузки (`lib/all_configs.py`):

1. Если у проекта есть `project_id` (`request.state.project`) — сначала пробует
   локальный конфиг из `./conf_projects/project_<project_id>`.
2. Иначе (или если не найден) — из `config_folder` конфига деплоя
   (`configs/<проект>`), по умолчанию `'conf'`.
3. `load_form_from_dir` делает `importlib.import_module(f"{module_dir}.{config}")`
   и читает переменную `form` (схему экрана).
4. Догружает `events.py` (в `form_data['events']`) и `events_for_fields.py`
   (события по полям).
5. Создаёт `Form(arg)`, вызывает `load_data(form_data)`.
6. `after_read_form_config(form)` из конфига деплоя.
7. `form.script`, `form.config`, `form.db` (read или write), `form.manager`.

**Всегда `await`.** Забытый `await` возвращает coroutine вместо `Form` —
известные места перечислены в `10-known-issues.md`.

### Возврат `error` вместо `Form`

При ошибке импорта/отсутствии конфига `read_config` возвращает объект `error`
(`lib/all_configs.py:69-72`), у которого есть только `errors` и `success`.
Вызывающий код всё равно обращается к `form.errors` — работает, но тип другой.
Всегда проверяйте, что вернулось.

## Схема `form`

`configs/<проект>/<инструмент>/__init__.py` экспортирует `form = {...}`.
Значения по умолчанию — в `lib/CRM/form/__init__.py:22`.
Ключевые атрибуты: `work_table`, `work_table_id`, `fields`, `script`, `action`,
`title`, `search_links`, `max_level`, `tree_use`, `sort_field`, `not_create`,
`make_delete`, `card_format` и т.п.

Методы: `form.success()`, `form.run_event(...)`, `form.get_values()`,
`form.get_fields_values()`, `form.load_data(data)`, `form.db.*`.

`form.success()` (`lib/CRM/form/__init__.py:179`) возвращает `True`, если
`len(form.errors) == 0`.

## События

- `events.py` — экспортирует `events = {...}`: `before_insert`,
  `after_save`, `before_delete`, `after_delete`, `before_code`, `permissions` и др.
- `events_for_fields.py` — `events = { '<field_name>': { 'before_save': fn, ... } }`.
  Событие подхватывается, только если имя поля есть в `events`.
- Поддерживаемые имена событий перечислены в `lib/all_configs.py:121-134`.
- `lib/CRM/form/run_event.py` всегда делает `await event(form)`. **Sync-функция
  даст `TypeError` → 500**: одиночное событие ловится только по `AttributeError`,
  список событий — по общему `Exception`. Все хуки пишите `async def`.

Событие может быть одиночной функцией или списком функций.

## `load_form_from_dir`

`lib/all_configs.py:76`. Возвращает `[form, errors]`. Учитывает наличие
`events.py` и `events_for_fields.py` в папке инструмента.
