# Типы полей (`form.fields[].type`)

Сжатая карта для агентов. Пользовательская версия с примерами —
`docs-developer/04-field-types.md`, `docs-developer/16-field-types-backend.md`,
`docs-developer/field-types/*`.

## Конвейер

`read_config` (`lib/all_configs.py`) → `set_orig_types` →
`get_values` → `run_all_before_code` → `get_fields_values`.

`set_orig_types.py:25` ставит `orig_type` и `type='select'` (только в
`edit_form`) **лишь** для: `select_from_table`, `select_values`,
`filter_extend_select_from_table`, `filter_extend_select_values`.

`is_wt_field` (`lib/core.py:165-175`) — белый список типов, сохраняемых в
основную таблицу: `text, textarea, hidden, wysiwyg, select_from_table,
select_values, checkbox, switch, date, time, datetime, yearmon, daymon,
font-awesome, file, codelist`.

## Матрица `type` × этап

| type | get-filters | WHERE | edit-form | get-result | save |
|---|---|---|---|---|---|
| `text`/`textarea` | → text | LIKE (`= %s` при `filter_type:'eq'`) | да | html | `is_wt_field` |
| `wysiwyg` | как есть | общая | да | html | `is_wt_field` |
| `checkbox`/`switch` | как есть | `=0/=1` | да | да/нет | пусто→`'0'` |
| `select_values` | → select | `IN wt.db_name` | select+orig_type | подпись values | пусто→`'0'` |
| `select_from_table` | → select | `IN wt.db_name` | select+orig_type | header_field | пусто→`'0'` |
| `date`/`datetime` | range | `>=`/`<=` | да | date_to_rus | спец. |
| `time` | range | общая | да | строка | `00:00:00` |
| `daymon`/`yearmon` | range | общая | да | html | `is_wt_field` |
| `hidden` | пропуск | общая | да | html | `is_wt_field` |
| `font-awesome` | как есть | общая | да | `startswith('font')` | `is_wt_field` |
| `file` | как есть | `<>""`/`=""` | да | ссылка | `is_wt_field` |
| `password` | пропуск | — | генерация | `[зашифрован]` | только insert |
| `code` | пропуск | — | `code(form,field)` | html | нет |
| `1_to_m` | пропуск | не сортируется | да | html | отдельно |
| `1_to_1_*` | — | — | да | html | `update_1_to_1` |
| `multiconnect` | как есть | `relation_table_id IN` | да | group_concat | `multiconnect_save` |
| `multiconnect_old` | пропускается | — | да (чекбоксы) | строка | `is_wt_field` (строка `;key;`) |
| `memo` | тянет users | дата/текст/автор | да | type=memo | нет |
| `in_ext_url` | как есть | сорт. по ext_url | да | `in_ext_url__ext_url` | `save_in_ext_url` |
| `filter_extend_text` | → text | LIKE | **не вырезано** | html | — |
| `filter_extend_select_values` | → select | `IN wt.db_name` | вырезано | values | — |
| `filter_extend_select_from_table` | → select | `IN table.db_name` | вырезано | header_field | — |
| `filter_extend_date` | → date | диапазон | **не вырезано** | html | — |
| `filter_extend_datetime` | как есть | диапазон | **не вырезано** | нет ветки | — |
| `filter_extend_checkbox`/`_switch` | **как есть** | `table.db_name=0/1` | **не вырезано** | да/нет | — |
| `filter_extend_time` | как есть | общая | — | строка | — |

Код: `routes/get_filters_routes.py:41-78`, `lib/CRM/form/get_search_where.py`,
`routes/edit_form/process_edit_form.py:53-58`,
`routes/get_result/process_result_list.py:60-164`, `lib/CRM/form/save_form.py`.

## Типы-компоненты (виртуальные поля)

Часть типов — не колонки, а «слоты» под Vue-компонент: в основную таблицу не
сохраняются (`is_wt_field` их не знает), в `get-filters`/`get-result` не
участвуют (в конфиге помечаются `not_filter:1`), а в карточке рендерятся
компонентом `field-<type>`.

| type | Компонент (фронт) | Смысл |
|---|---|---|
| `project_clone` | `ProjectClone.vue` | клон проекта (легаси: свой `template` + папка) |
| `project_export` | `ProjectExport.vue` | выгрузка проекта |
| `project_struct` | `ProjectCreateStruct.vue` | уникальные структуры проекта |
| `project_sitemap` | `ProjectSitemap.vue` | карта сайта проекта |
| `domain_sync` | `DomainSync.vue` | перенос/копирование настроек конструктора на другой домен |
| `page_blocks` | редактор блоков | блоки страницы (конфиги DS) |
| `in_ext_url` | `fields/in_ext_url.vue` | ЧПУ записи (текст) — читается/пишется в `in_ext_url` |

### `in_ext_url` — ЧПУ в карточке

Поле не колонка `wt`: значение читается из `in_ext_url` по шаблону `in_url`
(`lib/CRM/form/get_values.py::get_in_ext_url`) и переопределяет авто-slug.

```python
{'description':'URL (ЧПУ)','type':'in_ext_url','name':'in_ext_url','in_url':'/news/<%id%>'},
```

Правила записи (`lib/CRM/chpu.py::save_chpu_for_form`, только для конфигов с
`chpu_*`): ввели новое значение → сохраняем его (транслит + дедуп); очистили →
генерируем из `chpu_dependence_field`; url ещё нет (новая запись) → генерируем;
url есть и не менялся → **не трогаем** (переименование заголовка не ломает
проиндексированный адрес). В списках/фильтрах поле работает через
`LEFT JOIN in_ext_url` (`get_search_tables.py` подмешивает join, если в
`fields` есть такое поле) — иначе колонка `in_ext_url__ext_url` была бы пустой.

Цепочка: `form.fields[].type` → `EditForm/FormBlock.vue` (`case '<type>'` →
`field-<type>`) → `src/dynamic_component_loader.js`
(`app.component('field-<type>', defineAsyncComponent(...))`). Компонент получает
пропсы `form` и `field`; `form.id` — id записи (`work_table_id`), например в
карточке домена это `domain_id`. Подробности про инструменты — `15-svcms-admin.md`.

## filter_extend_* — фильтры по JOIN

- Обычный тип фильтрует **текущую** `work_table` (`wt`) и выводится в карточке.
- `filter_extend_*` фильтрует **смежную** таблицу: `tablename` = alias из
  `QUERY_SEARCH_TABLES`, `db_name` = SQL-выражение по алиасу.
- `checkbox` (текущая таблица + EditForm) ↔ `filter_extend_checkbox`
  (смежная таблица, только фильтр; `table.db_name = 0/1`).
- `QUERY_SEARCH_TABLES` (`lib/CRM/form/get_search_tables.py:20-81`): `t/table`,
  `a/alias`, `l/link` (ON), `lj/left_join`, `for_fields`, `select_fields`,
  `not_add_in_select_fields`.

## Мультиконнект

Атрибуты: `relation_table`, `relation_table_header`, `relation_table_id`,
`relation_save_table`, `relation_save_table_header`,
`relation_save_table_id_worktable`, `relation_save_table_id_relation`,
`relation_tree_order`, `tree_use`, `tree_table`, `subtype:'table'`+`fields`,
`tablename`. Код: `lib/CRM/form/multiconnect.py`,
`routes/edit_form/multiconnect.py`.

## Memo

`memo_table`, `memo_table_id`, `memo_table_comment`, `memo_table_registered`,
`memo_table_auth_id`, `memo_table_foreign_key`, `memo_table_alias`, `auth_table`,
`auth_id_field`, `auth_name_field`. Код: `routes/memo.py`.

## 1_to_m

`table`, `table_id`, `foreign_key`, `foreign_key_value`, `fields`, `sort`,
`sort_field`, `where`, `order`, `view_type`, `not_out_in_slide`,
`change_in_slide`. Код: `lib/get_1_to_m_data.py`,
`routes/edit_form/one_to_m/*`.

## multiconnect_old

Совместимость со старым `multicheckbox`: опции описываются строкой `extended`
(`key;подпись;...`), хранится строкой `;key1;;key2;` в колонке основной таблицы.
Реализация: `lib/CRM/form/multiconnect_old.py` (`parse_extended`/`split_value`/
`join_value`), `lib/core.py` (`check_list`), `lib/CRM/form/get_values.py`
(парсинг `extended`), фронт `src/components/fields/multiconnect_old.vue`.
Пример — `configs/svcmsadmin/project` (поле `options`).

## punycode (домены)

Атрибут поля `'punycode': True` (текстовые фильтры домена): при поиске
(`get_search_where`) и в `/autocomplete` значение нормализуется в punycode
(`lib/CRM/form/idn.py:prepare_search_domain`), а при выводе
(`process_result_list`, autocomplete) — обратно в юникод
(`domain_to_unicode`). Пример — `configs/svcmsadmin/project` (поле `domain`).

## Связанные дефекты

См. `10-known-issues.md` (filter_extend не вырезается/не конвертируется,
заглушка select-фильтров, `read_config` form-init исправлен).
