# Типы полей — по одному файлу на тип

Полный список типов с атрибутами, примерами и особенностями. Общие атрибуты —
в [../03-fields-common.md](../03-fields-common.md); краткий каталог —
в [../04-field-types.md](../04-field-types.md).

## Текстовые

| Тип | Документ |
|---|---|
| `text` | [text.md](text.md) |
| `textarea` | [textarea.md](textarea.md) |
| `wysiwyg` | [wysiwyg.md](wysiwyg.md) |

## Логические

| Тип | Документ |
|---|---|
| `checkbox` | [checkbox.md](checkbox.md) |
| `switch` | [switch.md](switch.md) |

## Списки/выбор

| Тип | Документ |
|---|---|
| `select_values` | [select_values.md](select_values.md) |
| `select_from_table` | [select_from_table.md](select_from_table.md) |
| `select` | внутренний тип, см. [select_values.md](select_values.md) и [select_from_table.md](select_from_table.md) |

## Даты и время

| Тип | Документ |
|---|---|
| `date` | [date.md](date.md) |
| `datetime` | [datetime.md](datetime.md) |
| `time` | [time.md](time.md) |
| `daymon` | [daymon.md](daymon.md) |
| `yearmon` | [yearmon.md](yearmon.md) |

## Пароль

| Тип | Документ |
|---|---|
| `password` | [password.md](password.md) |

## Файлы

| Тип | Документ |
|---|---|
| `file` | [file.md](file.md) |

## Связи

| Тип | Документ |
|---|---|
| `1_to_m` | [1_to_m.md](1_to_m.md) |
| `multiconnect` | [multiconnect.md](multiconnect.md) |
| `multiconnect_old` | [multiconnect_old.md](multiconnect_old.md) |
| `1_to_1_*` | [1_to_1.md](1_to_1.md) |

## Прочие

| Тип | Документ |
|---|---|
| `font-awesome` | [font-awesome.md](font-awesome.md) |
| `in_ext_url` | [in_ext_url.md](in_ext_url.md) |
| `code` | [code.md](code.md) |
| `header` | [header.md](header.md) |
| `component` | [component.md](component.md) |
| `memo` | [memo.md](memo.md) |
| `docpack` | [docpack.md](docpack.md) |
| `table` | [table.md](table.md) |
| `time_table` | [time_table.md](time_table.md) |
| `accordion` | [accordion.md](accordion.md) |
| `chart` | [chart.md](chart.md) |
| `GPTAssist` | [gptassist.md](gptassist.md) (плагин, не тип) |

## Только для фильтров списка

| Тип | Документ |
|---|---|
| `filter_extend_*` | [filter_extend.md](filter_extend.md) |

## Массовые действия

| Тип | Документ |
|---|---|
| `set_all_value_field`, `change_price`, `delete` | [multiaction.md](multiaction.md) |

## Легаси

| Тип | Примечание |
|---|---|
| `enabled` | Встречается в старых конфигах; отдельной обработки нет — используйте `checkbox` |
| `required`, `unique` (атрибуты) | Не реализованы в Python-бэкенде |
