# `1_to_m` — дочерние записи

Отдельная таблица, связанная `foreign_key`. Поля дочерней записи описываются в
`fields`. Бэкенд: `lib/get_1_to_m_data.py`, роуты `routes/one_to_m_routes.py`.
Фронт: `src/components/fields/1_to_m.vue` и `1_to_m/{slide,form,...}.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `table` / `table_id` / `foreign_key` | дочерняя таблица, PK, FK (обязательно) |
| `foreign_key_value` | жёсткая привязка; пустое значение → дочерних нет |
| `sort` / `sort_field` | сортировка дочерних (`sort_field` по умолчанию `sort`) |
| `where`, `order` | доп. SQL (объединяются с `foreign_key`) |
| `fields` | поля дочерней записи |
| `view_type` | `'list'` — вывод карточками (`1_to_m/slide.vue`) вместо таблицы |
| `read_only` | только чтение |
| `not_create` | запрет добавления дочерних |
| `link_add` | внешняя ссылка на добавление (`<%form.id%>`, `<%id%>`) |
| `fields[].not_out_in_slide` | не выводить поле в слайде |
| `fields[].change_in_slide` | редактировать прямо в слайде |
| `fields[].slide_code` | `async def(form, field, data)` — вычисляемое значение |

## Пример

```python
{
  'description': 'Фотогалерея',
  'type': '1_to_m',
  'name': 'gal',
  'table': 'struct_5830_good_galery',
  'table_id': 'id',
  'foreign_key': 'good_id',
  'sort': 1,
  'fields': [
     {'description': 'Название', 'name': 'header', 'type': 'text'},
     {'description': 'Фото', 'name': 'photo', 'type': 'file',
      'filedir': './files/project_5830/good/galery'},
  ],
  'tab': 'gal',
}
```

## Inline-редактирование в слайде

```python
{'description': 'Цена', 'name': 'price', 'type': 'text',
 'change_in_slide': 1}

async def price_tax(form, field, data):
    return str(float(data.get('price') or 0) * 1.2)

{'description': 'С налогом', 'name': 'price_tax', 'type': 'text',
 'slide_code': price_tax}
```

## Эндпоинты

`GET /1_to_m/{config}/{field}/{id}` (данные), `POST /1_to_m/insert/...`,
`POST /1_to_m/update/...`, `POST /1_to_m/update_field/...`,
`POST /1_to_m/sort/...`, `GET /1_to_m/delete/...`,
`POST /1_to_m/upload_file/...`, `GET /1_to_m/download/...`,
`GET /1_to_m/delete_file/...`.

## Особенности

- Редактировать дочерние можно только после сохранения основной карточки
  (`form.id`).
- Если в дочерней записи ровно одно поле-файл, доступна массовая загрузка
  (`multiload`).
- `slide_code` вызывается на бэке при чтении каждого дочернего поля.
- Для `select_from_table` внутри `fields` значения догружаются автоматически.
