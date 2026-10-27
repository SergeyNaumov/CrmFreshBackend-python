# Деплой svcms_manager (менеджер проектов)

Кратко по `config_svcms_manager`. Общее — в `00-overview.md`, контракт
Engine — в `02-engine.md`.

## Прод-адреса (дев ↔ прод)

| Что | Дев | Прод |
|---|---|---|
| MySQL `svcms` | `localhost` (`config_*.py` → `connects.crm_*`) | **`localhost`** (`mysql -u svcms svcms` на прод-хосте; user `svcms`, пароль пустой) |
| Web/движок сайтов | локально | `naumov@185.76.252.12` (ssh `-p7725`), движок в `/var/www/svcms-async/sites` |
| Бэкенд админки | `:5000` (`config_svcms_admin`) | `/var/www/svcms/admin/backend`, сервис `svcms.admin` (`:3011`), фронт `admin3.design-b2b.com` |

`host` задаётся в конфиге **на сервере**; после переезда прода там снова
`localhost`, т.е. совпадает с репозиторным (дев) значением. Движок сайтов держит
свой адрес БД в `sites/lib/config.py` — деплой `tools/sync_engine_to_prod.sh` из
репо `svcms-async` его **не заливает** (`--exclude='config.py'`). Правило
оставляем: конфиг на сервере — серверный файл, не перезаписывать
(см. `agent-doc/18_prod_runtime.md` в репо `svcms-async`).

### Прод-хост — `185.76.252.12`, MySQL на нём локальная

С 2026-10 прод переехал: ssh — `ssh -p7725 naumov@185.76.252.12`, на этот же IP
указывают DNS всех доменов (`demo1.digitalstrateg.ru`, `admin3.design-b2b.com`,
`crm.digitalstrateg.ru`, …). База `svcms` снова живёт **на самом прод-хосте**:

- внутри прод-хоста: `mysql -u svcms svcms` (сокет, **без `-h`**);
- конфиги на проде (менеджер, движок, админка): `host = 'localhost'`;
- снаружи БД не слушает — дампы/миграции только через ssh;
- прежняя схема (web-хост `178.57.220.192` + БД по `-h 185.76.252.12`) устарела:
  не возвращать `-h 185.76.252.12`/`-h127.0.0.1` в скрипты и доки.
- IP-адреса в конфигах админки (`LETS_ENCRYPT_ADDR`, шаблон DNS/SPF при
  создании домена) — тоже `185.76.252.12`.

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
  promo, `files`/`robot_files`, find_files, wysiwyg_template) — **общие** конфиги
  инструментов (`config_folder: 'configs/svcmsmanager'` в
  `config_svcms_manager.py`). Загружаются, если у проекта нет своей папки
  `conf_projects/project_<id>/<config>/`. Часть из них (`ds_*`, `promo`,
  `files`, `robot_files`) — симлинки на канон в движке
  `svcms-async/manager/backend/conf/` (дев-путь). На проде `config_folder` в
  `config.py` не задан → читается `conf` рабочего каталога
  `/var/www/svcms/manager/backend/conf/` — общий конфиг заливать туда.

## Файлы для поисковиков (таблица `files`)

Сервис в меню manager: **«Файлы для поисковиков»** — пункт встроен в базовое
левое меню (`routes/svcms/left_menu.py`, `FILES_MENU_ITEM`) для всех проектов;
конфиг называется **`files`** — как в легаси-менеджере
(`admin_table.pl?config=files`, «Файлы на сайте»). Таблица `files`:
`id, url, body, project_id, type`), записи фильтруются по текущему
`project_id` (`conf/files/events.py: permissions`).

Имена-синонимы: `robot_files` (его использует проект 5794) — **симлинк** на
каталог `files`; `find_files` (5759) — свой legacy-конфиг, не трогаем.

Канон конфига — в движке: `svcms-async/manager/backend/conf/files/`
(как `ds_*` и `promo`), в этом репозитории
`configs/svcmsmanager/files` и `configs/svcmsmanager/robot_files` — **симлинки**
на него. На проде рантайм менеджера — `/var/www/svcms/manager/backend`
(`WorkingDirectory` юнита `svcms.manager`), поэтому общий конфиг заливается в
`/var/www/svcms/manager/backend/conf/files/` (`config_folder` на проде
не задан → по умолчанию `conf`).

Зачем: администратор размещает **произвольный контент файлов домена** —
`/robots.txt`, `/sitemap.xml`, `/AGENTS.md`, `/ads.txt`, `/rrrxxx` и т.п.
Движок (`svcms-async`, `sites/lib/server_files.py`) отдаёт их **раньше** штатных
robots/sitemap: `/robots.txt` и `/sitemap.xml`, заданные в `files`,
переопределяют автогенерацию (`lib/seo_files.py` / `for_robots_id`).
Если записи в `files` нет — работает прежнее поведение (авто-robots/sitemap,
иначе обычная страница/404).

Правила заполнения:

- `url` — путь с ведущего слэша (`/robots.txt`); расширение не обязательно
  (`/rrrxxx`, `/ads`, `/AGENTS` тоже работают — движок проверяет любой путь,
  кроме корня); events нормализуют значение и **не дают создать дубль**
  `(project_id, url)` — в таблице нет уникального ключа;
- `type` (MIME) — необязателен: пусто → по расширению (`.html`/`.htm` →
  `text/html`, `.xml` → `application/xml`, `.md` → `text/markdown`, иначе
  `text/plain`), для `text/*` движок дописывает `charset=utf-8`;
- `body` — содержимое как есть (textarea в форме, в списке — экранированный
  фрагмент, без inline-редактора);
- `tree_use`/`sort` у `files` нет (плоская таблица) — в конфиге выключены,
  иначе каскадное удаление ищет несуществующий `parent_id`.

Проверено на деве (Host `demo1.digitalstrateg.ru`): `get-filters`/`get-result`
(`files` и `robot_files`), insert (url нормализуется, `project_id`
проставляется), дубль и пустой url отклоняются, edit/delete работают; движок
отдаёт запись из БД для `/robots.txt`, `/sitemap.xml`, `/AGENTS.md`, `/rrrxxx`,
а без записи — прежний ответ (`Disallow: /` для demo-поддомена, 404 для прочих).

## Константы магазина (Яндекс.Маркет)

Сервис «Настройки сайта» (`ds_const`, таблица `const`) — статический список
полей в `configs/svcmsmanager/ds_const/events.py`. Для автогенерируемого
`/catalog.yml` (движок `sites/lib/seo_files.py::catalog_yml`, см.
`svcms-async/agent-doc/06_seo.md`) добавлен таб **«Магазин (Яндекс.Маркет)»**:

| Константа | Что задаёт |
|---|---|
| `delivery_cost` | стоимость доставки, ₽; пусто — блок доставки в YML не выгружается, `0` — бесплатная |
| `delivery_days` | срок доставки (`1-3`) — атрибут `days` у `<option>` (опционально) |
| `pickup` | самовывоз: `1`/`да` → `<pickup>true</pickup>` |

Значения — **per-project** (строка в `const` с `project_id`), в коде ничего не
хардкодится. Имена должны быть и в `template_const` шаблона DS (иначе движок не
попадёт ими в `cnst`, `lib/dsengine/__init__.py::get_const` фильтрует по
`template_const`), поэтому для шаблона `2026/ds-constructor` они заведены там же.

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
