# Таблицы конструктора страниц

Бэкенд: `routes/svcmsadmin/page_constructor/`. Роут: `svcmsadmin/page-constructor`. Привязка — `domain_id` (не `template_id`); набор страниц и настройки хранятся отдельно для каждого домена из таблицы `domain`.

## Файлы

| Файл | Назначение |
|---|---|
| `__init__.py` | 15 эндпоинтов конструктора, чтение/запись всех таблиц ниже |
| `domain_migration.sql` | DDL новых таблиц + перенос данных из `template_*` (выполняется один раз) |
| `base_pages.json` | сид справочника `template_pages_base` (19 базовых страниц) |
| `structure_migration.sql` | старый ALTER `template_constructor` (до переезда на `domain_id`) |

## Таблицы

### `domain_page` — страницы домена
| Поле | Тип | Смысл |
|---|---|---|
| `id` | int unsigned AI | PK |
| `domain_id` | int, FK→`domain.domain_id` | владелец; ON DELETE CASCADE |
| `url` | varchar(200) | адрес страницы, уникален в паре с `domain_id` (`domain_id_url`) |
| `header` | varchar(255) | название страницы в списке |
| `blocks` | mediumtext | JSON формата v2: `{schema:"svcms.page_blocks", version:2, blocks:[…]}` |

### `domain_constructor` — тема и структура домена (1 строка на домен)
| Поле | Тип | Смысл |
|---|---|---|
| `domain_id` | int, PK, FK→`domain` | домен |
| `color` / `style` / `layout` / `font` | varchar(100) | имена выбранных схем (ссылки на `domain_theme_*`) |
| `color_css` … `font_css` | mediumtext | инлайновый CSS оси; если NULL — берётся из таблицы схем |
| `header_blocks` | mediumtext | JSON блока `header` — шапка, общая для всех страниц домена |
| `footer_blocks` | mediumtext | JSON блока `footer` — подвал |
| `updated` | datetime | авто |

Строки может не быть — тогда `GET /theme/<domain_id>` отдаёт дефолты (`digitalstrateg`/`soft`/`standard`/`inter`), а `/init` создаёт её при первом сохранении.

### `domain_theme_color`, `domain_theme_style`, `domain_theme_layout`, `domain_theme_font` — схемы тем
Одинаковая структура, различаются осью.

| Поле | Тип | Смысл |
|---|---|---|
| `domain_id` | int, часть PK | `0` — общий пресет для всех доменов; `>0` — индивидуальная схема домена |
| `header` | varchar(100), часть PK | идентификатор схемы (вместо прежнего `name`) |
| `label` | varchar(255) | подпись в селекте |
| `short` | varchar(500) | краткое описание под селектом |
| `descr` | text | описание |
| `css` | mediumtext | полный CSS оси |
| `sort` | int | порядок в списке |
| `is_default` | tinyint(1) | схема по умолчанию для оси |
| `is_custom` | tinyint(1) | 1 — созданная в UI схема (только такие удаляются) |
| `updated` | datetime | авто |

Правила выбора схем доменом: индивидуальная (`domain_id=<домен>`) приоритетнее одноимённой общей; общие схемы не перетираются доменом — индивидуальный заводит свою копию (чекбокс «Общая схема» в `ThemeTool` пишет в `domain_id=0`). `DELETE /theme-schemes/<axis>/<name>/delete` работает только по `domain_id>0` и `is_custom=1`.

### `template_pages_base` — справочник базовых страниц (не переносится)
`url, header, sort, blocks`. Общий для всех доменов. `POST /base-pages` копирует строки в `domain_page` конкретного домена, уже существующие по `url` пропускает.

### Старые таблицы (только чтение, на удаление)
`template_page`, `template_constructor`, `template_theme_color/style/layout/font` — предыдущая привязка к `template_id`. Код конструктора их больше не читает; удаляются после приёмки отдельным шагом. `template` (папка/шапка сайта) нужна: `/init` берёт `folder` через `JOIN domain → template` и отдаёт его как `templateBase`.

## Как это связано

```
domain (domain_id) ──FK──> domain_page       страницы домена
      │                        │
      └──FK──> domain_constructor  тема + шапка/подвал
                   │  color/style/layout/font (имена)
                   └──> domain_theme_*  CSS схем (общие domain_id=0 + индивидуальные)

template (template_id) ──JOIN по domain.template_id──> folder для превью
template_pages_base ──копирование──> domain_page (кнопка «Базовый набор»)
```