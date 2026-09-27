# 08. События формы и полей

События — это функции, которые движок вызывает в нужный момент. Все они
**должны быть `async def`** (кроме полевого `code` — см. ниже) и работать через
`form.db`.

- **Уровень формы** — файл `events.py`: `events = {'имя': func | [func, ...]}`.
- **Уровень поля** — файл `events_for_fields.py`: `events = {'<поле>': {'имя': func}}`.
  События переносятся прямо в словарь поля (`field['имя'] = func`).
- `events.py` **полностью заменяет** словарь событий формы, поэтому перечисляйте
  в нём все нужные события.

## Полный список имён

### Формы (`events.py`)

| Событие | Когда |
|---|---|
| `permissions` | до расчёта прав/полей |
| `before_code` | перед `before_code` полей (модификация формы) |
| `before_search_tables` | (find_objects) до сборки таблиц |
| `before_search` | до сборки `WHERE` |
| `before_search_mysql` | перед выполнением SQL поиска |
| `after_search` | после выдачи списка |
| `before_insert` / `before_save` | insert |
| `before_update` / `before_save` | update |
| `after_insert` / `after_save` | после inssert |
| `after_update` / `after_save` | после update |
| `before_delete` / `after_delete` | удаление |
| `after_sort` | после сортировки в дереве |

### Поля (`events_for_fields.py` или `before_code` в поле)

| Событие | Когда / подпись |
|---|---|
| `permissions` | `async def(form, field)` |
| `before_code` | `async def/form(form, field)`, можно вернуть новое поле |
| `before_insert`, `before_update`, `before_save` | `(form, field)` |
| `before_insert_code`, `before_save_code`, `before_delete_code` | `(form, field)` |
| `after_add` | (memo) `(form, field, data)` |
| `after_insert`, `after_update`, `after_save` | `(form, field)` |
| `after_save_code`, `after_delete_code` | `(form, field)` |
| `code` | **sync** `(form, field)` — заполняет `field['html']` |
| `slide_code` | `async def(form, field, data)` — значение в слайде `1_to_m` |
| `filter_code` | `async def(form, field, row)` — вывод значения в списке |

> ⚠ **Баг/особенность:** в `lib/all_configs.py:129` имена
> `'after_insert_code''after_update_code'` склеены в одно — поэтому полевой
> `after_update_code` **не регистрируется**. Не полагайтесь на него.

> ⚠ **Опечатка:** в списке триггеров `after_all_change_action`
> (`lib/CRM/form/__init__.py:175`) есть `'aftert_insert'` — то есть после
> `after_insert` общий хук `after_all_change_action` не вызовется.

## Порядок вызова

**Карточка (insert/update):**

1. `read_config`: `permissions` (форма) → `permissions` (поля) →
   `before_code` (форма) → `before_code` (поля).
2. `form_update_or_insert`: `before_insert`/`before_update` → `before_save`
   (форма, затем поля).
3. `form.save()` → `update_1_to_1`, `multiconnect`/`in_ext_url` → БД →
   `after_insert`/`after_update` → `after_save` (форма, затем поля).

**Список (find_objects):** `before_search_tables` → `before_search` →
`before_search_mysql` → SQL → `after_search` (плюс `filter_code` по полям).

**Дерево:** сортировка → `after_sort`.

**Константы:** `after_save_const`.

**1_to_m:** при выводе каждого дочернего поля — `slide_code`.

## Контекст и ошибки

- Внутри события доступны `form`, `field`, `form.db`, `form.request`,
  `form.R`, `form.params`.
- Ошибку добавляйте в `form.errors.append(...)` — это прервёт обработку
  (`run_event` проверяет `form.success()` в начале).
- Исключение внутри события ловится и добавляется в `form.errors`
  (с traceback), поэтому «тихих» падений нет.

## Примеры

`events.py`:

```python
from .ajax import ajax
from lib.CRM.plugins.InExtUrl import InExtUrl

async def permissions(form):
    project_id = form.request.state.project['project_id']
    await InExtUrl(form, {
        'foreign_key': 'project_id', 'foreign_key_value': project_id,
        'dependence_field': 'header', 'in_url': '/news/<%id%>',
        'url_prefix': '/news/', 'ajax': 'in_ext_url', 'tab': 'promo',
    })
    form.work_table = f'struct_{project_id}_news'
    form.ajax = ajax

events = {'permissions': permissions}
```

`events_for_fields.py`:

```python
async def normalize_phone(form, field):
    # модификация поля перед рендером
    field['placeholder'] = '+7 (___) ___-__-__'

async def goods_html(form, field):
    field['html'] = '...HTML...'

events = {
    'phone': {'before_code': normalize_phone},
    'goods': {'code': goods_html},
}
```
