# `text` — однострочный текст

Базовое строковое поле. На фронте — `v-text-field` (`src/components/fields/text.vue`,
тип обрабатывается вместе с `textarea`).

## Атрибуты

| Атрибут | Тип | Смысл |
|---|---|---|
| `description` | str | подпись (обязательно) |
| `name` | str | имя = колонка БД (обязательно) |
| `value` | str | значение по умолчанию для `new` |
| `placeholder` | str | плейсхолдер |
| `subtype` | str | `color`, `percent`, `qr_call`, `email`, `kladr`, `dadata_address` |
| `values` | list | быстрые варианты-ссылки `[{'v','d'}]` |
| `prefix_list`, `prefix_list_header` | list/str | выбор «города» для адресных полей |
| `show_only_subtype` | bool | показывать только подтип |
| `hide_field` | bool | не рисовать контрол (поле обрабатывается) |
| `style` | str | инлайн-стиль |
| `read_only` | bool | только чтение |
| `regexp_rules` | list | валидация `[regex, msg, ...]` (см. [07](../07-validation-deps.md)) |
| `replace_rules` | list | нормализация на фронте |
| `add_description` | str | подпись под полем |
| `before_html` / `after_html` | str | HTML вокруг поля |

## Примеры

```python
{'description': 'Название', 'type': 'text', 'name': 'header',
 'placeholder': 'до 200 символов', 'filter_on': 1}

# цвет: палитра вариантов
{'description': 'Цвет', 'type': 'text', 'name': 'color', 'subtype': 'color',
 'values': [{'v': '#000000', 'd': 'чёрный'}, {'v': '#ffffff', 'd': 'белый'}]}

# процент
{'description': 'Скидка', 'type': 'text', 'name': 'discount', 'subtype': 'percent'}

# адрес с подсказками DaData
{'description': 'Адрес', 'type': 'text', 'name': 'address', 'subtype': 'dadata_address'}

# только цифры
{'description': 'Цена', 'type': 'text', 'name': 'price',
 'regexp_rules': ['/^[0-9]*$/', 'Укажите целое число'],
 'replace_rules': ['/[^0-9]+/g', '']}
```

## Особенности

- `subtype: 'color'` — цветовой пикер; `subtype: 'percent'` — процент.
- `subtype: 'kladr'`/`'dadata_address'` — автодополнение (эндпоинты `/extend/KLADR`,
  `/extend/DADATA`).
- `subtype: 'qr_call'` — рендерится компонентом `text_subtypes/qr_call`.
- `values` — это не выпадающий список, а ссылки-подсказки под полем.
- Для «не рисовать, но обработать» используйте `hide_field`.

## Где в коде

- Фронт: `src/components/fields/text.vue`
- Раскладка: `src/components/EditForm/FormBlock.vue`
