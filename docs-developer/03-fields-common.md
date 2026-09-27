# 03. Поля: обязательные и общие атрибуты

Поле — это словарь в `form['fields']`. У каждого типа есть свои атрибуты
(см. [04-field-types.md](04-field-types.md)), но есть общий набор.

## Обязательные

| Атрибут | Смысл |
|---|---|
| `description` | Подпись поля |
| `type` | Тип (см. [04](04-field-types.md)); без `type` — ошибка загрузки |
| `name` | Имя поля = колонка в таблице (если не задан `db_name`) |

## Общие атрибуты

| Атрибут | Смысл |
|---|---|
| `value` | Значение по умолчанию для `new` |
| `values` | Список вариантов `[{'v':..,'d':..}]` для select/checkbox |
| `db_name` | Колонка в БД, если отличается от `name` |
| `read_only` | Только чтение (поле и его сохранение) |
| `not_process` | Не сохранять/не обрабатывать при update |
| `hide` | Скрыть поле (можно менять динамически из `before_code`/зависимостей) |
| `hide_field` | Для `text`: не рисовать сам контрол, но обработать |
| `required` | ⚠ **legacy** — в Python-бэкенде не реализовано; используйте `regexp_rules` |
| `unique` | ⚠ **legacy** — в Python-бэкенде не реализовано |
| `regexp_rules` | Пары `[regex, message]` (см. [07](07-validation-deps.md)) |
| `replace_rules` | Пары `[regex, replacement]` на фронте (см. [07](07-validation-deps.md)) |
| `before_code` | `def/async def(form, field)` — модификация поля перед рендером |
| `permissions` | `async def(form, field)` — права поля |
| `filter_on` | Показывать в фильтрах списка |
| `filter_code` | `async def(form, field, row)` — как выводить значение в списке |
| `not_filter` | Не выводить в фильтрах |
| `allready_out_on_result` | Уже выводится в результате (не дублировать) |
| `make_change_in_search` | Редактируемое поле прямо в списке |
| `tab` | Имя блока/вкладки (`cols`/`tabs`) |
| `width` | Ширина (CSS) |
| `style` | Инлайн-стиль контрола |
| `placeholder` | Плейсхолдер (text/in_ext_url) |
| `icon` | Иконка (для отдельных типов/кнопок) |
| `add_description` | Подпись-подсказка под полем |
| `before_html` / `after_html` | HTML до/после поля |
| `error_message` / `warning_message` | Сообщение об ошибке/предупреждении (можно ставить из `before_code`/зависимостей) |
| `not_description` | Не выводить `description` (полная строка) |
| `full_str` | Поле на всю ширину блока |
| `not_out_in_slide` | (для вложенных полей `1_to_m`) не выводить в «слайд» |
| `change_in_slide` | (для `1_to_m`) редактировать прямо в строке слайда |

## Раскладка на фронте (FormBlock)

Фронт (`src/components/EditForm/FormBlock.vue`) сам решает, как вывести поле:

- `is_only_field(field)` — «только контрол», без описания:
  - `checkbox`, `switch` (у них подпись — сам `label`), а также `read_only` `date`/`datetime`.
- `is_default_full_str(field)` — рендер полной строкой (описание сверху) для типов:
  `text`, `textarea`, `wysiwyg`, `checkbox`, `switch`, `select` (в него
  нормализуются `select_values`/`select_from_table`), `date`, `time`, `datetime`,
  `memo`, `file`, `password`, `1_to_m`, `multiconnect`, `time_table` и их
  `1_to_1_*`-вариантов. Переопределяется `full_str`.
- `is_default_not_description(field)` — **не** показывать `description` для всех типов,
  кроме: `wysiwyg`, `memo`, `1_to_m`, `password`, `file`, `datetime`, `code`
  (и `multiconnect`). Переопределяется `not_description`.

Остальные поля (не попавшие в full_str) выводятся двумя колонками: описание слева
(`md=2`), контрол справа (`md=10`). Скругления/отступы — из схемы (`--app-space-*`).

> Если поле ведёт себя «не так», как ожидается, смотрите сначала эти три функции —
> часто достаточно выставить `full_str` или `not_description`.

## Сообщения об ошибках/предупреждениях

- Бэк может положить `field['error_message']` / `field['warning_message']` из
  `before_code`/`ajax` — фронт выведет их сразу под контролом (класс `.err`/`.warn`).
- `regexp_rules` на фронте (`field_functions.js:check_fld`) ставят `error_message`
  автоматически при несоответствии.
- Формат ответа зависимостей: `['имя_поля', {'error': 'текст'}]` →
  фронт (`js/edit_form.js:apply_dep_to_field`) превращает в `error_message`.
  Для предупреждения — ключ `warning`. См. [07](07-validation-deps.md).
