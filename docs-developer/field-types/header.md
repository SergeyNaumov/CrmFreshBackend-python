# `header` — декоративный заголовок

Разделитель-заголовок. Используется в основном на странице констант
(`script='const'`), где рендерится как заголовок секции (`Const.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description` | текст заголовка |
| `type` | `'header'` |

## Пример

```python
{'description': 'YandexGPT', 'type': 'header'},
{'description': 'Включить YandexGPT', 'type': 'checkbox', 'name': 'yandexgpt-enable'},
```

## Особенности

- В `const` рендерит `description` как заголовок.
- В `edit_form` отдельного контрола нет — для заголовков используйте блоки
  `cols` (`{'description': 'Раздел', 'name': 'block'}`) и `tab`.
