# 19. Известные расхождения и дефекты

Здесь собраны места, где код ведёт себя не так, как ожидается (или не так, как
описано в старых документах). Это не призыв «срочно чинить» — а карта граблей.

## `filter_extend_*`: вырезание из карточки

- **Ожидается** (и так написано в старых `04`/`filter_extend.md`): все
  `filter_extend_*` вырезаются из `edit_form`.
- **Реально** (`routes/edit_form/process_edit_form.py:55`): вырезаются только
  поля, у которых `orig_type` начинается на `filter_extend_`, а `orig_type`
  ставится (`set_orig_types.py:25`) лишь для `filter_extend_select_values` и
  `filter_extend_select_from_table`.
- Следствие: `filter_extend_text`, `filter_extend_checkbox`,
  `filter_extend_switch`, `filter_extend_date`, `filter_extend_datetime`
  остаются в `form.fields`. Фронт не падает (у них нет компонента в
  `FormBlock.dynamic_component` — поле просто не рисуется), но они занимают
  место в форме и потенциально участвуют в обработке.
- **Обход:** для «фильтр-only» полей, которые должны гарантированно не попадать
  в карточку, можно вручную поставить `'orig_type':'filter_extend_text'` и т.п.

## `filter_extend_checkbox` / `filter_extend_switch` и фильтры

- `get_filters_routes.py` **не** конвертирует эти типы в тип фильтра, а в
  `OnFilters.dynamic_component` (фронт) ветки для них нет и `filter-checkbox`
  не зарегистрирован.
- Итог: булев фильтр по смежной таблице через `filter_extend_checkbox` в списке
  **не отрисуется**.
- WHERE при этом строится корректно (`get_search_where.py:120`):
  `table.db_name = 0/1`.
- **Обход:** если нужен булев фильтр по текущей таблице — использовать
  `checkbox` + `filter_on` (фронт сам покажет select «Не использовать/Да/Нет»,
  см. `AdminTable.vue:333-341`). Для JOIN-таблицы — нужна доработка фронта.

## Исправлено (2026-09-28): `filter_extend_*` и `tablename`

- `lib/CRM/form/get_search_where.py` для `filter_extend_select_values`
  строил WHERE по `wt.db_name`, игнорируя `tablename` — фильтры по смежной
  таблице (`author` → `apv.login`, `tmp_type` → `t.type`) падали.
- Теперь для типов `filter_extend_*` используется алиас `table` (=`tablename`).

## `filter_extend_datetime`

- Не конвертируется в `get_filters` и не имеет ветки в `process_result_list`
  (в отличие от `date`/`datetime`). Для диапазона дат по JOIN лучше
  `filter_extend_date`.

## `get_filters_routes.py`: select-фильтры без значений

- В файле есть локальная заглушка `get_values_for_select_from_table` (строки
  9-10), которая всегда возвращает `[]`, и вызывается она с обратным порядком
  аргументов (`:57`).
- Следствие: select-фильтры по `select_from_table` могут прийти без `values`.

## `read_config` и `project_id` (исправлено)

- `lib/all_configs.py` при пустом `project_id` не инициализировал `form` и падал
  с `UnboundLocalError` на `if not(form)`.
- Исправлено: `form=False; errors=[]` объявляются до ветки проекта. Это
  необходимо для админки, работающей без проекта
  (`request.state.project['project_id'] is None`).

## Прочие дефекты (не связаны с админкой)

- `lib/core.py:85-91` — `get_func` ищет `func:` в `f['name']`, а не в `f['db_name']`.
- `lib/CRM/form/get_search_where.py:138` — неопределённая `dn_name` в ветке
  текстового поля с `func:`.
- `routes/get_result/process_result_list.py:96` — ветка `field['type'].startswith('font')`
  обращается к несуществующему ключу.
- `lib/CRM/form/save_form.py:20` — `update_1_to_1` не сохраняет
  `1_to_1_select_values` (читается, но не пишется).
- `routes/edit_form/process_edit_fields.py:11` — опечатка `enctypt_method` (не
  удаляется реальный `encrypt_method`).
- `save_form.py:120` берёт `config['auth']['encrypt_method']`, а
  `routes/password.py:37` — `config['encrypt_method']`.

## Исправлено (2026-09-28): autocomplete

- `routes/autocomplete.py`, ветка `filter_extend_text`, безусловно читала
  `element['filter_table']` → `KeyError` (500), если в поле задан только
  `tablename`. Теперь таблица определяется по `tablename` (алиас) или
  `filter_table`; для `filter_extend_text` строится
  `SELECT DISTINCT db_name ... LIKE %s`.
- В той же функции `search_query` получал `limit 30` дважды
  (`limit 30 limit 30`) → SQL-ошибка и `list:null`. `limit` добавляется один раз.
- `get_list` теперь всегда возвращает список (в конце добавлен `return []`).

## См. также

- [field-types/filter_extend.md](field-types/filter_extend.md)
- [16-field-types-backend.md](16-field-types-backend.md)
