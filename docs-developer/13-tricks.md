# 13. Каталог хитростей

Сборник приёмов «как сделать X». Каждый раздел — с якорем, чтобы можно было
найти нужное.

## Скрыть поле

### Статически
```python
{'description': 'Цена', 'type': 'text', 'name': 'price', 'hide': True}
```
Фронт не отрисует поле, но оно есть в форме.

### Динамически из зависимостей
```python
{
  'description': 'Акция', 'type': 'checkbox', 'name': 'action',
  'frontend': {
    'fields_dependence': '''
      v => { window.EditForm.get_field_by_name('price').hide = !v.action }
    '''
  }
}
{'description': 'Цена', 'type': 'text', 'name': 'price', 'hide': True}
```

### Из `before_code`
```python
async def hide_if_readonly(form, field):
    if form.read_only:
        field['hide'] = True
```

### `hide_field` (только для `text`)
Поле обрабатывается, но контрол не рисуется — удобно, если значение нужно
только для зависимостей/сохранения.

---

## Зависимые поля

### Локально (JS на фронте)
`field.frontend.fields_dependence` — строка `v => [...]`. См.
[07](07-validation-deps.md). Работает без сервера.

### Через сервер
`field.frontend.ajax = {'name': 'controller', 'timeout': 300}` + контроллер в
`ajax.py`. См. [09](09-ajax.md).

### Каскад
Изменения применяются каскадно: движок пересчитывает зависимые поля, пока не
стабилизируется (предохранитель 300 шагов).

---

## Валидация

### Регулярка + сообщение
```python
'regexp_rules': ['/^[0-9]*$/', 'Укажите целое число']
```

### Нормализация (только фронт)
```python
'replace_rules': ['/[^0-9]+/g', '']   # плоский список пар [rule, repl, ...]
```
> Формат — плоский список `[rule, replacement, rule, replacement, ...]`.

### Ошибка из `before_code`/ajax
Установите `field['error_message'] = 'текст'` (и `field['error'] = True`) — фронт
покажет под полем и заблокирует сохранение.

### Уникальность значения
Напишите проверку в `before_save` (или в ajax) и добавьте `form.errors`.

---

## Даты

```python
{'description': 'Дата', 'type': 'date', 'name': 'registered', 'empty_value': 'null'}
```
`empty_value: 'null'` сохраняет `NULL` вместо `'0000-00-00'`.

---

## Select-ы

### С деревом
```python
{'type': 'select_from_table', 'table': 'catalog',
 'header_field': 'header', 'value_field': 'id', 'tree_use': 1}
```

### Только выбор из списка
`'autocomplete': 1` — запрещает ввод произвольного значения.

### Кастомный список
- `query`: `'SELECT id v, header d FROM ... WHERE ...'`.
- `list`: готовый список (без запроса).
- `where`/`order`.

---

## Связи

### Inline-редактирование в `1_to_m`
- `change_in_slide: 1` у дочернего поля — правится прямо в слайде.
- `slide_code` — вычисляемое значение.
- `not_out_in_slide` — скрыть поле в слайде.

### Связь с полем связи (`multiconnect` + `subtype: 'table'`)
Добавляет доп. поля к самой связи (см. [05](05-relations.md)).

### Поле из отдельной таблицы (`1_to_1_*`)
`save_table` + `foreign_key` + `db_name`.

---

## Файлы

### Ресайзы и превью
```python
'resize': [
  {'file':'<%filename_without_ext%>_mini.<%ext%>', 'size':'156x117', 'quality':'100'},
],
'preview': '156x117'
```

### Вычисляемый `filedir` по проекту
В `__init__.py` заглушка `./files/project_[project_id]/good`, а в
`events.permissions` подстановка:
```python
async def permissions(form):
    pid = form.request.state.project['project_id']
    for f in form.fields:
        if f.get('filedir'):
            f['filedir'] = f['filedir'].replace('[project_id]', str(pid))
```

### Вычисляемый `work_table` по проекту
```python
form.work_table = f'struct_{pid}_news'
```

---

## wysiwyg

```python
{'description':'Описание','type':'wysiwyg','name':'body',
 'filedir':'./files/project_5830/good',
 'plugins':[{'type':'GPTAssist','set_value_button':'Отправить в описание'}]}
```

---

## JS на форме

```python
'javascript': {'edit_form': "alert('загружено')"},
'javascript_static': {'edit_form_static': ['/CrmFresh/.../edit_form.js']},
```
Внутри доступны `window.EditForm`, `window.bus`, `config`, `BackendBase`,
`BaseUrl`, функция `form.param(name)` печатает CGI-параметр.

---

## Скрытые/динамические поля из `events`

```python
async def permissions(form):
    form.add_field({'description':'Служебное','type':'text','name':'service'}, after='header')
    # или
    form.remove_field('unused')
```

---

## Список и фильтры

### Фильтр по умолчанию
`'default_find_filter': 'header,anons'` (строка со запятыми → список).

### Своё отображение значения в списке
```python
async def status_title(form, field, row):
    return 'Активен' if row.get('enabled') else 'Выключен'
# 'filter_code': status_title
```

### JOIN только когда нужно
```python
{'t':'vendor','alias':'v','l':'wt.vendor_id=v.id','lj':1,'for_fields':['vendor_id']}
```
Таблица подключится, только если `vendor_id` участвует в фильтре.

### Массовые действия
`'search_multi_action': search_multi_action_list` (`set_all_value_field`,
`change_price`, `delete`). См. [10](10-lists-filters.md).

---

## Дерево и галерея

- `changed_in_tree: True` — редактирование модалкой.
- `view_type: 'gallery'` + `photo_for_gallery` + `cols` — галерея.
- `sort` — разрешает перетаскивание (дерево/галерея).
- `tree_select_header_query` — свой заголовок ветки.
- `max_level` — ограничить вложенность.

См. [11](11-tree-gallery.md).

---

## Права

- Форма: `events['permissions'] = async def(form)`.
- Поле: `field['permissions'] = async def(form, field)`.
- Быстро: `read_only`, `not_create`, `not_edit`, `make_delete`.

---

## Отладка

- `form.pre(value)` — дамп в `form.log` (виден в ответе).
- `'explain': 1` — SQL поиска.
- `'explain': 1` в `db.save`/`db.query` (через вызовы) — детальнее.

---

## «Грабли»

| Симптом | Причина |
|---|---|
| Обращение к `form.s` падает/путается | Глобальный engine запрещён, используйте `form.request.state.engine` |
| Поле не выводится | `hide`, либо `tab` не совпадает с блоками (`cols`/`tabs`) |
| `after_update_code` на поле не срабатывает | Баг в `all_configs.py:129` (склейка имён) |
| `required`/`unique` ничего не делают | Не реализованы в Python-бэкенде (legacy) |
| Мульти-select не работает | Атрибут называется `multilpe` (опечатка в коде), не `multiple` |
| Галерея не включается | Бэк ждёт `gallery`/`galery` и `photo_for_gallery`; проверьте написание |
| Фото обрезано | Это `object-fit`; для галереи нужен `contain` (уже так) |
| Событие не вызывается | Оно должно быть в `events.py` (словарь заменяет дефолтный целиком) |
| Ошибка `async` | Все события формы/поля должны быть `async def` |
