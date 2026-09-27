# `multiconnect` — связь многие-ко-многим

Связь M2M через таблицу связи. Бэкенд: `lib/CRM/form/multiconnect.py`,
`routes/edit_form/multiconnect.py`. Фронт: `src/components/fields/multiconnect.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `name` | имя поля |
| `relation_table` / `relation_table_header` / `relation_table_id` | таблица сущностей |
| `relation_save_table` | таблица связи |
| `relation_save_table_header` | колонка-подпись в таблице связи (если нужна) |
| `relation_save_table_id_worktable` | FK на текущую запись |
| `relation_save_table_id_relation` | FK на связанную сущность |
| `tree_use` | сущности — дерево |
| `tree_table` | таблица-дерево |
| `tablename` | алиас для фильтра в списке |
| `subtype` | `'table'` — с доп. полями связи |
| `fields` | доп. поля (при `subtype: 'table'`) |
| `fast_search` | быстрый поиск по списку |
| `make_add` | разрешить добавление новых тэгов |
| `view_only_selected` | показывать только выбранные |
| `out_tree` | выводить деревом (`v-treeview`) |
| `cols` | число колонок чекбоксов |
| `read_only` | только чтение |

## Пример (простой M2M)

```python
{
  'description': 'Доп. категории',
  'type': 'multiconnect',
  'name': 'good_category',
  'relation_table': 'category',
  'relation_table_header': 'header',
  'relation_table_id': 'id',
  'relation_save_table': 'good_category',
  'relation_save_table_header': 'header',
  'relation_save_table_id_worktable': 'good_id',
  'relation_save_table_id_relation': 'category_id',
  'tree_use': 1,
  'tree_table': 'category',
  'tablename': 'gc',
}
```

## Пример (со связью с доп. полями)

```python
{
  'description': 'Цвета и цены',
  'type': 'multiconnect',
  'subtype': 'table',
  'name': 'good_color',
  'relation_table': 'color', 'relation_table_header': 'header', 'relation_table_id': 'id',
  'relation_save_table': 'good_color',
  'relation_save_table_id_worktable': 'good_id',
  'relation_save_table_id_relation': 'color_id',
  'fields': [{'description': 'Цена', 'name': 'price', 'type': 'text'}],
}
```

## Особенности

- `get_values` возвращает список id (или объектов при `subtype: 'table'`).
- `save` удаляет отсутствующие связи и добавляет/обновляет новые; после —
  событие `after_save_multiconnect`.
- В фильтре `tablename` используется в `get_search_where`.
- При `subtype: 'table'` во фронте можно править доп. поля связи.
