# `time` — время

Время в формате `HH:MM` / `HH:MM:SS`. На фронте — поле с выбором времени и
ссылкой «очистить» (`src/components/fields/time.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `read_only` | только чтение |
| `filter_on` | фильтр в списке |
| `add_description`, `before_html`, `after_html` | оформление |
| `error_message`, `warning_message` | сообщения |

## Примеры

```python
{'description': 'Время', 'type': 'time', 'name': 'f_time', 'filter_on': 1}

{'description': 'Начало', 'type': 'time', 'name': 'start_time'}
```

## Особенности

- Пустое значение сохраняется как `'00:00:00'` (`save_form.py`).
