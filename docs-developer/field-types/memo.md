# `memo` — комментарии к записи

Лента комментариев с автором и датой. Бэкенд: `routes/memo.py`; фронт:
`src/components/fields/memo.vue`.

## Атрибуты поля

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `memo_table` | таблица комментариев |
| `memo_table_id` | PK комментария |
| `memo_table_comment` | колонка текста |
| `memo_table_registered` | колонка даты |
| `memo_table_auth_id` | колонка автора |
| `memo_table_foreign_key` | FK на текущую запись |
| `auth_table` | таблица пользователей |
| `auth_id_field` / `auth_name_field` | id и имя пользователя |
| `show_type` | режим отображения |
| `reverse` | обратный порядок |
| `read_only` | запрет добавления/изменения |
| `before_out_tags` | `async def(form, data)` — обработка перед выводом |

## Пример

```python
{
  'description': 'Комментарии',
  'type': 'memo',
  'name': 'comments',
  'memo_table': 'memo',
  'memo_table_id': 'id',
  'memo_table_comment': 'comment',
  'memo_table_registered': 'registered',
  'memo_table_auth_id': 'manager_id',
  'memo_table_foreign_key': 'good_id',
  'auth_table': 'manager',
  'auth_id_field': 'id',
  'auth_name_field': 'name',
}
```

## Эндпоинты

`GET /memo/get/<config>/<field>/<id>`, `POST /memo/add/...`,
`POST /memo/update/...`, `GET /memo/delete/...`.

## Особенности

- Событие поля `after_add` вызывается после добавления комментария.
- В фильтрах доступен как `memo` (по дате/тексту/автору), см.
  [10-lists-filters.md](../10-lists-filters.md).
