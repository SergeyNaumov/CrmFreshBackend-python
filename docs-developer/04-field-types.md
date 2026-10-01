# 04. Каталог типов полей

Тип поля — `type`. Ниже назначение, специфичные атрибуты и пример.
Общие атрибуты — в [03-fields-common.md](03-fields-common.md).

> 📂 Подробная документация по каждому типу (все атрибуты, примеры, особенности) —
> в папке [field-types/](field-types/README.md).
>
> Быстрые ссылки: [text](field-types/text.md) ·
> [textarea](field-types/textarea.md) ·
> [wysiwyg](field-types/wysiwyg.md) ·
> [checkbox](field-types/checkbox.md) ·
> [switch](field-types/switch.md) ·
> [select_values](field-types/select_values.md) ·
> [select_from_table](field-types/select_from_table.md) ·
> [date](field-types/date.md) ·
> [datetime](field-types/datetime.md) ·
> [time](field-types/time.md) ·
> [daymon](field-types/daymon.md) ·
> [yearmon](field-types/yearmon.md) ·
> [password](field-types/password.md) ·
> [file](field-types/file.md) ·
> [1_to_m](field-types/1_to_m.md) ·
> [multiconnect](field-types/multiconnect.md) ·
> [1_to_1](field-types/1_to_1.md) ·
> [filter_extend](field-types/filter_extend.md) ·
> [multiaction](field-types/multiaction.md)

Скрипты нормализуют часть типов (`set_orig_types`): в `edit_form` типы
`select_from_table`, `select_values`, `filter_extend_select_from_table`,
`filter_extend_select_values` превращаются в `select`, а оригинал хранится в
`orig_type`.

---

## Текстовые

### `text`
Однострочный текст.

| Атрибут | Смысл |
|---|---|
| `placeholder` | плейсхолдер |
| `values` | быстрые варианты-ссылки под полем (`[{'v','d'}]`) |
| `subtype` | `color`, `percent`, `qr_call`, `email`, `kladr`, `dadata_address` |
| `show_only_subtype` | показывать только подтип |
| `prefix_list`, `prefix_list_header` | выбор «города» для адреса (select + автозаполнение) |
| `hide_field` | не рисовать контрол |
| `style` | инлайн-стиль |

```python
{'description': 'Название', 'type': 'text', 'name': 'header', 'placeholder': 'до 200 символов'}

# цвет: палитра из values, значение — HEX
{'description': 'Цвет', 'type': 'text', 'name': 'color', 'subtype': 'color',
 'values': [{'v': '#000', 'd': 'чёрный'}, {'v': '#fff', 'd': 'белый'}]}

# адрес с подсказками DaData
{'description': 'Адрес', 'type': 'text', 'name': 'address', 'subtype': 'dadata_address'}
```

- `subtype=='color'` — цветовой пикер (см. `fields/text.vue`).
- `subtype=='kladr'`/`'dadata_address'` — автодополнение через
  `/extend/KLADR` и `/extend/DADATA`.
- `subtype=='qr_call'` — рендерится компонентом `text_subtypes/qr_call`.
- `subtype=='percent'` — процент (используется и внутри `multiconnect`).

### `textarea`
Многострочный текст (авто-высота).

```python
{'description': 'Анонс', 'type': 'textarea', 'name': 'anons'}
```

### `wysiwyg`
Визуальный редактор (TinyMCE) с загрузкой файлов.

| Атрибут | Смысл |
|---|---|
| `filedir` | папка для файлов редактора |
| `edit_mode` | `1` — сразу в режиме редактирования |
| `plugins` | `[{'type':'GPTAssist','set_value_button':'Отправить в описание'}]` |

```python
{'description': 'Описание', 'type': 'wysiwyg', 'name': 'body', 'filedir': './files/project_5830/news'}
```

> `GPTAssist` — не отдельный тип поля, а плагин к `text`/`wysiwyg`
> (см. `src/components/GPTAssist/`).

---

## Логические

### `checkbox`, `switch`
Булево значение `0/1`. Подпись — `description` (сам `label`).

```python
{'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled', 'value': 1}
{'description': 'Показывать', 'type': 'switch', 'name': 'show'}
```

---

## Выпадающие списки

### `select_values`
Выбор из фиксированного списка `values`.

| Атрибут | Смысл |
|---|---|
| `values` | `[{'v': '1', 'd': 'Первый'}, ...]` |
| `multilpe` | мультивыбор (внимание: именно `multilpe`, так в коде) |
| `background_color` | цвет фона выбранного (старые конфиги) |

```python
{'description': 'Тип', 'type': 'select_values', 'name': 'type',
 'values': [{'v':'1','d':'С вкладками'}, {'v':'2','d':'Без вкладок'}]}
```

### `select_from_table`
Выбор значения из другой таблицы.

| Атрибут | Смысл |
|---|---|
| `table` | таблица-источник |
| `header_field` | колонка-подпись (по умолчанию `header`) |
| `value_field` | колонка-значение (по умолчанию `id`) |
| `where`, `order` | фильтр/сортировка (можно SQL) |
| `query` | полностью свой SELECT (перекрывает всё) |
| `list` | готовый список (без запроса) |
| `tree_use` | список деревом (использует `parent_id`) |
| `autocomplete` | только выбор из списка (иначе можно ввести произвольное) |
| `tablename` | алиас таблицы в `QUERY_SEARCH_TABLES` (для сортировки/фильтра) |
| `db_name` | колонка-значение в текущей таблице, если не `name` |

```python
{'description': 'Рубрика', 'name': 'catalog_id', 'type': 'select_from_table',
 'table': 'struct_5830_catalog', 'header_field': 'header', 'value_field': 'id',
 'tree_use': 1, 'tablename': 'c'}
```

### `select`
Внутренний тип (образуется из `select_values`/`select_from_table` в
`edit_form`). В конфиге напрямую почти не используется.

---

## Даты и время

### `date`, `datetime`, `time`, `daymon`, `yearmon`
- `date` — дата `YYYY-MM-DD`.
- `datetime` — дата+время.
- `time` — время `HH:MM[:SS]`.
- `daymon` — день и месяц (`{день, месяц}`).
- `yearmon` — год и месяц (`YYYY-MM`).

| Атрибут | Смысл |
|---|---|
| `empty_value` | для пустой даты: `'null'` → в БД `NULL` (иначе `'0000-00-00'`) |
| `not_clear` | (datetime) не показывать «очистить» |
| `filter_type` | `'range'` — фильтр диапазоном в списке |

```python
{'description': 'Дата', 'type': 'date', 'name': 'registered', 'empty_value': 'null'}
{'description': 'Время', 'type': 'time', 'name': 'f_time', 'filter_on': True}
```

---

## Пароль

### `password`
Специальный вид: значение не отдаётся на фронт, есть генерация и отправка.

| Атрибут | Смысл |
|---|---|
| `min_length` | минимальная длина (по умолчанию `6`) |
| `generate_len_pas` | длина генерируемого пароля |
| `symbols` | алфавит для генерации |
| `methods_send` | `[{'description': '...', 'method_send': func}]` — варианты сохранения/отправки |

```python
{'description': 'Пароль', 'type': 'password', 'name': 'password', 'min_length': 8,
 'methods_send': [{'description': 'сохранить', 'method_send': without_send}]}
```

См. `routes/edit_form/process_edit_form.py` (тип сохраняется только при insert; в
`get_values` значение вырезается), `lib/CRM/form/save_form.py` (шифрование).

---

## Файлы

### `file`
Загрузка файла(ов) в `filedir`.

| Атрибут | Смысл |
|---|---|
| `filedir` | папка (обязательно). `./files/...` |
| `resize` | список `{'file','size','quality','grayscale','composite_*'}` |
| `crops` | пропорции для кропа (`cropper`) |
| `cropper` | включить кроппер |
| `preview` | `'WxH'` — какая из `resize` используется для превью (в 1_to_m/списках) |
| `size`, `quality` | размер/качество по умолчанию |

```python
{'description': 'Фото', 'name': 'photo', 'type': 'file',
 'filedir': './files/project_5830/good',
 'preview': '156x117',
 'resize': [
   {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '156x117', 'quality': '100'},
   {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '355x215', 'quality': '100'},
 ]}
```

Подробности — [06-files-wysiwyg.md](06-files-wysiwyg.md).

---

## Связи (подробно — [05-relations.md](05-relations.md))

### `1_to_m`
Дочерние записи («слайды»). | Атрибут | Смысл | |---|---| |
`table`, `table_id`, `foreign_key` | дочерняя таблица и связь | |
`foreign_key_value` | жёсткая привязка (иначе `form.id`) | |
`sort`, `sort_field` | сортировка дочерних | |
`where`, `order` | доп. SQL | |
`fields` | поля дочерней записи | |
`view_type` | `'list'` — карточками, иначе таблица | |
`not_out_in_slide`, `change_in_slide`, `slide_code` | управление выводом в слайде | |

### `multiconnect`
M2M через таблицу связи. | Атрибут | Смысл | |---|---| |
`relation_table`, `relation_table_header`, `relation_table_id` | таблица
сущностей | | `relation_save_table`, `relation_save_table_header`,
`relation_save_table_id_worktable`, `relation_save_table_id_relation` | таблица
связи | | `tree_use`, `tree_table`, `tablename` | дерево/алиас | |
`subtype == 'table'` + `fields` | с доп. полями связи | | `fast_search`,
`view_only_selected`, `out_tree` | режимы отображения |

### `1_to_1_text`, `1_to_1_textarea`, `1_to_1_wysiwyg`, `1_to_1_checkbox`, `1_to_1_switch`, `1_to_1_select_values`
Поле, хранимое в отдельной таблице (один-к-одному). Обязательны `save_table`,
`foreign_key`.

```python
{'description': 'Таблица размеров', 'type': '1_to_1_wysiwyg',
 'save_table': 'category_sizes', 'foreign_key': 'id',
 'name': 'size_table', 'db_name': 'body'}
```

---

### `multiconnect_old`
Старый мультичекбокс (совместимость со Perl-типом `multicheckbox`): опции
задаются строкой `extended`, выбранное хранится строкой `;key1;;key2;` в поле
основной таблицы. Подробно — [field-types/multiconnect_old.md](field-types/multiconnect_old.md).

## Прочие типы (кратко)

| Тип | Назначение | Документ |
|---|---|---|
| `font-awesome` | выбор иконки | [field-types/font-awesome.md](field-types/font-awesome.md) |
| `memo` | комментарии к записи | [field-types/memo.md](field-types/memo.md) |
| `in_ext_url` | ЧПУ (таблица `in_ext_url`) | [field-types/in_ext_url.md](field-types/in_ext_url.md) |
| `code` | HTML, формируемый `code(form, field)` (sync) | [field-types/code.md](field-types/code.md) |
| `header` | декоративный заголовок (для `const`) | [field-types/header.md](field-types/header.md) |
| `component` | загрузка внешнего Vue-компонента | [field-types/component.md](field-types/component.md) |
| `accordion` | секция-аккордеон | [field-types/accordion.md](field-types/accordion.md) |
| `table` | таблица | [field-types/table.md](field-types/table.md) |
| `time_table` | расписание | [field-types/time_table.md](field-types/time_table.md) |
| `chart` | график | [field-types/chart.md](field-types/chart.md) |
| `docpack` | пакет документов | [field-types/docpack.md](field-types/docpack.md) |

### `code` — пример

```python
{'description': 'Товары', 'type': 'code', 'name': 'goods', 'full_str': 1,
 'after_html': '//'}
```

В `events_for_fields.py` поле `goods` получает `code(form, field)`, который
формирует `field['html']`. Функция **синхронная** (`edit_form_process_fields.py:28`).

### `in_ext_url` — пример

Обычно создаётся плагином в `events.py`:

```python
await InExtUrl(form, {
    'foreign_key': 'project_id', 'foreign_key_value': project_id,
    'dependence_field': 'header',        # поле, из которого генерится ЧПУ
    'in_url': '/news/<%id%>',            # уникальное «внутреннее» имя
    'after_field': 'header',
    'url_prefix': '/news/',
    'ajax': 'in_ext_url',
    'tab': 'promo',
})
```

---

## Типы только для фильтров (admin_table)

`filter_extend_*` — фильтры списка, ищущие по **смежной** таблице
(`QUERY_SEARCH_TABLES`); обычные типы фильтруют текущую `work_table` и
выводятся в карточке.

| Тип | Аналог | В карточке | Смысл |
|---|---|---|---|
| `filter_extend_text` | `text` | нет* | текст по `db_name` (LIKE) |
| `filter_extend_select_values` | `select_values` | вырезается | select по `values` |
| `filter_extend_select_from_table` | `select_from_table` | вырезается | select из таблицы |
| `filter_extend_date` / `filter_extend_datetime` | `date`/`datetime` | нет* | диапазон дат |
| `filter_extend_checkbox` / `filter_extend_switch` | `checkbox`/`switch` | нет* | булев фильтр по JOIN |

\* Бэкенд вырезает из `edit_form` только поля с `orig_type`, начинающимся на
`filter_extend_` (а он ставится лишь для двух select-типов). Остальные
`filter_extend_*` остаются в форме, но фронт их не рисует (нет компонента).
Подробности — [field-types/filter_extend.md](field-types/filter_extend.md) и
[19-known-gaps.md](19-known-gaps.md).

## Массовые действия (`search_multi_action`)

Не тип поля, а список действий в форме (см. [10](10-lists-filters.md)).
`type` действий: `set_all_value_field`, `change_price`, `delete`
(`routes/multiaction_routes.py`).
