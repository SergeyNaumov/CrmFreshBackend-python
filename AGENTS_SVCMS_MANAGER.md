# AGENTS.md — svcms_manager (путь «менеджер проектов»)

Кратко по деплою `config_svcms_manager`. Общее по проекту — в `AGENTS.md`.

## Контракт request state (обязателен здесь)

Всё состояние запроса живёт в `request.state` — никаких модульных глобалов,
`Engine` создаётся на каждый запрос (`main.py:48`).

| Источник | Что брать |
|---|---|
| `request.state.engine` | объект `Engine` (имя в роутах — `s`) |
| `request.state.engine.db` | асинхронный MySQL (aiomysql) |
| `request.state.manager` | менеджер (после `after_create_engine`; вся файловая логика читает `manager['files_dir']`/`manager['files_dir_web']`) |
| `request.state.project['project_id']` | ID проекта (домен `dev-crm.test` → `5830`) |
| `request.state.project['template_id']` | шаблон редактора |

**Запрещено в контуре svcms_manager:**
- `from lib.engine import s` — глобал из `lib/engine.py:131`. В роутах удалён.
- `form.manager` — alias из `lib/all_configs.py:238` (костыль на время миграции
  других конфигов). Читать `form.request.state.manager`.
- `form.s.project_id`, `s.project_id`, `form.s.template_id`. Только
  `form.request.state.project[...]`.
- `db.get_db()` / `from db import db` — это `None`/мемоизованный синглтон,
  не process-independent. Только `request.state.engine.db`.

## Асинхронность

- Всё события БД и хуки — `async def`. `lib/CRM/form/run_event.py` всегда делает
  `await event(form)`; sync-функция → `TypeError` и 500 (поймать невозможно —
  ловится только `AttributeError`).
- Все `form.db.*` и помощисточники (например модуль `InExtUrl`) вызываются
  только через `await`, включая вложенные (например `exists_url()` в
  `conf_projects/project_5830/*/ajax.py`).

## Карта живого кода

- `config_svcms_manager.py:20` — `after_create_engine` резолвит проект по Host:
  `dev-crm.test` → project_id 5830, заполняет `request.state.project`,
  `request.state.manager` (files_dir/files_dir_web).
- `configs/svcmsmanager/config_wysiwyg.py` — WYSIWYG options/hooks, project_id
  из request state. Импортируется напрямую (не через `config_folder`).
- `configs/svcmsmanager/gptassist_rules.py` — GPT-ассистент, rules через
  `request.state.engine`. Вызывается из `routes/gptassist/__init__.py`.
- `conf_projects/project_5830/<инструмент>/` — конфиги проекта 5830
  (`good`, `catalog`, `news`, `partner`, `vendor`, `advantages`, `text_page`,
  `cert`, `owner`, ...). Загружаются `read_config` через
  `load_form_from_dir('./conf_projects/project_<id>', ...)`.
- `configs/svcmsmanager/**` (bottom_menu, top_menu_tree, bot_rules, content,
  promo, robot_files, find_files, wysiwyg_template) — БД-аватары инструментов.
  Как fallback **не загружаются** (`config_folder` в конфиге не задан), правки
  там пока ни на что не влияют — но правила выше соблюдать.

## Протестировано (дев, Host: dev-crm.test)

- `POST /wysiwyg/good/anons/2` (file_list/create_folder/delete) → 200,
  `files_dir_web: /files/project_5830`.
- `GET /wysiwyg/good/anons/init_options` → 200.
- `GET /svcms/left-menu`, `/gpt-assist/init`, `/mainpage` → 200.
- Проблемный WYSIWYG чинился так: `routes/wysiwyg_routes.py` теперь передаёт
  `request` в `read_config`, `options_modify/out_template` awaited,
  `wysiwyg_process.py` не сваливается на успешном ответе (был мёртвый `return`).

## Мелочи

- В dev-базе `svcms` нет таблицы `wysiwyg_template` — `init_options` отвечает
  пустым `templates`, шаблонов не будет до её создания.
- `transliterate` установлен в `.venv`, но отсутствует в `requirements.txt`
  (используется `conf_projects/project_5830/*/ajax.py`).
- `routes/messenger.py` переведён на per-request engine; при
  `messenger_rules={}` часть эндпоинтов отдаёт нейтральные ответы.