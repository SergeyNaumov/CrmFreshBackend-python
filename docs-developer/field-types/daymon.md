# `daymon` — день и месяц

Составное поле: день + месяц (без года). На фронте — autocomplete дня и select
месяца (`src/components/fields/daymon.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `read_only` | только чтение |
| `filter_on` | фильтр в списке |
| `add_description`, `before_html`, `after_html` | оформление |

## Пример

```python
{'description': 'День и месяц', 'type': 'daymon', 'name': 'daymon',
 'make_change_in_search': True}
```

## Особенности

- Используется для событий/праздников, привязанных к дате без года.
- Значение хранится в одном поле; для фильтра по датам обычно не подходит.
