# `filter_extend_*` — фильтры по смежным таблицам (JOIN)

`filter_extend_*` — это **не поля карточки**, а поля-**фильтры** списка.
Ключевая идея: такой фильтр ищет по колонке **смежной таблицы** (из
`QUERY_SEARCH_TABLES`), а не по основной `work_table`.

Сравнение с обычными типами:

| | Обычный тип (`text`, `checkbox`, `select_from_table`, `date`) | `filter_extend_*` |
|---|---|---|
| Где хранится | основная таблица (`wt`) | смежная таблица (алиас из JOIN) |
| В карточке EditForm | **да** (сохраняется) | нет (только список) |
| Фильтр в списке | да | да |
| `db_name` | колонка (или выражение) | SQL-выражение по алиасу |
| Нужен `tablename` + JOIN | обычно нет | **обязательно** |

Пример пары для одного и того же смысла:

```python
# checkbox — булев признак в САМОЙ таблице; виден и в карточке, и в фильтре
{'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled', 'filter_on': True}

# filter_extend_checkbox — булев признак в СМЕЖНОЙ таблице ph; только фильтр
{'description': 'Хостинг выключен', 'type': 'filter_extend_checkbox',
 'name': 'disabled', 'tablename': 'ph', 'db_name': 'disabled'}
```

## Виды `filter_extend_*`

| Тип | Аналог (обычный) | WHERE | `db_name` |
|---|---|---|---|
| `filter_extend_text` | `text` | `db_name LIKE %s` | колонка/выражение смежной таблицы |
| `filter_extend_select_values` | `select_values` | `wt.db_name IN (...)` | обычно колонка текущей |
| `filter_extend_select_from_table` | `select_from_table` | `table.db_name IN (...)` | если нет — берётся `value_field` |
| `filter_extend_date` | `date` | диапазон `>=` / `<=` | колонка |
| `filter_extend_datetime` | `datetime` | диапазон `>=` / `<=` | колонка |
| `filter_extend_checkbox` | `checkbox` | `table.db_name = 0/1` | колонка |
| `filter_extend_switch` | `switch` | `table.db_name = 0/1` | колонка |
| `filter_extend_time` | `time` | общая ветка | колонка |

Разбор кода: `lib/CRM/form/get_search_where.py:71,120,129,149,165,208`.

## Что происходит на этапах

| Тип | `/get-filters` конвертирует | фильтр рисуется на фронте | вырезается из карточки |
|---|---|---|---|
| `filter_extend_text` | да → `text` | да | **нет** (нет `orig_type`) |
| `filter_extend_select_values` | да → `select` | да | да (`orig_type`) |
| `filter_extend_select_from_table` | да → `select` | да | да (`orig_type`) |
| `filter_extend_date` | да → `date` | да | **нет** |
| `filter_extend_datetime` | нет | **нет** | **нет** |
| `filter_extend_checkbox` | нет | **нет** | **нет** |
| `filter_extend_switch` | нет | **нет** | **нет** |

Причины и обходы — [../19-known-gaps.md](../19-known-gaps.md).

## Пример с JOIN

```python
# project/__init__.py
'QUERY_SEARCH_TABLES': [
  {'t': 'project', 'a': 'wt'},
  {'t': 'domain',  'a': 'd', 'l': 'd.project_id=wt.project_id', 'lj': 1},
  {'t': 'template','a': 't', 'l': 'd.template_id=t.template_id', 'lj': 1},
  {'t': 'project_hosting', 'a': 'ph', 'l': 'ph.domain_id=d.domain_id', 'lj': 1},
],
'fields': [
  {'description': 'Домен', 'type': 'filter_extend_text', 'name': 'domain',
   'tablename': 'd', 'db_name': 'domain', 'filter_on': True, 'autocomplete': True},

  {'description': 'Хостинг выключен', 'type': 'filter_extend_checkbox',
   'name': 'disabled', 'tablename': 'ph', 'db_name': 'disabled'},

  {'description': 'Шаблон', 'type': 'filter_extend_select_from_table',
   'name': 'template_id', 'tablename': 't', 'table': 'template',
   'header_field': 'header', 'value_field': 'template_id',
   'db_name': 'template_id', 'filter_on': True},
],
```

- `tablename` **обязан** совпадать с `alias` из `QUERY_SEARCH_TABLES`.
- `db_name` — полноценное SQL-выражение по алиасу (можно `func:` и `group_concat`).
- Порядок фильтров задаётся `filter_on` (по возрастанию).
- В `get_filters` из копии поля вырезаются служебные ключи
  (`regexp_rules`, `tab`, `where`, `table_id`, …).

## Домены и punycode

Для доменных фильтров ставьте `'punycode': True`. Тогда:

- в поиске (AdminTable) и в `/autocomplete/<config>` кириллица и полный URL
  нормализуются в punycode (`prepare_search_domain`: срезаются `http(s)://`,
  `www.`, путь, затем `idna`);
- подсказки autocomplete и значение в списке выводятся обратно в юникоде
  (`domain_to_unicode`).

```python
{'description': 'Домен', 'type': 'filter_extend_text', 'name': 'domain',
 'filter_table': 'domain', 'tablename': 'd', 'db_name': 'domain',
 'punycode': True, 'filter_on': True, 'autocomplete': True}
```

Хелперы — `lib/CRM/form/idn.py`; обработка — `get_search_where.py`,
`routes/autocomplete.py`, `process_result_list.py`.

## См. также

- [../16-field-types-backend.md](../16-field-types-backend.md) — матрица
  обработки всех типов.
- [../10-lists-filters.md](../10-lists-filters.md) — списки и JOIN-ы.
- [../19-known-gaps.md](../19-known-gaps.md) — расхождения.
