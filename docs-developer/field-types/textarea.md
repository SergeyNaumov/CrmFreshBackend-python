# `textarea` — многострочный текст

Многострочное текстовое поле. Обрабатывается тем же компонентом, что и
`text` (`src/components/fields/text.vue`), отличается рендером (`v-textarea`,
авто-высота).

## Атрибуты

Атрибуты те же, что у [`text`](text.md), кроме текстовых подтипов (`subtype`
для `textarea` не применяется). Часто используются:

| Атрибут | Смысл |
|---|---|
| `description`, `name`, `value` | базовые |
| `read_only` | только чтение |
| `regexp_rules` | валидация `[regex, msg, ...]` |
| `add_description` | подпись под полем |
| `before_html` / `after_html` | HTML вокруг поля |
| `filter_on` | показывать в фильтрах списка |
| `full_str` | на всю ширину блока |

## Примеры

```python
{'description': 'Анонс', 'type': 'textarea', 'name': 'anons'}

{'description': 'Анонс', 'type': 'textarea', 'name': 'anons',
 'regexp_rules': ['/^.{3,255}$/', 'длина анонса должна быть не менее 3 символов']}

{'description': 'Описание в списке', 'type': 'textarea', 'name': 'description',
 'filter_on': 1}
```

## Особенности

- По умолчанию рендерится «полной строкой» (описание сверху).
- Ошибки/подсказки выводятся сразу под полем (классы `.err` / `.add_description`).
- Для длинного текста с форматированием используйте [`wysiwyg`](wysiwyg.md).
