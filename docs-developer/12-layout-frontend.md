# 12. Раскладка и рендеринг на фронте

Фронт получает от `/edit-form/{config}` (см. `routes/edit_form/process_edit_form.py`):

```
action, title, success, errors, fields, id, log,
read_only, wide_form, cols, tabs, config,
javascript, javascript_static, redirect
```

## Колонки и блоки (`cols`)

```python
'cols': [
    [   # колонка 1
        {'description': 'SEO',      'name': 'promo', 'hide': True},
        {'description': 'Основное', 'name': 'main',  'hide': False},
    ],
    [   # колонка 2
        {'description': 'Фотогалерея', 'name': 'gal',  'hide': False},
        {'description': 'Описание',    'name': 'desc', 'hide': False},
    ],
],
```

- Внешний список — колонки (делятся поровну).
- Внутри — блоки (карточки с заголовком и сворачиванием).
- `hide`: `True` — блок свёрнут по умолчанию.
- `on_show`: JS-строка, исполняется при раскрытии блока (`block_toggle`).
- Поле попадает в блок через `tab: 'main'`.

## Вкладки (`tabs`)

```python
'tabs': [
    {'name': 'main', 'description': 'Основное'},
    {'name': 'promo', 'description': 'SEO'},
],
```

Поле привязывается к вкладке через `tab: 'main'`. Если заданы и `cols`, и
`tabs`, фронт сначала строит колонки/блоки (`FormBody.vue`).

## Если ни `cols`, ни `tabs`

Все поля рендерятся одним блоком.

## `wide_form`

Широкая карточка без ограничения `960px` (класс `container_fluid`).

## Атрибуты поля, влияющие на вид (сводка)

| Атрибут | Эффект |
|---|---|
| `full_str` | Поле на всю ширину блока (описание сверху) |
| `not_description` | Не выводить `description` |
| `hide` | Скрыть поле |
| `hide_field` | (text) не рисовать контрол |
| `wide` | Широкое поле |
| `style` | Инлайн-стиль контрола (или список URL CSS для wysiwyg) |
| `tab` | Блок/вкладка |
| `add_description` | Текст-подсказка под полем |
| `before_html` / `after_html` | HTML до/после поля |
| `error_message` / `warning_message` | Сообщения (красный/оранжевый) под полем |
| `background_color` | Цвет фона (select) |

Подробнее о логике «только контрол / полная строка / без описания» —
[03-fields-common.md](03-fields-common.md#раскладка-на-фронте-formblock).

## JavaScript на форме

- `javascript.edit_form` — JS-строка, исполняется через `eval` после загрузки
  карточки (`EditForm.vue`).
- `javascript.admin_table` — то же для таблицы.
- `javascript.find_objects` — для поиска.
- `javascript_static.edit_form` — список URL внешних скриптов, подключаются
  в `<head>`.

```python
'javascript': {
    'edit_form': "console.log('форма загружена')",
},
'javascript_static': {
    'edit_form_static': ['/CrmFresh/trade/users_card/edit_form.js'],
},
```

> Это `eval`-точки. В них доступны глобалы `window.EditForm`, `window.bus`,
> `config`, `BackendBase`, `BaseUrl`.

## `redirect` и `card_format`

- `redirect` — после `GET /edit-form` бэк вернёт `redirect`, и фронт уйдёт по
  URL (используется для перенаправлений).
- `card_format: 'old'` — ссылка на старую карточку `/edit_form.pl?...`
  (в `get_edit_link`).

## Модалка `changed_in_tree`

В дереве при `changed_in_tree: true` клик открывает `AdminTree/FormInBranch.vue`
— это тот же form-engine (`form_controller.js` + `FormBody.vue`), но в диалоге.
Поля, события, зависимости работают так же, как в `EditForm`.

## Хитрости

- Один и тот же блок можно переиспользовать в разных колонках — достаточно
  сослаться на `tab` с тем же `name`.
- `on_show` удобно использовать для ленивой подгрузки (например, вызвать
  `window.EditForm`-метод).
- Если поле «пропало» — проверьте `hide`/`tab`: поле с `tab`, которого нет ни в
  одном блоке, не отрисуется в блочном режиме (в одно-блочном режиме
  отрисуется).
