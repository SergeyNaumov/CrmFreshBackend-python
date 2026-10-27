# Деплой svcms_manager (менеджер проектов)

Кратко по `config_svcms_manager`. Общее — в `00-overview.md`, контракт
Engine — в `02-engine.md`.

## Прод-адреса (дев ↔ прод)

| Что | Дев | Прод |
|---|---|---|
| MySQL `svcms` | `localhost` (`config_*.py` → `connects.crm_*`) | **`185.76.252.12`** (user `svcms`, пароль пустой) |
| Web/движок сайтов | локально | `naumov@178.57.220.192:7725`, движок в `/var/www/svcms-async/sites` |
| Бэкенд админки | `:5000` (`config_svcms_admin`) | `/var/www/svcms/admin/backend`, сервис `svcms.admin` (`:3011`), фронт `admin3.design-b2b.com` |

`host` задаётся в конфиге **на сервере** и в репозитории остаётся `localhost`
(дев-значение). Движок сайтов держит свой адрес БД в
`sites/lib/config.py` — деплой `tools/sync_engine_to_prod.sh` из репо
`svcms-async` его **не заливает** (`--exclude='config.py'`); заливка `localhost`
на прод роняет все сайты (см. `agent-doc/18_prod_runtime.md` в репо `svcms-async`).

### На прод-хосте две MySQL — работать только с `185.76.252.12`

На `178.57.220.192` локально поднят старый mysqld с базой `svcms` — это
**устаревшая копия**, её не использует ни один конфиг (менеджер, движок и
админка смотрят на `185.76.252.12`, `@@hostname = stg-web01-new`).

- `mysql -u svcms svcms` **без `-h`** (сокет/`127.0.0.1`) идёт в локальную
  копию, а не в прод → миграции «применяются», но ничего не меняют.
  Всегда указывать `-h 185.76.252.12`.
- Сверка 2026-10-18: `ds_good` (503), `const` (62123), `domain` (7818),
  `ds_zakaz` (5) совпадали, но локальная копия отставала по `ds_news`
  (MAX(id) 308 против 314) и не имела миграций `ds_options.parent_id/note`
  (31 опция против 33).
- Локальную копию не трогаем и не синкаем: источник истины — только
  `185.76.252.12`. `sync/pull_from_prod.sh` при этом дампит `127.0.0.1`
  (устаревшая ветка скрипта) — для актуальных данных брать `-h 185.76.252.12`.

## Контракт request state (обязателен здесь)

Всё состояние запроса живёт в `request.state` — никаких модульных глобалов,
`Engine` создаётся на каждый запрос (`main.py:51`).

| Источник | Что брать |
|---|---|
| `request.state.engine` | объект `Engine` (имя в роутах — `s`) |
| `request.state.engine.db` | асинхронный MySQL (aiomysql) |
| `request.state.manager` | менеджер (после `after_create_engine`; файловая логика читает `manager['files_dir']` / `manager['files_dir_web']`) |
| `request.state.project['project_id']` | ID проекта (домен `dev-crm.test` → `5830`) |
| `request.state.project['template_id']` | шаблон редактора |

**Запрещено в контуре svcms_manager:**

- `from lib.engine import s` — глобал из `lib/engine.py:131`.
- `form.manager` — alias из `lib/all_configs.py:239` (костыль миграции).
  Читать `form.request.state.manager`.
- `form.s.project_id`, `s.project_id`, `form.s.template_id` — только
  `form.request.state.project[...]`.
- `db.get_db()` / `from db import db` — `None`/мемоизованный синглтон.
  Только `request.state.engine.db`.

## Асинхронность

- Все события БД и хуки — `async def`. `lib/CRM/form/run_event.py` всегда делает
  `await event(form)`; sync-функция → `TypeError` и 500 (ловится только
  `AttributeError`).
- Все `form.db.*` и помощники (например модуль `InExtUrl`) вызываются через
  `await`, включая вложенные (`exists_url()` в `conf_projects/project_5830/*/ajax.py`).

## Карта живого кода

- `config_svcms_manager.py:6` — `after_create_engine` резолвит проект по Host:
  `dev-crm.test` → project_id 5830, заполняет `request.state.project`,
  `request.state.manager`. `after_read_form_config:63` проставляет
  `files_dir`/`files_dir_web` проекта.
- `configs/svcmsmanager/config_wysiwyg.py` — WYSIWYG options/hooks, project_id из
  request state. Импортируется напрямую (не через `config_folder`).
- `configs/svcmsmanager/gptassist_rules.py` — GPT-ассистент через
  `request.state.engine`; вызывается из `routes/gptassist/__init__.py`.
- `conf_projects/project_5830/<инструмент>/` — конфиги проекта 5830 (`good`,
  `catalog`, `news`, `partner`, `vendor`, `advantages`, `text_page`, `cert`,
  `owner`, ...). Загружаются `read_config` через
  `load_form_from_dir('./conf_projects/project_<id>', ...)`.
- `configs/svcmsmanager/**` (bottom_menu, top_menu_tree, bot_rules, content,
  promo, robot_files, find_files, wysiwyg_template) — БД-аватары инструментов.
  Как fallback **не загружаются** (`config_folder` в конфиге не задан), правки
  там пока ни на что не влияют — но правила выше соблюдать.

## Импорт / экспорт данных проекта

Инструмент в меню manager: **«Импорт / экспорт данных»** (`value='ds-data'`,
маршруты `/vue/ds-data` и `/ds-data`). Переносит данные таблиц DS-проекта и
файлы `files/project_<id>` между проектами одним zip-архивом.

Код:

| Файл | Назначение |
|---|---|
| `lib/svcmsmanager/ds_data_transfer.py` | **реестр таблиц** (единственное место, где описаны все переносимые таблицы) |
| `lib/svcmsmanager/ds_data_export.py` | сборка архива, задача `svcmsmanager/project_export` |
| `lib/svcmsmanager/ds_data_import.py` | dry-run (`build_plan`) + импорт, задача `svcmsmanager/project_import` |
| `routes/svcms/data_transfer.py` | эндпоинты (см. ниже) |

Эндпоинты (все под префиксом `/svcms`, контракт `success/errors`):

- `GET /data/tables` — таблицы проекта со счётчиками и человеческими
  названиями (`title` из реестра);
- `POST /data/export/start` `{tables:[...]}` — фоновая задача экспорта;
  архив появляется в `files/tmp/`, ссылка на скачивание — в `result.url`
  (`/download_tmp/<file>`);
- `POST /data/import/preview` (multipart `file`) — загрузка архива + dry-run
  план (ничего не пишет);
- `POST /data/import/start` `{import_id, mode}` — фоновая задача импорта,
  `mode`: `replace` | `merge`.

Формат архива: `manifest.json` + `data/<table>.json` + `files/` (всё
содержимое `files/project_<src>/`, **включая ресайзы** `_mini1..3`).
`project_id` в данные не пишется (берётся целевой проект по домену), исходный
`id` строк сохраняется — только для ремапа ссылок (`rubricator_id`, `good_id`,
`parent_id`, ...), т.к. AUTO_INCREMENT в другом проекте другой.

Импорт — одна транзакция (`db.pool.acquire()` + ручной COMMIT/ROLLBACK);
файлы копируются в проект только **после COMMIT**, при ошибке БД откатывается,
файлы остаются нетронутыми. Режим `replace` очищает строки выбранных таблиц
проекта перед вставкой; `merge` ищет существующие по «натуральному» ключу
таблицы (`natural_key`) и обновляет, без ключа — вставляет заново. Файлы в
`merge` с другим содержимым не перезаписываются (счётчик `conflicts`).
Служебные таблицы (`ds_zakaz`, `ds_zakaz_good`, `ds_form_submit` — заказы и
заявки с персональными данными) по умолчанию **не выгружаются**, только по
явному выбору. После успешного импорта сбрасывается кэш домена
(`clear_cache_for_domain`).

Очистка `files/tmp`: загруженные архивы импорта (`ds_import_*.zip`) удаляются
через 24 часа, готовые архивы экспорта (`ds_data_export_*.zip`) — через неделю;
чистка «ленивая», при следующем экспорте/загрузке (системного cron нет).

**Важно:** реестр таблиц статический. При добавлении новой таблицы `ds_*`
(структуры) её нужно прописать в `lib/svcmsmanager/ds_data_transfer.py` —
задать `title`, порядок вставки `order`, при необходимости `natural_key`,
`parent_col`, `refs` и `file_cols`. Иначе таблица не попадёт в экспорт/импорт.
Подробная инструкция и чек-лист — в `docs-developer/21-ds-data-transfer.md`.

## Debug

`config_svcms_manager.py:180` — `debug.hosts: ['sv-home']`, `manager_id: 5520`.
На этих хостах авторизация обходится (см. `01-run-config.md`).

## Протестировано (дев, Host: dev-crm.test)

- `POST /wysiwyg/good/anons/2` (file_list/create_folder/delete) → 200,
  `files_dir_web: /files/project_5830`.
- `GET /wysiwyg/good/anons/init_options` → 200.
- `GET /svcms/left-menu`, `/gpt-assist/init`, `/mainpage` → 200.
- WYSIWYG чинился так: `routes/wysiwyg_routes.py` передаёт `request` в
  `read_config`, `options_modify/out_template` awaited, `wysiwyg_process.py`
  не сваливается на успешном ответе (был мёртвый `return`).

## Мелочи

- В dev-базе `svcms` нет таблицы `wysiwyg_template` — `init_options` отдаёт
  пустой `templates`.
- `transliterate` установлен в `.venv`, но отсутствует в `requirements.txt`
  (используется `conf_projects/project_5830/*/ajax.py`).
- `routes/messenger.py` переведён на per-request engine; при
  `messenger_rules={}` часть эндпоинтов отдаёт нейтральные ответы.
