# `accordion` — секции-аккордеон

Набор раскрывающихся секций. Фронт: `src/components/fields/accordion.vue`.
Работает без формы (данные берутся из `field.data`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `name` | имя поля |
| `data` | список секций |

Элемент `data`:
| Ключ | Смысл |
|---|---|
| `id` | id секции |
| `header` | HTML заголовка |
| `header_links` | `[{'header','url','style'}]` — ссылки в заголовке |
| `not_container` | без обёртки `v-container` |
| `content` | список блоков: `{'type': 'html'|'table'|'chart', ...}` |

## Пример

```python
{
  'description': 'Справка',
  'type': 'accordion',
  'name': 'help',
  'data': [
     {
        'id': 1,
        'header': 'Как оформить заказ',
        'header_links': [{'header': 'документация', 'url': '/docs#order'}],
        'content': [
            {'type': 'html', 'body': '<p>Текст...</p>'},
            {'type': 'table', 'table': {'headers': [{'h': 'Шаг'}], 'data': [['1']]}},
        ],
     },
  ],
}
```

## Особенности

- Внутри поддерживаются вложенные [`table`](table.md) и [`chart`](chart.md).
- Удобно для страниц-справок/дашбордов без привязки к записи.
