# `font-awesome` — выбор иконки

Поле выбора иконки (FontAwesome). Фронт: `src/components/fields/font-awesome.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `add_description`, `before_html`, `after_html` | оформление |
| `error_message`, `warning_message` | сообщения |

## Пример

```python
{'description': 'Иконка', 'type': 'font-awesome', 'name': 'icon', 'tab': 'advanced'}
```

## Особенности

- Значение — имя иконки (напр. `fa fa-home`).
- Используется в меню/каталоге (см. `configs/beyeezy/top_menu/fields.py`).
- Версии шрифтов фиксированы проектом — не меняйте подключение иконок.
