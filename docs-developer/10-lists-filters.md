# 10. Списки и фильтры (admin_table / find_objects)

Табличный экран обслуживают `routes/get_filters_routes.py` (фильтры) и
`routes/get_result_routes.py` (выдача). Поля формы одновременно служат
колонками/фильтрами.

## Ключи формы для списка

| Ключ | Смысл |
|---|---|
| `default_find_filter` | Поля фильтра по умолчанию (строка `'header'` или список; можно `header,anons`) |
| `search_on_load` | `1` — искать сразу при открытии |
| `perpage` | Записей на страницу (по умолчанию `20`) |
| `not_perpage` | `1` — без пагинации |
| `not_order` | Запретить сортировку по клику на заголовок |
| `QUERY_SEARCH_TABLES` | JOIN-ы (см. ниже) |
| `GROUP_BY` | `GROUP BY` |
| `add_where` | Доп. условия (`str` или `list`) |
| `priority_sort` | Значение по умолчанию `[поле, 'asc'|'desc']` |
| `search_links` | Доп. ссылки над фильтрами |
| `on_filters` | Предустановленные значения фильтров |
| `filters_groups` | Группы фильтров |
| `before_filters_html` | HTML перед фильтрами |
| `search_plugin` | Плагин выдачи |
| `search_multi_action` | Массовые действия (см. ниже) |
| `explain` | Печатать SQL поиска |

## Атрибуты поля для списка

| Атрибут | Смысл |
|---|---|
| `filter_on` | Показывать в фильтрах (влияет на порядок) |
| `not_filter` | Не показывать в фильтрах |
| `allready_out_on_result` | Поле уже выводится в результате (`query`) |
| `filter_code` | `async def(form, field, row)` — как отобразить значение в списке |
| `make_change_in_search` | Редактировать поле прямо в результатах |
| `tablename` | Алиас таблицы (для сортировки/фильтра) |
| `db_name` | Колонка/выражение для вывода и фильтра |
| `filter_type` | `'range'` — диапазон (для дат), `'eq'` — точное совпадение |
| `not_order` | Запретить сортировку по этому полю |

## Типы фильтров

`get_filters_routes.py` конвертирует типы полей в типы фильтров:

| Тип поля | Фильтр |
|---|---|
| `text`, `textarea`, `filter_extend_text` | текст (LIKE) |
| `select_values`, `filter_extend_select_values` | select |
| `select_from_table`, `filter_extend_select_from_table` | select из таблицы |
| `date`, `time`, `datetime`, `daymon`, `yearmon` | с `range` по умолчанию |
| `checkbox`, `switch`, `filter_extend_checkbox` | да/нет |
| `file` | `1` — есть файл, `2` — нет |
| `multiconnect` | выбор связанных сущностей |
| `memo` | фильтр по комментариям |

Из фильтров удаляются поля типов `password`, `code`, `1_to_m`, `hidden`.
Из копии поля для фильтра вырезаются служебные атрибуты
(`tablename`, `db_name`, `regexp_rules`, `tab`, `where`, `table_id`, …) — не
удивляйтесь, что фильтр не видит их.

## `QUERY_SEARCH_TABLES` (JOIN-ы)

```python
'QUERY_SEARCH_TABLES': [
    {'t': 'struct_5830_good', 'alias': 'wt'},
    {'t': 'struct_5830_catalog', 'alias': 'c', 'link': 'wt.catalog_id=c.id', 'lj': 1},
    {'t': 'struct_5830_vendor',  'alias': 'v', 'link': 'wt.vendor_id=v.id',  'lj': 1,
     'for_fields': ['vendor_id']},
]
```

| Ключ | Смысл |
|---|---|
| `t` / `table` | имя таблицы |
| `alias` / `a` | алиас |
| `link` / `l` | условие `ON` (без него — таблица подключается без JOIN) |
| `lj` / `left_join` | `LEFT JOIN` |
| `for_fields` | подключать таблицу только если эти поля участвуют в фильтре (оптимизация) |
| `select_fields` | брать в SELECT только эти колонки |
| `not_add_in_select_fields` | не добавлять колонки таблицы в SELECT |

Алиас таблицы поля (`tablename`) должен совпадать с `alias` здесь — иначе
сортировка/фильтр не найдут колонку.

## Сортировка

- По умолчанию сортировка по колонке поля (`table.db_name`) либо по выражению.
- Клик по заголовку меняет направление (`make_sort`).
- Дерево/`select_from_table` сортируются по `header_field`.
- `datetime`/`date` по умолчанию `desc`.

## `search_multi_action` — массовые действия

Список действий над выбранными записями (`routes/multiaction_routes.py`).
Поддерживаемые `type`: `set_all_value_field`, `change_price`, `delete`.

```python
# search_multi_action.py
search_multi_action_list = [
    {'description': 'перенести всё в рубрику', 'type': 'set_all_value_field',
     'name': 'category_id', 'step': 1},
    {'description': 'изменить цену', 'type': 'change_price',
     'name': 'price', 'step': 1},
]
# __init__.py: 'search_multi_action': search_multi_action_list
```

## События поиска

`before_search_tables` → `before_search` → `before_search_mysql` → SQL →
`after_search` (см. [08-events.md](08-events.md)). В `before_search_mysql`
доступны текущие `tables`/`where`.

## Хитрости

- `filter_code` позволяет вывести в списке значение, которого нет в таблице
  (например, собранное из join-ов или отформатированное).
- `make_change_in_search` + `parent`-колбэк делают поле редактируемым прямо в
  результатах (см. `AdminTable/FindResults.vue`).
- `explain: 1` печатает итоговый SQL в лог — быстрый способ отладки сложных
  `QUERY_SEARCH_TABLES`.
- `default_find_filter` можно указать строкой с запятыми — разберётся в список.
