# `datetime` — дата и время

Дата + время. На фронте — два поля (дата с календарём и время) и ссылки
«очистить» / «текущая дата и время» (`src/components/fields/datetime.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `empty_value` | `'null'` — сохранять `NULL` вместо `'0000-00-00 00:00:00'` |
| `not_clear` | не показывать ссылку «очистить» |
| `read_only` | только чтение |
| `filter_on`, `filter_type` | фильтр (по умолчанию диапазон) |
| `add_description`, `before_html`, `after_html` | оформление |

## Примеры

```python
{'description': 'Создано', 'type': 'datetime', 'name': 'created'}

{'description': 'Опубликовано', 'type': 'datetime', 'name': 'published',
 'empty_value': 'null', 'not_clear': True}
```

## Особенности

- Значение `'0000-00-00 00:00:00'` (и пустое) трактуется как отсутствующее.
- По умолчанию рендерится «полной строкой» и без подписи (как `wysiwyg`/`file`).
