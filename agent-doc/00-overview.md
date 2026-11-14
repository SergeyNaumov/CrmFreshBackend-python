# Обзор проекта

Асинхронный JSON-бэкенд CRM на FastAPI. Фронтенд — отдельное приложение
Vue 3 + Vuetify (`../CrmFreshFront-v3`), бэкенд отдаёт только JSON.
Свои HTML-шаблоны отдаются редко через `lib/CRM/form/template.py`.

- Текущая ветка — `async`, старая — `v1`.
- Python 3.12, виртуальное окружение `.venv` в корне.
- Типовых аннотаций почти нет, отступ **2 пробела** (детали — `11-conventions-security.md`).

## Карта папок

| Путь | Назначение |
|---|---|
| `main.py` | точка входа: FastAPI, CORS, startup-пул, middleware `for_all_requests` |
| `config.py` | загрузка конфига по env `config` |
| `config_*.py` | настройки конкретных деплоев |
| `routes/` | HTTP-роуты (карта — `05-routes-map.md`) |
| `configs/<проект>/<инструмент>/` | `form = {...}` — схема экрана/инструмента |
| `conf_projects/project_<id>/` | пер-проектные переопределения (SV-CMS) |
| `lib/engine.py` | класс `Engine` — контекст запроса (`02-engine.md`) |
| `lib/all_configs.py` | `read_config()` — фабрика `Form` (`03-forms.md`) |
| `lib/session.py` | логин, сессии, права (`08-auth-cors-cookies.md`) |
| `lib/core.py`, `lib/core_crm.py` | утилиты и CRM-логика |
| `lib/CRM/form/` | класс `Form` + сохранение, файлы, поиск, шаблоны |
| `db/` | `FreshDB` (async, aiomysql) и `FreshDBSync` (sync, pymysql) (`04-db.md`) |
| `files/` | загруженные файлы (в gitignore), раздаёт nginx, не FastAPI |
| `settings/nginx_section.txt` | пример nginx-конфига (справка) |
| `daemons/`, `dbd_creator/`, `dbf_daemon/` | фоновые задачи и выгрузка в XBase |
| `start/*.sh` | скрипты запуска под конкретные деплои |

## Универсальный конструктор CRM (мультитенантность)

Репо — **платформа CRM «конструктор»**, обслуживающая много тенантов:
`config_svcms_manager.py` (менеджер DS-сайтов), `config_svcms_admin.py`
(админка svcms), `config_beyeezy/crimea/teleweb/trade/test` и др. Общих
дефолтов нет: каждый деплой — свой `config_*.py` (БД, `config_folder`,
фичи).

**Правило изоляции тенантов.** Специфика тенанта — только в его неймспейсах:
- роуты: `routes/svcms/`, `routes/svcmsadmin/` (generic: `routes/edit_form*`,
  `ajax.py`, `admin_tree*`, `parser_excel/`, `documentation_routes.py` —
  тенант-нейтральны);
- либы: `lib/svcmsmanager/`; общее ядро — `lib/CRM/**`, `lib/engine.py`,
  `db/`, `main.py`;
- конфиги инструментов: `configs/<config_folder>/` (для svcms —
  `configs/svcmsmanager/`, для DS-конфигов — симлинки на канон в движке);
  пер-проектные переопределения — `conf_projects/project_<id>/`;
- миграции тенанта: `db/migrate_ds_*`.

В общем ядре нельзя: имён таблиц тенанта (`ds_*`), хардкодов проектов
(`5837`, доменов) и `if`-веток по тенанту. Тенант-специфику — через
конфиг/field-атрибуты (`params_table`, `values_table`, `foreign_key`…)
или через механизмы ядра (`frontend.ajax`, `events`, `plugins`).

Примеры правильного использования: меню DS — `routes/svcms/left_menu.py`;
текстовые блоки — `lib/svcmsmanager/text_blocks.py` + `configs/svcmsmanager/ds_text_block`;
prefill характеристик — конфиг `ds_good` + общий `frontend.ajax`.
Вопрос перед правкой: «это фича тенанта или платформы?» — платформа обязана
работать у всех тенантов.

Гейт монтирования: `routes/__init__.py` подключает `/svcms` и `/svcmsadmin`
только если `config['features']['ds']` истинно (флаг тенанта; прод-конфиг
`/var/www/svcms/manager/backend/config.py` тоже). Плюс scope-проверки уже
внутри: `page_constructor` сверяет `domain_id` с проектом менеджерской
сессии (`_project_scope_error`) — чужой домен = отказ (и на GET тоже).

## Безопасность (пентест 2026-11)

- Права админа — `lib/authz.py` (`require_permission('admin_main')`);
  применяется в `routes/svcmsadmin/*` и `/password`. Продеты таблиц
  `admin_permissions`/`permissions` — иначе гейт даёт 403.
- 500 без трейсбека: `main.py` — `FastAPI(debug=False)` + обработчики
  `Exception`/`PermissionError`; стек — только в `debug_mode` движка.
- CORS: петлевые origin (dev vite) — только при `config['cors_allow_local']`.
- В SQL значения — параметрами; идентификаторы (parent_id/id в
  `admin_tree`, values в `autocomplete`, multiconnect) — только числа.
- Загрузки: имя файла — `os.path.basename` (wysiwyg), путь — только внутри
  `files_dir` (normpath/chroot).
- Rate-limit логина: `session_create` пишет неудачи в `session_fails_table`
  (`manager_session_fails`/`admin_session_fails`), порог — из аргументов
  `/login` (3/час на логин, 20/час на IP); старые метки чистятся. TTL сессии —
  `auth['session_ttl']` (в конфигах 30 суток).

## Мёртвый / пустой код

- `models/` — нерабочий Peewee, нигде не импортируется, `peewee` нет в зависимостях.
- `confsvcmsmanager/` — пустая папка, актуальный аналог — `configs/svcmsmanager/`.
- `tasks/` — пустая, под Celery (сам Celery не используется).
- `routes/core_routes/login.py` — не импортируется, мёртвый.
- `routes/beeline/` — создан, но не подключён.

## Инструменты (`configs/`)

`configs/<проект>/<инструмент>/` — «экран» CRM: списки, карточки, справочники.
Проекты: `beyeezy` (18), `crimea` (13), `teleweb` (15), `test` (6),
`svcmsmanager` (9). Загрузка — `lib/all_configs.py:load_form_from_dir`
через `importlib.import_module(f"{config_folder_as_module}.{config}")`.

Тяжёлая логика вынесена из роутов в соседние модули:
`routes/edit_form/`, `routes/get_result/`, `routes/docpack_routes/`,
`routes/parser_excel/`.

## Зона текущей работы

Основной деплой — `config_svcms_manager` (см. `09-svcms-manager.md`).

### Границы поддерживаемого кода

- **В работе**: `routes/`, `lib/`, `db/`, `main.py`, `config_svcms_manager.py`,
  `configs/svcmsmanager/**`, `conf_projects/project_5830/**`.
- **Проект 5837** (CMS-конструктор `t1`, домен `demo1.digitalstrateg.ru`):
  `conf_projects/project_5837/**` — инструменты `ds_*`; эталон — проект 5830.
  «Золотые» копии инструментов живут в `/var/www/svcms-async/manager/backend/conf/`
  (движок сайта читает их через `sites/lib/dbl/load_struct.py`:
  `conf_projects/project_5837/` → `conf/`; в manager считаются как
  `configs/svcmsmanager` или данные из БД). Конфиги-симлинки
  `configs/svcmsmanager/ds_*` указывают туда же.
  Соглашения конструкторных конфигов — `12-configs.md`.
- **Вне области правок** (отдельные деплои, не трогать): `configs/teleweb/**`,
  `configs/test/**`, `configs/beyeezy/**`, `configs/crimea/**` и их
  `config_*.py`. Глобал `s=Engine()` в `lib/engine.py` сохранён исключительно
  как legacy-шим для них.
- `conf_projects/project_5759/5782/5793/5794/5795` — переведены на async
  (2026-09-27), см. `10-known-issues.md`.
