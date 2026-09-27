# 02. Ключи формы `form = {...}`

Все ключи словаря `form` через `load_data` становятся атрибутами объекта
`Form` (`lib/CRM/form/__init__.py`). Ниже — сгруппированный справочник.

## Идентичность и база

| Ключ | Тип | По умолч. | Смысл |
|---|---|---|---|
| `title` | str | `''` | Заголовок экрана (попадает в `document.title` на фронте) |
| `work_table` | str | имя `config` | Таблица записей |
| `work_table_id` | str | `'id'` | PK |
| `header_field` | str | `'header'` | Поле-заголовок (заголовок дерева/списка) |
| `fields` | list | `[]` | Список полей (см. [03](03-fields-common.md), [04](04-field-types.md)) |
| `card_format` | str | `'vue'` | Формат карточки; `'old'` → ссылка на `/edit_form.pl?...` |

## Права и скоуп

| Ключ | Смысл |
|---|---|
| `read_only` | Запрет редактирования (карточка только для чтения, нельзя сохранять) |
| `not_create` | Запрет создания новых записей |
| `not_edit` | Скрыть карандаш редактирования в списке |
| `make_delete` | Можно удалять (при `read_only` по умолчанию `0`) |
| `foreign_key`, `foreign_key_value` | Значение FK, автоматически дописывается при insert/update и фильтрует записи |
| `work_table_foreign_key`, `work_table_foreign_key_value` | Дополнительная проверка родителя при update |
| `permissions` | Событие (см. [08-events.md](08-events.md)), не обычный ключ |

## Сортировка и списки (admin_table / find_objects)

| Ключ | Смысл |
|---|---|
| `sort` | Включить сортировку. Для списка — сортировка по `sort_field`; для галереи/дерева — разрешает drag |
| `sort_field` | Колонка сортировки (по умолчанию `'sort'`) |
| `default_find_filter` | Поле(я) фильтра по умолчанию (строка или список) |
| `search_on_load` | `1` — выполнить поиск сразу при открытии списка |
| `perpage` | Записей на страницу (по умолчанию `20`) |
| `not_perpage` | `1` — без постраничности |
| `not_order` | Глобально запретить сортировку |
| `QUERY_SEARCH_TABLES` | JOIN-ы для поиска: `[{'t':...,'alias':...,'link':...,'lj':1,'for_fields':[...]}]` |
| `GROUP_BY` | `GROUP BY` для запроса поиска |
| `add_where` | Доп. условия (строка или список) |
| `search_links` | Доп. ссылки над фильтрами |
| `on_filters` | Готовые значения фильтров |
| `filters_groups` | Группы фильтров |
| `before_filters_html` | HTML перед фильтрами |
| `search_plugin`, `search_multi_action` | Плагин выдачи / массовые действия (см. [10](10-lists-filters.md)) |
| `explain` | `1` — выводить SQL поиска (отладка) |

## Дерево (admin_tree)

| Ключ | Смысл |
|---|---|
| `tree_use` | `1` — дерево по `parent_id` (иначе плоский список) |
| `max_level` | Максимальный уровень вложенности |
| `tree_select_header_query` | Кастомный SQL заголовков веток |
| `changed_in_tree` | `1` — редактирование прямо в дереве (модалка) |
| `sort`, `sort_field` | Сортировка веток |

## Раскладка карточки (edit_form)

| Ключ | Смысл |
|---|---|
| `cols` | Колонки → блоки: `[[{'description','name','hide'}], [...]]` |
| `tabs` | Вкладки: `[{'name','description'}]` (поле привязывается через `tab`) |
| `wide_form` | Широкая карточка |
| `width` | Ширина (CSS) |
| `redirect` | URL, куда перейти после загрузки карточки |
| `javascript` | Словарь JS: `{'edit_form': '...', 'admin_table': '...', 'find_objects': '...'}` |
| `javascript_static` | Словарь внешних скриптов: `{'edit_form_static': [url, ...]}` |

Структура `cols`: внешний список — колонки, внутри каждой список блоков
(`{'description': заголовок, 'name': имя блока, 'hide': 0/1, 'on_show': 'js'}`).
Поле попадает в блок через `tab` (имя блока).

## Галерея (admin_tree)

| Ключ | Смысл |
|---|---|
| `view_type` | `'gallery'` (бэк также принимает `'galery'`) — вывод галереей «фото + название» |
| `photo_for_gallery` | Имя поля-файла, из которого берётся фото (бэк также `photo_for_galery`) |
| `cols` | Количество колонок галереи |

Пример — `conf_projects/project_5830/advantages/__init__.py`:

```python
form = {
    'work_table': 'struct_5830_advantages',
    'title': 'Наши преимущества',
    'view_type': 'gallery',
    'photo_for_gallery': 'photo',
    'sort': 1,
    'tree_use': False,
    'header_field': 'header',
    'changed_in_tree': False,
    'cols': 3,
    'fields': [
        {'description': 'Преимущество', 'type': 'textarea', 'name': 'header'},
        {'description': 'Иконка', 'type': 'file', 'name': 'photo', 'filedir': './files/project_5830/advantages'},
    ],
}
```

## Константы (const)

| Ключ | Смысл |
|---|---|
| `work_table` | Обычно `const` |
| `name_field` | Колонка с именем константы (обычно `name`) |
| `value_field` | Колонка со значением (обычно `value`) |
| `work_table_foreign_key`, `work_table_foreign_key_value` | Скоуп констант (например, `template_id`) |
| `filedir`, `filedir_http` | Папка файлов и её HTTP-префикс (для поля `file`) |
| `tabs` | Табы на странице констант |

Пример — `conf_projects/project_5830/template_const/__init__.py`.

## Служебные поля объекта (не задавать в конфиге)

`config`, `script`, `id`, `action`, `db`, `s`, `request`, `manager`, `R`,
`errors`, `log`, `values`, `fields_hash` — выставляются рантаймом.

## Приоритет и значения по умолчанию

`Form.__init__` задаёт дефолты (`read_only=0`, `make_delete=1`, `header_field='header'`,
`work_table_id='id'`, `sort_field=''`, …), затем `default_config_attr`
дополняет их (`make_delete` учитывает `read_only`, `work_table` = имя папки).
Значения из вашего словаря всегда перекрывают дефолты.
