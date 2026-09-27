# `component` — внешний Vue-компонент

Загружает внешний Vue-компонент по ссылкам из конфига. Фронт:
`src/components/fields/component.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `name` | имя поля |
| `template` | URL HTML-шаблона компонента |
| `methods` | URL JS-строки с `methods` (исполняется через `eval`) |
| `object` | URL JS-строки с объектом компонента (`eval`) |
| `data` | объект, дополняющий `data()` компонента |

> `object`/`methods` исполняются через `eval` — это доверенный код разработчика.
> См. [07-validation-deps.md](../07-validation-deps.md) и раздел безопасности в
> [15-conventions.md](../15-conventions.md).

## Пример

```python
{
  'description': 'Статистика',
  'type': 'component',
  'name': 'stat',
  'template': '/components/stat/template.html',
  'methods': '/components/stat/methods.js',
  'data': {'config': 'good'},
}
```

## Особенности

- Компонент грузится асинхронно; ошибки загрузки показываются через `<errors>`.
- Удобно для сложных кастомных виджетов, не покрытых штатными типами.
- `field.data` домешивается в реактивные данные компонента.
