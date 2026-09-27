# Массовые действия (`search_multi_action`)

Это не поля карточки, а действия над выбранными записями в списке.
Обработчик — `routes/multiaction_routes.py`, ключ формы — `search_multi_action`
(см. [10-lists-filters.md](../10-lists-filters.md)).

## Формат

```python
# search_multi_action.py
search_multi_action_list = [
    {'description': 'перенести всё в рубрику', 'type': 'set_all_value_field',
     'name': 'category_id', 'step': 1},
    {'description': 'изменить цену', 'type': 'change_price',
     'name': 'price', 'step': 1},
    {'description': 'удалить', 'type': 'delete', 'step': 1},
]
# __init__.py: 'search_multi_action': search_multi_action_list
```

| Ключ | Смысл |
|---|---|
| `description` | текст пункта меню |
| `type` | `set_all_value_field` / `change_price` / `delete` |
| `name` | имя поля, к которому применяется действие |
| `step` | шаг мастера (состояние UI) |

## Типы действий

### `set_all_value_field`
Установить одно значение всем выбранным записям:
`UPDATE <table> SET <name>=<value> WHERE id IN (...)`.

### `change_price`
Изменить числовое поле на процент/сумму:
`value = {'value': 10, 'operation': 'plus'|'minus', 'type': 'cnt'|'percent'}`.

### `delete`
Удалить выбранные записи (требует `make_delete`).

## Эндпоинт

```
POST /{config}
{
  "subaction": "set_all_value_field" | "change_price" | "delete",
  "ids": [1, 2, 3],
  "name": "price",
  "value": ...           # зависит от действия
}
```

## Требования

- В форме задан `search_multi_action`, иначе ошибка «отсутствует параметр
  конфига search_multi_action».
- `read_only`/`make_delete` проверяются для соответствующих действий.
