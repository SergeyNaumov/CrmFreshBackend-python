# 11. Дерево и галерея (admin_tree)

Роут `GET|POST /admin-tree/{config}` → `routes/admin_tree/admin_tree_run.py`.
Поведение зависит от ключей формы.

## Ключи формы

| Ключ | Смысл |
|---|---|
| `tree_use` | `1` — дерево по `parent_id`; иначе плоский список |
| `max_level` | Максимальный уровень вложенности (влияет на показ «+»/добавление) |
| `tree_select_header_query` | Свой SQL для заголовков веток (вместо `SELECT *`) |
| `header_field` | Поле-заголовок узла |
| `sort`, `sort_field` | Сортировка (`ORDER BY sort_field`); drag&drop только при `sort` |
| `changed_in_tree` | `1` — редактирование прямо в дереве (модалка `FormInBranch`) |
| `default_find_filter` | Заголовок ветки, по умолчанию строится из `header_field` |
| `not_create` | Запрет добавления |
| `make_delete` | Разрешить удаление узлов |
| `read_only` | Запрет редактирования/сортировки |
| `view_type` | `'gallery'` — вывод галереей (см. ниже) |
| `photo_for_gallery` | Поле-файл с фото для галереи |
| `cols` | Число колонок галереи |

## Плоское дерево (без иерархии)

`tree_use: False` — просто список с редактированием/удалением/сортировкой.
Пример — `news`, `advantages`.

## Иерархия (`tree_use: True`)

- Узлы группируются по `parent_id` (корень — `parent_id IS NULL or 0`).
- Раскрытие узла подгружает детей через `action:'get_branch'`
  (`show_this` на фронте).
- `max_level` ограничивает показ «+» и вложенность.

## `tree_select_header_query`

Если нужен особый заголовок ветки (например, из join-а или с вычислением),
задайте SQL целиком. В примере `get_branch` использует его и вместо `SELECT *`,
и для пути ветки.

## Галерея (`view_type: 'gallery'`)

Плоский вывод карточками «фото + название». См.
`conf_projects/project_5830/advantages/__init__.py`.

```python
form = {
    'work_table': 'struct_5830_advantages',
    'title': 'Наши преимущества',
    'view_type': 'gallery',
    'photo_for_gallery': 'photo',   # имя поля type='file'
    'cols': 3,                       # число колонок
    'sort': 1,                       # разрешить перетаскивание
    'tree_use': False,
    'header_field': 'header',
    'changed_in_tree': False,
    'fields': [
        {'description': 'Преимущество', 'type': 'textarea', 'name': 'header'},
        {'description': 'Иконка', 'type': 'file', 'name': 'photo',
         'filedir': './files/project_5830/advantages'},
    ],
}
```

Что делает бэкенд (`admin_tree_run.py`):

- При `view_type == 'gallery'` и заданном `photo_for_gallery` добавляет каждому
  узлу `el['photo']` — веб-путь: `filedir` (с заменой `./` → `/`) + имя файла.
- Отдаёт `form.view_type`, `form.photo_for_gallery`, `form.cols`.

Что делает фронт (`AdminTree/branch.vue`):

- Рисует сетку в `form.cols` колонок.
- Фото масштабируется с `object-fit: contain` (не обрезается).
- Перетаскивание карточки доступно только при `form.sort` (иначе Sortable
  `disabled`).
- Кнопки edit/delete — по hover, только при соответствующих правах.
- Название/карандаш открывают редактирование (модалка при `changed_in_tree`,
  иначе новая вкладка).

> Бэкенд принимает оба написания: `gallery`/`galery` и
> `photo_for_gallery`/`photo_for_galery`.

## Действия (`action` в POST)

| `action` | Что делает |
|---|---|
| `add_branch_plain` | Добавить узел(ы) по `header` (можно несколько через `\n`) |
| `get_branch` | Дети узла (`parent_id`) |
| `sort` | Сохранить порядок (`obj_sort`, только при `sort`) |
| `move` | Перенести узел (`id`, `to`) |
| `delete_branch` | Удалить узел (и потомков при `tree_use`) |
| `update_branch` | Быстро переименовать (`id`, `header`) |

При `add_branch_plain` бэкенд сам считает `sort` (в конце списка) и проставляет
`parent_id`/`path` для дерева.

## Событие `after_sort`

Вызывается после сохранения порядка (в дереве). Удобно для пересчёта кэша/сайта.

## Хитрости

- `changed_in_tree: True` даёт быстрое редактирование без ухода со страницы
  (модалка использует тот же form-engine, см. [12](12-layout-frontend.md)).
- Сортировка хранится в `sort_field`; при `add_branch_plain` новому узлу
  присваивается `max+1`.
- Для проектных таблиц `work_table` удобно собирать в `events.permissions`
  (например, `struct_5830_news`), см. `news/events.py`.
