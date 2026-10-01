# `multiconnect_old` — старый мультичекбокс (строка в поле)

Совместимость со старым Perl-типом `multicheckbox`. Набор опций задаётся
строкой `extended`, а выбранные значения хранятся **строкой** в колонке
основной таблицы (формат менять нельзя):

```
;key1;;key2;
```

| Атрибут | Смысл |
|---|---|
| `extended` | Описание опций: `key;подпись;key2;подпись2;...`. Подпись может содержать HTML (`<hr/>`, ссылки) |
| `name` | Колонка (например `project.options`) |
| `values` | Формируется бэкендом из `extended` (`lib/CRM/form/multiconnect_old.py:parse_extended`) |

```python
{
  'description': 'Опции проекта',
  'type': 'multiconnect_old',
  'name': 'options',
  'full_str': True,
  'not_filter': 1,
  'tab': 'opt',
  'extended': 'ex_links;использование собственных ссылок;'
              'site_redirect;Редиректы<hr/>;'
              'yandex_yml;включить catalog.yml;',
}
```

Как это работает:

- `lib/core.py` — тип добавлен в `check_list`, поэтому значение пишется в
  основную таблицу (`is_wt_field`).
- `lib/CRM/form/get_values.py` — `values` парсится из `extended`.
- `lib/CRM/form/multiconnect_old.py` — `parse_extended`, `split_value`, `join_value`.
- `routes/get_filters_routes.py` — тип не выводится в фильтры.
- Фронт: `src/components/fields/multiconnect_old.vue` (список чекбоксов,
  подписи через `v-html`), значение — строка `;key;`.

Хранилище остаётся совместимым со старыми сайтами (они читают ту же строку).
Пример — `configs/svcmsadmin/project` (поле `options`).
