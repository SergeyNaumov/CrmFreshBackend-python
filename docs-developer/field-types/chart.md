# `chart` — график

График на canvas (библиотека в `src/js/chart.js`). Фронт:
`src/components/fields/chart.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `name` | имя поля |
| `style` | инлайн-стиль контейнера |
| `data` | данные графика (структура — как ждёт `src/js/chart.js`) |

## Пример

```python
{
  'description': 'Динамика продаж',
  'type': 'chart',
  'name': 'sales_chart',
  'style': 'height: 300px',
  'data': { 'labels': ['Янв', 'Фев'], 'values': [10, 20] },
}
```

## Особенности

- Используется внутри [`accordion`](accordion.md) (`content[].type == 'chart'`).
- Данные обычно формируются на бэке в `before_code`/`code`.
- Редкий тип — смотрите `chart.vue` и `src/js/chart.js` при интеграции.
