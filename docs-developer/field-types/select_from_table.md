# `select_from_table` — выбор из таблицы

Выпадающий список, значения которого берутся из другой таблицы
(`lib/CRM/form/get_values_for_select_from_table.py`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `table` | таблица-источник (обязательно) |
| `header_field` | колонка-подпись (по умолчанию `header`) |
| `value_field` | колонка-значение (по умолчанию `id`) |
| `where` | условие (можно `WHERE ...`) |
| `order` | сортировка (по умолчанию `header_field`, для дерева — `parent_id`) |
| `query` | полностью свой `SELECT` (перекрывает всё выше) |
| `list` | готовый список (без запроса) |
| `tree_use` | построить иерархию по `parent_id` |
| `autocomplete` | запретить произвольный ввод (только выбор) |
| `tablename` | алиас таблицы в `QUERY_SEARCH_TABLES` (для сортировки/фильтра) |
| `db_name` | колонка-значение в текущей таблице, если не `name` |
| `add_description`, `style`, `filter_on` | оформление/фильтр |

> В `edit_form` тип подменяется на `select` (`orig_type` сохраняется).
> Значения догружаются в `get_values`/`get_fields_values`.

## Примеры

```python
{'description': 'Рубрика', 'name': 'catalog_id', 'type': 'select_from_table',
 'table': 'struct_5830_catalog', 'header_field': 'header', 'value_field': 'id',
 'tablename': 'c'}

# дерево рубрик
{'description': 'Рубрика', 'name': 'catalog_id', 'type': 'select_from_table',
 'table': 'struct_5830_catalog', 'tree_use': 1}

# только выбор из списка
{'description': 'Вендор', 'name': 'vendor_id', 'type': 'select_from_table',
 'table': 'struct_5830_vendor', 'autocomplete': 1}

# свой запрос
{'description': 'Менеджер', 'name': 'manager_id', 'type': 'select_from_table',
 'query': 'SELECT id v, name d FROM manager WHERE active=1 ORDER BY name'}
```

## Особенности

- Если `autocomplete: 1` и нет `value`, список будет пустым (значение ожидается
  из зависимости).
- В `edit_form` первым добавляется пункт `{'v':'0','d':'выберите значение'}`.
- Для сортировки в списке задайте `tablename`, совпадающий с алиасом в
  `QUERY_SEARCH_TABLES`.
