# 15. Соглашения, безопасность, чеклист

## Именование и структура

- Папка инструмента = `config` в URL; имя файла конфига ровно `__init__.py`.
- Проектные конфиги — `conf_projects/project_<id>/<config>/`.
- Таблицы: `struct_<project_id>_<tool>` (для проектов) или просто `<tool>`.
- `work_table_id` обычно `id`, `header_field` обычно `header`.
- Не создавайте «универсальные» конфиги на все случаи: лучше отдельный
  инструмент/скрипт.

## `form.s` запрещён

В конфигах нельзя обращаться к глобальному engine `form.s` — при параллельных
запросах это общее мутабельное состояние. Правильно:

| Было | Стало |
|---|---|
| `form.s` | `form.request.state.engine` |
| `form.s.project_id` | `form.request.state.project['project_id']` |
| `form.s.manager` / `form.manager` | `form.request.state.manager` |
| `s.db` | `form.db` или `form.request.state.engine.db` |

## События

- Все события формы/поля — `async def` (кроме полевого `code` — он sync).
- Внутри используйте `await form.db.*`.
- Ошибки — `form.errors.append('текст')`; исключение внутри события тоже
  попадёт в `form.errors` (с traceback).
- Помните: словарь из `events.py` **заменяет** дефолтный набор событий.

## Работа с БД

- Только через `form.db.query(...)` / `form.db.get(...)` / `form.db.save(...)`.
- Значения — параметрами (`values=[...]`), не подстановкой строк (SQL-инъекции).
- Динамические идентификаторы (имена таблиц/колонок) берите из конфига
  (доверенный код), а не из пользовательского ввода.
- `form.db` — read/write в зависимости от скрипта (см. [01](01-overview.md)).
  Не пытайтесь писать из `find_objects` (там read-соединение).

## eval-точки

В конфиге есть места, исполняемые как код/JS на бэке и фронте:

- Бэкенд: полевой `code(form, field)` (sync), `form.javascript` передаётся на фронт.
- Фронт: `javascript.edit_form` (eval), `field.frontend.fields_dependence` (eval),
  `obj.jscode` из ответов зависимостей/ajax (eval), серверные `data.javascript`
  из `elements`-конфигов.

Не кладите в них пользовательские данные. Считайте эти строки кодом
разработчика.

## Ответы и ошибки

```json
{ "success": true,  "data": { }, "errors": [] }
{ "success": false, "errors": ["..."] }
```

- `form.success()` = «нет ошибок».
- Пользователю показывайте понятные тексты, технические детали — в `form.log`
  (`form.pre`) или `explain`.

## Права

- `read_only`, `not_create`, `not_edit`, `make_delete` — грубые ограничения.
- Тонкие — `permissions` (форма и поля), часто на ролях/скоупе проекта.

## Известные грабли

| Место | Проблема |
|---|---|
| `lib/all_configs.py:129` | Полевой `after_update_code` не регистрируется (склейка строк) |
| `lib/CRM/form/__init__.py:175` | `aftert_insert` — опечатка, `after_insert` не дёргает `after_all_change_action` |
| `get_values_for_select_from_table.py` | `autocomplete` без `value` даёт пустой список |
| `save_form.py` | `required`/`unique` не реализованы (legacy) |
| `multiconnect` | мультивыбор в `select_values` — `multilpe` (опечатка в коде) |
| Жизненный цикл | `events.py` заменяет словарь событий целиком |
| Данные | Строки из БД приходят как `str` (в т.ч. числа), учитывайте при сравнениях |

## Чеклист ревью конфига

- [ ] `__init__.py` содержит `form`, у всех полей есть `description`, `type`, `name`.
- [ ] `work_table`/`work_table_id`/`header_field` корректны и существуют.
- [ ] Проектные зависимости (`project_id`) вычисляются в `events.py`, а не хардкодятся.
- [ ] `filedir` ведёт в `./files/...` и создаётся автоматически при загрузке.
- [ ] События — `async def`, зарегистрированы в `events.py`/`events_for_fields.py`.
- [ ] Нет обращений к `form.s`.
- [ ] SQL — только с параметрами.
- [ ] Для select/1_to_m/multiconnect указаны `table`/`foreign_key`/`relation_*`.
- [ ] Фильтры (`filter_on`) и `default_find_filter` заданы, если нужен список.
- [ ] Для дерева — `tree_use`/`max_level`, для галереи — `view_type`/`photo_for_gallery`/`cols`.
- [ ] Проверено на стенде: карточка, список, (дерево/галерея), сохранение, загрузка файла.

## Проверка на стенде

```bash
export config=config_svcms_manager
.venv/bin/uvicorn --reload --port=5000 --workers 1 main:app
# и далее по фронту: /edit_form/<config>, /admin_table/<config>, /admin_tree/<config>
```
