# `checkbox` — флажок

Булево значение `0/1`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description` | подпись (сам `label` флажка) |
| `name` | имя = колонка БД |
| `value` | значение по умолчанию (`1`/`0`) |
| `read_only` | только чтение |
| `hide` | скрыть |
| `add_description` / `before_html` / `after_html` | оформление |
| `error_message` / `warning_message` | сообщения |
| `filter_on` | фильтр в списке |

## Примеры

```python
{'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled'}

{'description': 'TOP', 'type': 'checkbox', 'name': 'top', 'filter_on': 1}

# значение по умолчанию + динамика в before_code
async def default_on(form, field):
    if form.action == 'new':
        field['value'] = 1

{'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled',
 'before_code': default_on}
```

## Особенности

- Рендерится «только контрол» (is_only_field) — без отдельной подписи сверху:
  подпись = `description` у самого флажка.
- В `select_values`/фильтрах значение нормализуется к `0/1`.
- В `save_form` пустое значение превращается в `'0'`.

## См. также

- [`switch`](switch.md) — визуальный переключатель.
