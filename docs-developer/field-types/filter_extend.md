# `filter_extend_*` — расширенные фильтры (admin_table)

Это не поля карточки, а **поля-фильтры** списка. В `edit_form` они вырезаются
(`routes/edit_form/process_edit_form.py`), в `admin_table` конвертируются в
подходящие типы (`routes/get_filters_routes.py`).

## Типы

| Тип | Смысл |
|---|---|
| `filter_extend_text` | текстовый фильтр по колонке/выражению (`db_name`) |
| `filter_extend_select_values` | select-фильтр по `values` |
| `filter_extend_select_from_table` | select-фильтр из таблицы |
| `filter_extend_date` | диапазон дат |
| `filter_extend_datetime` | диапазон дата+время |
| `filter_extend_checkbox` | булев фильтр |
| `filter_extend_switch` | булев фильтр (switch) |

## Примеры

```python
# текстовый фильтр по связанной колонке
{
  'description': 'Email', 'type': 'filter_extend_text',
  'name': 'email', 'tablename': 'me', 'db_name': 'group_concat(me.email SEPARATOR ", ")',
}

# фильтр-выборка из таблицы
{
  'description': 'Менеджер', 'type': 'filter_extend_select_from_table',
  'name': 'manager_id', 'table': 'manager',
  'header_field': 'name', 'value_field': 'id', 'tablename': 'm',
  'filter_on': 1,
}
```

## Особенности

- Для `filter_extend_select_from_table` без `db_name` берётся `value_field`.
- `db_name` здесь — полноценное SQL-выражение (алиасы из `QUERY_SEARCH_TABLES`).
- Порядок фильтров задаётся `filter_on` (по возрастанию).
- В `get_filters` из копии поля вырезаются служебные ключи (`regexp_rules`,
  `tab`, `where`, `table_id`, …).

## См. также

- [10-lists-filters.md](../10-lists-filters.md) — как устроен список и JOIN-ы.
