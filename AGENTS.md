# AGENTS.md — CrmFreshBackend-python-async

Асинхронный JSON-бэкенд CRM на FastAPI (Python 3.12, `.venv`). Фронт — отдельное
Vue 3 приложение (`../CrmFreshFront-v3`). Текущая ветка — `async`.
Подробности — в `agent-doc/` (читай только нужный файл, не весь проект).

## Железные правила (действуют всегда)

- Запуск **только из корня репозитория** (`.venv/bin/uvicorn`), иначе сломается
  debug-обход авторизации: `lib/engine.py:9` захватывает `os.getcwd()`.
- Состояние запроса — только `request.state.engine` (`s`). **Никогда**
  `from lib.engine import s` и `form.s` (есть `form.request.state.engine`) —
  это небезопасный module-level глобал.
- Все хуки и обращения к БД — `async` (`await`). Sync-хук → `TypeError` → 500.
- `read_config` вызывается **только с `await` и `request=`**; при ошибке
  возвращает объект `error`, а не `Form`.
- Ошибки не передаются HTTP-кодом: ответ всегда `200`, неуспех — `success: 0`
  и непустой `errors`.
- Отступ **2 пробела**, комментарии и пользовательские строки — на русском.
- Не менять `AGENTS.md` и `agent-doc/` без просьбы; правки минимальны.

## Навигация по документации

| Файл | Когда читать |
|---|---|
| `agent-doc/00-overview.md` | общая карта папок, стек, мёртвый код, структура `configs/` и `conf_projects/` |
| `agent-doc/01-run-config.md` | запуск, env `config`, ключи `config_*.py`, debug-обход авторизации |
| `agent-doc/02-engine.md` | контракт `Engine`, `request.state`, cookies, заголовки, middleware |
| `agent-doc/03-forms.md` | `read_config`, схема `form`, события (`events.py`, `events_for_fields.py`) |
| `agent-doc/04-db.md` | `FreshDB`, `get_db`, сборка SQL, `exists_arg`, `out_error`, `func:` |
| `agent-doc/05-routes-map.md` | полная таблица всех роутов: префиксы, эндпоинты, назначение |
| `agent-doc/06-response-contract.md` | конверт ответа, типовой хендлер, правила ошибок |
| `agent-doc/07-core-routes.md` | детали ключевых роутов (`edit_form`, `get_result`, docpack, wysiwyg, ...) |
| `agent-doc/08-auth-cors-cookies.md` | логин/сессии, CORS, cookies, кросс-доменный логин |
| `agent-doc/09-svcms-manager.md` | **основной деплой**: контракт `request.state`, проект 5830, async-правила |
| `agent-doc/10-known-issues.md` | известные дефекты и «мёртвый код» — не чинить без нужды |
| `agent-doc/11-conventions-security.md` | соглашения кода и заметки по безопасности |
| `agent-doc/12-configs.md` | как составлять конфиги-инструменты: `form`, поля, события, добавление инструмента |

Как искать: задача про конкретный роут → `05-routes-map.md` → при необходимости
`07-core-routes.md`; задача про формы/поля → `03-forms.md` и `12-configs.md`;
про деплой svcms_manager → `09-svcms-manager.md`.

## Быстрый запуск

```bash
export config=config_svcms_manager && .venv/bin/uvicorn --reload --port=5000 --workers 1 main:app
```

Основной скрипт — `start/svcms_manager.sh`. Без env `config` приложение не
поднимется (`config.py` делает `quit()` на импорте). Тестов нет — проверка через
реальный uvicorn и `curl`.

## Инструкции для агентов

- Планирование (plan), исследование (explore), архитектура — локальная модель
  `openai/r1-coder` (endpoint `http://localhost:11434/v1`).
- Написание кода и мелкий багфикс — образ `rafw007/ornith-claude-coder:latest`.

## Output Language

- Output in Russian
- Generate all explanations, comments, and plans in Russian
