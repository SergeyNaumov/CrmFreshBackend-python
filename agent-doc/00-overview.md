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
- **Вне области правок** (отдельные деплои, не трогать): `configs/teleweb/**`,
  `configs/test/**`, `configs/beyeezy/**`, `configs/crimea/**` и их
  `config_*.py`. Глобал `s=Engine()` в `lib/engine.py` сохранён исключительно
  как legacy-шим для них.
- `conf_projects/project_5759/5782/5793/5794/5795` — переведены на async
  (2026-09-27), см. `10-known-issues.md`.
