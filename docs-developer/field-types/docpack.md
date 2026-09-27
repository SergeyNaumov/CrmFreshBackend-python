# `docpack` — пакет документов

Составной виджет для работы с пакетами документов (счета, договоры, тарифы).
Фронт: `src/components/fields/docpack.vue` (+ `docpack/dogovor.vue`,
`docpack/docpack_new.vue`).

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `not_create_docpack` | запретить создание пакета |
| `only_dogovor` | только договоры |
| `after_html` | HTML после виджета |

## Пример

```python
{
  'description': 'Пакеты документов',
  'type': 'docpack',
  'name': 'docpack',
  'only_dogovor': 0,
}
```

## Особенности

- Виджет завязан на инструменты `docpack`, `tarif`, `ur_lico`, `dogovor`
  (см. ссылки внутри шаблона).
- Редкий тип: используйте как образец существующий конфиг/компонент.
- Удаление пакета доступно, если в нём нет счетов (`cnt_bill == 0`).
