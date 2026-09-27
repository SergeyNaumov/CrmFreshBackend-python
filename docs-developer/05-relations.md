# 05. Связи: select, 1_to_m, multiconnect, 1_to_1

## select_values

Выбор из фиксированного списка:

```python
{'description': 'Тип', 'type': 'select_values', 'name': 'type',
 'values': [{'v': '1', 'd': 'с вкладками'}, {'v': '2', 'd': 'без вкладок'}]}
```

- `v` — значение в БД, `d` — подпись.
- `multilpe` (так в коде) — мультивыбор (значения сохраняются списком).

## select_from_table

Значения тянутся из другой таблицы (`lib/CRM/form/get_values_for_select_from_table.py`):

```python
{'description': 'Рубрика', 'name': 'catalog_id', 'type': 'select_from_table',
 'table': 'struct_5830_catalog',
 'header_field': 'header',   # подпись (по умолчанию 'header')
 'value_field': 'id',        # значение (по умолчанию 'id')
 'where': 'enabled=1',       # необязательно (можно с WHERE/AND)
 'order': 'header',          # необязательно
 'tree_use': 1,              # построить иерархию по parent_id
 'tablename': 'c'}           # алиас в QUERY_SEARCH_TABLES (для списка)
```

Особенности:

- Если указан `query`, он используется целиком вместо сборки SELECT.
- `autocomplete` — запретить ввод произвольного значения. Если при этом нет
  `value`, список будет пустым (ожидается, что значение придёт из зависимости).
- В `edit_form` всегда добавляется первым пунктом «выберите значение»
  (`{'v':'0','d':'выберите значение'}`), в `admin_table`/`find_objects` — нет.
- `list` — готовый список (без запроса к БД).
- Значения подгружаются в `get_values()` (первый проход) и
  `get_fields_values()` (второй проход), см. [01](01-overview.md).

## Тип `select` (внутренний)

В `edit_form` `select_from_table`/`select_values`/`filter_extend_*` подменяются
на `select` (`lib/CRM/form/set_orig_types.py`), исходный тип — в `orig_type`.
Бэкенд-логика (сохранение, поиск) смотрит на `orig_type`.

---

## 1_to_m (дочерние записи)

Отдельная таблица, связанная `foreign_key`:

```python
{
  'description': 'Фотогалерея',
  'type': '1_to_m',
  'name': 'gal',
  'table': 'struct_5830_good_galery',
  'table_id': 'id',
  'foreign_key': 'good_id',
  'sort': 1,                     # сортировка дочерних
  'sort_field': 'sort',          # колонка сортировки (по умолчанию 'sort')
  'view_type': 'list',           # опционально: карточками вместо таблицы
  'fields': [                    # поля дочерней записи
     {'description': 'Название', 'name': 'header', 'type': 'text'},
     {'description': 'Фото', 'name': 'photo', 'type': 'file',
      'filedir': './files/project_5830/good/galery'},
  ],
  'tab': 'gal',
}
```

| Атрибут | Смысл |
|---|---|
| `table`, `table_id`, `foreign_key` | дочерняя таблица, PK и FK |
| `foreign_key_value` | жёсткая привязка; если задан пустым — дочерних не будет |
| `sort`, `sort_field` | сортировка дочерних |
| `where`, `order` | доп. SQL (объединяются с `foreign_key`) |
| `fields` | поля дочерней записи |
| `view_type` | `'list'` — вывод карточками (`1_to_m/slide.vue`) |
| `not_out_in_slide` | не выводить поле в слайде |
| `change_in_slide` | редактировать прямо в строке слайда |
| `slide_code` | `async def(form, field, data)` — преобразовать значение при выводе |

Поля дочерней записи тоже читают общие атрибуты (`type`, `description`, `name`,
`filedir`, `subtype`, `change_in_slide`, `not_out_in_slide`). Дочерние
`select_from_table` подгружаются автоматически.

Сохранение/удаление/сортировка — `routes/one_to_m_routes.py`:
`/1_to_m/insert/...`, `/1_to_m/update/...`, `/1_to_m/delete/...`, `/1_to_m/sort/...`,
`/1_to_m/upload_file/...`, `/1_to_m/update_field/...`.

### Редактирование в слайде

- `change_in_slide: 1` у дочернего поля — inline-редактирование в списке слайдов.
- `slide_code` — вычисляемое значение; пример:

```python
async def price_with_tax(form, field, data):
    return str(float(data.get('price') or 0) * 1.2)
# в поле: {'name':'price_tax','type':'text','slide_code':price_with_tax}
```

---

## multiconnect (M2M)

Связь многие-ко-многим через таблицу связи (`lib/CRM/form/multiconnect.py`):

```python
{
  'description': 'Доп. категории',
  'type': 'multiconnect',
  'name': 'good_category',
  'relation_table': 'category',              # таблица сущностей
  'relation_table_header': 'header',
  'relation_table_id': 'id',
  'relation_save_table': 'good_category',    # таблица связи
  'relation_save_table_header': 'header',
  'relation_save_table_id_worktable': 'good_id',
  'relation_save_table_id_relation': 'category_id',
  'tree_use': 1,                             # если сущности — дерево
  'tree_table': 'category',
  'tablename': 'gc',                         # алиас для фильтра
}
```

Дополнительные поля связи (`subtype == 'table'`):

```python
{
  'type': 'multiconnect', 'subtype': 'table', 'name': 'good_color',
  'relation_save_table': 'good_color',
  'relation_save_table_id_worktable': 'good_id',
  'relation_save_table_id_relation': 'color_id',
  'fields': [
      {'description': 'Цена', 'name': 'price', 'type': 'text'},
  ],
}
```

Поведение: `get_values` возвращает список id (или объектов для `subtype='table'`);
`save` удаляет отсутствующие и добавляет/обновляет связи; после — событие
`after_save_multiconnect`.

## 1_to_1 (поле в отдельной таблице)

Типы `1_to_1_text`, `1_to_1_textarea`, `1_to_1_wysiwyg`, `1_to_1_checkbox`,
`1_to_1_switch`, `1_to_1_select_values`.

```python
{
  'description': 'Таблица размеров',
  'type': '1_to_1_wysiwyg',
  'name': 'size_table',
  'save_table': 'category_sizes',  # отдельная таблица
  'foreign_key': 'id',             # колонка связи в save_table (на form.id)
  'db_name': 'body',               # колонка значения внутри save_table
}
```

- Обязательны `save_table` и `foreign_key` (иначе ошибка в `get_values`).
- Значение читается из `save_table` по `foreign_key = form.id`.
- Сохранение — `save_form.py:update_1_to_1` (через `replace`).
- `db_name` по умолчанию = `name`.
