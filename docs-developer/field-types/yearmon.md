# `yearmon` — год и месяц

Составное поле: год + месяц (`YYYY-MM`). На фронте — два select-а и ссылки
«установить текущие значения» / «очистить» (`src/components/fields/yearmon.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `read_only` | только чтение |
| `filter_on` | фильтр в списке |
| `add_description`, `before_html`, `after_html` | оформление |

## Пример

```python
{'description': 'Период', 'type': 'yearmon', 'name': 'period'}
```

## Особенности

- Удобно для отчётов/тарифов «за месяц».
- В фильтрах доступен как `yearmon` (см. [10-lists-filters.md](../10-lists-filters.md)).
