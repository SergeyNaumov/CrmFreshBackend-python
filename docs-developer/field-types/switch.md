# `switch` — переключатель

То же, что [`checkbox`](checkbox.md), но в виде переключателя.

## Атрибуты

Идентичны `checkbox`:

| Атрибут | Смысл |
|---|---|
| `description` | подпись |
| `name` | имя = колонка БД |
| `value` | `1`/`0` |
| `read_only`, `hide` | состояние |
| `add_description`, `before_html`, `after_html` | оформление |
| `error_message`, `warning_message` | сообщения |
| `filter_on` | фильтр в списке |

## Пример

```python
{'description': 'Показывать на сайте', 'type': 'switch', 'name': 'show'}
```

## Особенности

- Значение `0/1`; рендерится без отдельной подписи сверху.
- В `1_to_1`-варианте — `1_to_1_switch` (см. [1_to_1.md](1_to_1.md)).
