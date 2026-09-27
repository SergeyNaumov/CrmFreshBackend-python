# `date` — дата

Дата в формате `YYYY-MM-DD`. На фронте — текстовое поле с календарём и ссылкой
«очистить» (`src/components/fields/date.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `empty_value` | `'null'` — сохранять `NULL` вместо `'0000-00-00'` |
| `read_only` | только чтение (рендерится как текст) |
| `hide` | скрыть |
| `filter_type` | `'range'` — фильтр диапазоном в списке |
| `filter_on` | показывать в фильтрах |
| `add_description`, `before_html`, `after_html` | оформление |
| `error_message`, `warning_message` | сообщения |

## Примеры

```python
{'description': 'Дата', 'type': 'date', 'name': 'registered'}

# пустая дата -> NULL
{'description': 'Дата', 'type': 'date', 'name': 'published', 'empty_value': 'null'}

# фильтр диапазоном
{'description': 'Дата', 'type': 'date', 'name': 'registered',
 'filter_on': 1, 'filter_type': 'range'}
```

## Особенности

- В БД по умолчанию пишется `'0000-00-00'` для пустой даты; `empty_value: 'null'`
  меняет это на `NULL`.
- В фильтрах по умолчанию — диапазон.
- В режиме `read_only` выводится как текст (без контрола).
