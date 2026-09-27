# 09. Ajax-контроллеры

Ajax-контроллеры обслуживают серверные зависимости полей
(`field.frontend.ajax`), кнопки (`field-buttons`) и внешние вызовы.

## Как подключить

1. В папке инструмента создайте `ajax.py` со словарём `ajax = {...}`.
2. Присвойте его форме в `events.py` (обычно в `permissions`):
   `from .ajax import ajax` и `form.ajax = ajax`.
   Либо задайте словарь прямо в `__init__.py`: `'ajax': {...}`.

> Автозагрузки `ajax.py` нет: `load_form_from_dir` читает только `events.py` и
> `events_for_fields.py`. Поэтому `form.ajax` выставляется вручную.

## Формат контроллера

```python
# ajax.py
async def gen_slug(form, values):
    return ['slug', {'value': make_slug(values.get('header'))}]

def echo_title(form, values):        # sync тоже поддерживается
    return ['slug', {'value': values.get('title')}]

ajax = {
    'gen_slug': gen_slug,
    'echo_title': echo_title,
}
```

- Первый аргумент — `form`, второй — `values` (данные из запроса: `form.R['values']`).
- Возврат — либо `None`, либо массив изменений в формате зависимостей:
  `['имя_поля', {'value': ..., 'error': ..., 'hide': ...}, ...]`
  (см. [07-validation-deps.md](07-validation-deps.md)).
- Может быть `async` или обычной функцией — роут сам делает `await` при
  необходимости (`routes/ajax.py:run_ajax`).

## Эндпоинт

```
GET|POST /ajax/{config}/{ajax_name}
тело: { "values": {...}, "id": <id> }
ответ: { "success": true, "errors": [], "result": [ ... ] }
```

Фронт вызывает его:
- из `field.frontend.ajax` (после изменения поля, с задержкой `timeout`);
- из кнопок поля (`frontend/buttons.vue` → `button.ajax`).

## Пример реального контроллера

`conf_projects/project_5830/news/ajax.py`:

```python
from transliterate import translit

async def exists_url(form, url):
    project_id = form.request.state.project['project_id']
    where = 'where ieu.ext_url=%s'
    if form.id:
        where += f" AND wt.id<>{form.id}"
    exists = await form.db.query(
        query=f"""
          select wt.id, wt.header, url
          from {form.work_table} wt
          JOIN in_ext_url ieu ON ieu.project_id={project_id} and ieu.in_url=concat('/news/',wt.id)
          {where}
        """,
        values=[url], onerow=1,
    )
    return f"url {url} уже занят" if exists else ''

async def in_ext_url(form, values):
    project_id = form.request.state.project['project_id']
    url = ''
    if header := values.get('header'):
        slug = translit(header, 'ru', reversed=True)
        slug = re.sub(r"[^a-zA-Z0-9]+", '-', slug).strip('-').lower()
        url = f"/news/{slug}"
    err = await exists_url(form, url)
    return ['in_ext_url', {'value': url.lower(), 'error': err}]

ajax = {'in_ext_url': in_ext_url}
```

## Хитрости

- В `values` приходят **все** значения формы (не только изменившееся поле).
- `form.id` доступен (передаётся из карточки) — удобно для проверок уникальности.
- Контроллер может вернуть `[]` — «ничего не менять».
- Ошибку удобно отдавать через `{'error': 'текст'}` у целевого поля — фронт
  покажет её под полем и заблокирует сохранение.
- Плагин `InExtUrl` сам регистрирует ajax-контроллер `in_ext_url`
  (`lib/CRM/plugins/InExtUrl.py`), не нужно писать его руками.
