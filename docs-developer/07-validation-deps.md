# 07. Валидация и зависимости полей

## `regexp_rules` — регулярки

Пары `[regex, message]` (в списке идут парами). Проверяются и на бэке, и на фронте.

```python
'anons': {
  'description': 'Анонс', 'type': 'textarea', 'name': 'anons',
  'regexp_rules': [
      '/^.{3,255}$/', 'длина анонса должна быть не менее 3 символов',
  ],
}
```

### Бэкенд (`lib/check_field.py`)

- Формат: `/pattern/mods`, где `mods` может содержать `i` (ignore case).
- Используется `re.match` (проверка с начала строки).
- Вызывается в `Form.check()` перед сохранением, только для полей, попавших в
  `new_values`; при несовпадении добавляет `message` в `form.errors`.

### Фронтенд (`fields/field_functions.js:check_fld`)

- Применяет `replace_rules`, затем `regexp_rules`.
- При несовпадении ставит `field.error_message` (и `field.error = true`), что
  блокирует сохранение (`calc_values` → `disabled_form`) и выводит текст под полем.
- `to_regex` понимает и строку `/.../mods`, и `RegExp`.

## `replace_rules` — нормализация (только фронт)

Пары `[regex, replacement]`. Выполняется при вводе, изменяя значение поля.
Пример из `configs/crimea/manager/fields.py`:

```python
{'description': 'Телефон', 'type': 'text', 'name': 'phone',
 'replace_rules': [
     '/[^0-9]+/g', '',          # убрать всё, кроме цифр
 ]}
```

> `replace_rules` обрабатывает фронт (`field_functions.js`). Бэкенд его не применяет.

## Зависимости полей (`field.frontend.fields_dependence`)

Строка с JS-функцией `v => [...]`, где `v` — объект значений формы
(`form.values`). Возвращает «массив изменений» (см. формат ниже).
Компилируется и исполняется движком (`src/components/js/edit_form.js`).

```python
{
  'description': 'Акция', 'type': 'checkbox', 'name': 'action',
  'frontend': {
    'fields_dependence': '''
      v=>{
        window.EditForm.get_field_by_name('price').hide = !v.action
      }
    '''
  }
}
```

Когда поле изменилось, движок вызывает его `fields_dependence`. Изменения
применяются к полям формы и каскадно пересчитываются (с защитой от циклов,
`ENGINE_MAX_STEPS = 300`).

## `field.frontend.ajax` — серверные зависимости

Поле может запросить пересчёт на сервере:

```python
{
  'description': 'Название', 'type': 'text', 'name': 'header',
  'frontend': {'ajax': {'name': 'in_ext_url', 'timeout': 600}},
}
```

- `name` — имя ajax-контроллера (`/ajax/<config>/<name>`, см. [09](09-ajax.md)).
- `timeout` — задержка (мс) перед запросом (по умолчанию `600`).
- Запрос: `POST /ajax/<config>/<name>` c `{values, id}`.
- Кэш одинаковых запросов — 1 с (`AJAX_CACHE_TTL`), плюс дедупликация «в полёте».

## Формат ответа зависимостей (и ajax, и fields_dependence)

Плоский массив пар `['имя_поля', {...}, 'имя_поля', {...}]`.
Поддерживаемые ключи объекта:

| Ключ | Действие |
|---|---|
| `value` | подставить значение |
| `instead_of_empty` | подставить, только если поле пустое (`begin_value`) |
| `values` | заменить список вариантов (для select) |
| `hide` | показать/скрыть |
| `error` | установить `error_message` (+ `error=true`) |
| `warning` | установить `warning_message` |
| `before_html` / `after_html` | заменить HTML вокруг поля |
| `description` | заменить подпись |
| `fields` | (для `1_to_m`) заменить список дочерних полей |
| `jscode` | произвольный JS, исполняется через `eval` |

Пример ответа ajax:

```python
return [
  'in_ext_url', {'value': url.lower(), 'error': url_error},
  'header',     {'error': 'скорректируйте url'},
]
```

## `before_code`

- Форма: `events.py` → `events = {'before_code': func}`.
- Поле: `before_code` прямо в словаре поля или в `events_for_fields.py`.
- Вызывается после `get_values()` и `permissions()` (`run_all_before_code`).
- Может быть sync или async; принимает `(form, field)`.
- **Если вернуть новый словарь поля** с другим `name` — форма заменит поле и
  обновит `fields_hash` (`lib/CRM/form/__init__.py:221-235`).

```python
async def before_code_top(form, field):
    if form.action == 'new':
        field['value'] = 1

{'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled',
 'before_code': before_code_top}
```

## `permissions`

Права динамически (по ролям/условиям). Форма — `events['permissions']`;
поле — `field['permissions'] = async def(form, field)`. Вызывается из
`read_config` до `before_code`.

## `not_process`, `read_only`, `hide`

- `read_only` — не редактируется, не сохраняется.
- `not_process` — не участвует в обработке (`save_form`, поиск).
- `hide` — скрыто; удобно включать/выключать из `before_code` или зависимостей
  (см. пример с `price.hide`).
