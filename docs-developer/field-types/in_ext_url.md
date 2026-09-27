# `in_ext_url` — ЧПУ

Поле «человекопонятный URL» (таблица `in_ext_url`). Обычно не пишется вручную,
а создаётся плагином `InExtUrl`. Бэкенд: `lib/CRM/plugins/InExtUrl.py`,
`lib/CRM/form/save_in_ext_url.py`. Фронт: `src/components/fields/in_ext_url.vue`.

## Атрибуты поля

| Атрибут | Смысл |
|---|---|
| `name` | обычно `in_ext_url` |
| `description` | подпись (по умолчанию `url`) |
| `in_url` | шаблон «внутреннего» URL, напр. `/news/<%id%>` |
| `foreign_key`, `foreign_key_value` | скоуп (обычно `project_id`) |
| `read_only`, `hide`, `style` | состояние |
| `add_description`, `before_html`, `after_html` | оформление |

## Параметры плагина `InExtUrl(form, {...})`

| Параметр | Смысл |
|---|---|
| `dependence_field` | поле, из которого генерируется ЧПУ (напр. `header`) |
| `in_url` | внутренний URL-шаблон (`<%id%>`) |
| `url_prefix` | префикс ЧПУ (напр. `/news/`) |
| `ajax` | имя ajax-контроллера (обычно `in_ext_url`) |
| `after_field` | вставить поле после указанного |
| `tab` | блок/вкладка |
| `foreign_key`, `foreign_key_value` | скоуп |

## Пример (в `events.py`)

```python
from .ajax import ajax
from lib.CRM.plugins.InExtUrl import InExtUrl

async def permissions(form):
    project_id = form.request.state.project['project_id']
    await InExtUrl(form, {
        'foreign_key': 'project_id', 'foreign_key_value': project_id,
        'dependence_field': 'header',
        'in_url': '/news/<%id%>',
        'after_field': 'header',
        'url_prefix': '/news/',
        'ajax': 'in_ext_url',
        'tab': 'promo',
    })
    form.work_table = f'struct_{project_id}_news'
    form.ajax = ajax

events = {'permissions': permissions}
```

## Особенности

- ЧПУ генерируется транслитерацией `dependence_field` и проверкой уникальности
  (`in_ext_url.ext_url`).
- Сохранение — в `in_ext_url` по ключу `in_url` (`save_in_ext_url.py`).
- Поддерживает `foreign_key`/`foreign_key_value` для разделения ЧПУ по проектам.
- Сам контроллер `in_ext_url` регистрируется плагином — писать его не нужно
  (при необходимости можно переопределить в `ajax.py`).
