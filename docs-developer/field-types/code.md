# `code` — HTML, формируемый кодом

Поле выводит произвольный HTML, который формируется функцией `code(form, field)`
(в `events_for_fields.py`). Фронт: `src/components/fields/code.vue`.
Обработка: `lib/CRM/form/edit_form_process_fields.py` (вызов `f['code'](form, f)`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `name` | имя поля |
| `description` | подпись (обычно нужно `full_str`) |
| `full_str` | на всю ширину |
| `after_html`, `before_html` | HTML вокруг |
| `style` | инлайн-стиль |

Функция `code` заполняет `field['html']`.

## Пример

```python
# __init__.py
{'description': 'Товары', 'type': 'code', 'name': 'goods', 'full_str': 1,
 'after_html': '//'}

# events_for_fields.py
def goods_html(form, field):
    # ВНИМАНИЕ: функция синхронная
    rows = []
    for g in form.ov.get('goods', []):
        rows.append(f"<li>{g}</li>")
    field['html'] = '<ul>' + ''.join(rows) + '</ul>'

events = {'goods': {'code': goods_html}}
```

## Особенности

- `code` — **синхронная** функция (в отличие от остальных событий полей):
  вызывается как `f['code'](form, f)` в `edit_form_process_fields.py`.
- Внутри доступны `form.ov` (сырая запись из БД, если её подготовили в
  `permissions`), `form.fields` и т.д.
- Если нужно просто поле ввода — это [`text`/`textarea`](text.md); `code` — только
  вывод.
