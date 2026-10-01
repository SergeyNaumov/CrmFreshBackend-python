# Известные проблемы

Не чинить, пока не понадобится; список, чтобы не открывать заново.

## Python 3.12

Исправлено: в `db/freshdb.py` убран module-level `asyncio.get_event_loop()` и
аргумент `loop=loop` в `aiomysql.create_pool`. Uvicorn импортирует приложение
до запуска event loop, поэтому старый код создавал второй loop и падал с
`got Future attached to a different loop`.

## Исправлено (2026-09-27): глобальный `s` / `db`, `read_config`

- Убран живой `from lib.engine import s` из `lib/CRM/plugins/search/xlsx.py`.
  Глобал `s=Engine()` в `lib/engine.py` оставлен **только** как legacy-шим для
  конфигов вне svcms_manager (см. `00-overview.md`).
- `lib/session.py`, `lib/send_mes.py` — убран `from db import db`; `session_create`
  использует `s.db`.
- `routes/docpack_routes/load_act.py`, `load_app.py` — `get_db()` вместо
  глобального `db`.
- `routes/testing.py` — `s.db` вместо глобального `db`, `pymysql.escape_string`.
- Добавлены `await read_config(request=request, ...)`: `routes/ajax.py`,
  `page_routes.py`, `table_routes.py`, `documentation_routes.py`,
  `extend_routes.py`, `multiaction_routes.py`, `news_routes.py`,
  `video_routes.py`, `autocomplete.py`, `const_routes.py`,
  `edit_form/multiconnect.py`.
- `routes/multiaction_routes.py` — `await` у `set_all_value_field`/`change_price`,
  `delete_records` теперь реально выполняет DELETE.

## `conf_projects/` — миграция выполнена

`project_5759/5782/5793/5794/5795` переведены на async (2026-09-27): хуки
`async def`, `form.db.*` через `await`, `form.s.project_id` → `request.state`.
Все модули импортируются. Осталось: в них встречаются вызовы `form.errors(...)`
как функции и похожие исторические дефекты (срабатывают только в ветках ошибок).

## Прочее

- `routes/core_routes.py` — в рабочем дереве был случайно дописан артефакт
  `<system> NOTE: Updated ...` и потерян `return response` (SyntaxError, роутер
  не импортировался). Исправлено.
- `routes/core_routes.py` → `/core/get-manager` вызывает
  `project_get_permissions_for(form=None, ...)` и `get_permissions_for(R=R)` —
  обе сигнатуры не совпадают, эндпоинт всегда возвращает ошибку.
- `start/translab.sh` ссылается на несуществующий `config_translab`.
- `start/svcms_admin.sh` делает `export config=svcms_manager` — модуля с таким
  именем нет. **Исправлено (2026-09-28):** теперь `config=config_svcms_admin`
  (см. `15-svcms-admin.md`).
- `routes/beeline/` создан, но нигде не подключён.
- `models/` — нерабочий Peewee, `peewee` нет в зависимостях.
- `lib/CRM/plugins/search/xlsx.py` импортирует `pandas`, `lib/seo.py` —
  `transliterate`, `lib/svcmsmanager/cache_pages.py` — `pymemcache`. Ни одного
  нет в `requirements.txt`, модули падают на импорте.
- `celery`, `redis`, `kombu`, `amqp`, `billiard` в `requirements.txt` не
  используются; `tasks/` пуста.
- `db/functions.py:116` — `query_count += " WHERE {where}"` без `f`, WHERE не
  попадает в count-запрос (ломается `maxpage`).
- `SET lc_time_names='ru_RU'` выполняется на **каждом** запросе
  (`db/freshdb.py:76`) — лишний round-trip.
- `db.close_pool()` нигде не вызывается, shutdown-хука нет.
- `lib/multiconnect.py` — устаревшая копия `lib/CRM/form/multiconnect.py`,
  смешивает sync/await и не работает.
- `lib/run_event.py` и `lib/run_event.py.back` — заглушки.
- `lib/save_url_file.py` — заглушка (`pass`).
- `lib/CRM/form/multiconnect_save.py` — пустой файл.
- `db/freshdbs.py:19` переопределяет `exists_arg`; дублирует
  `out_error`/`get_query`/`rez_to_str`/`get_func` из `db/functions.py`.
- `routes/testing.py` подключён в прод (`routes/__init__.py:49`) и отдаёт
  `/config` целиком (включая пароли БД). Отладочные эндпоинты оставлены
  по решению команды; при ужесточении безопасности — убрать из-под prod.
- `routes/core_routes/login.py` — мёртвый, никем не импортируется.
- `daemons/gpt-daemon.py` — отдельный процесс, использует глобальный
  `from db import db` (вне зоны правок).
- `configs/beyeezy/bottom_menu/fields.py` — синтаксическая ошибка (непарные
  скобки), конфиг beyeezy вне зоны правок.

## Исправлено (2026-09-28): админка svcms_admin

- `lib/all_configs.py:read_config` — при пустом `project_id` переменная `form`
  не инициализировалась (`UnboundLocalError` на `if not(form)`). Добавлены
  `form=False; errors=[]` до ветки проекта. Нужно для админки без проекта.
- `config_svcms_admin.py` — дописан `alter_all_change_action` (был `NameError`),
  добавлен `BaseUrl:''`, авторизация переведена на `admin`/`admin_session`/
  `admin_session_fails` + `mysql_encrypt`, добавлен `after_create_engine`.
- `start/svcms_admin.sh` — запускает `config_svcms_admin` (было `svcms_manager`).
- Новый контроллер `routes/svcmsadmin/left_menu_admin.py`
  (`GET /svcmsadmin/left-menu-admin`).
- `db/migrate_admin_menu_new.py` — перенос меню из `admin_menu` в `admin_menu_new`.
- Подробнее — `15-svcms-admin.md`.

## Типы полей: filter_extend_* (расхождение кода и docs)

- `set_orig_types.py:25` ставит `orig_type` и подменяет `type='select'` только
  для `select_from_table`/`select_values`/`filter_extend_select_from_table`/
  `filter_extend_select_values`.
- `process_edit_form.py:55` вырезает из карточки только поля с `orig_type^=filter_extend_`.
  Значит `filter_extend_text/checkbox/switch/date/datetime` остаются в
  `form.fields` (фронт их не рисует — нет компонента).
- `get_filters_routes.py` не конвертирует `filter_extend_checkbox/switch/datetime`
  → фильтр на фронте не отрисуется. Обход: `checkbox`+`filter_on` для текущей
  таблицы.
- `get_filters_routes.py:9` — заглушка `get_values_for_select_from_table` (возвращает
  `[]`, вызывается с обратным порядком аргументов) → select-фильтры без `values`.
- **Исправлено (2026-09-28):** `lib/CRM/form/get_search_where.py` для
  `filter_extend_select_values` использовал `wt.db_name` вместо алиаса
  `tablename` — фильтры по смежной таблице (`author`→`apv.login`,
  `tmp_type`→`t.type`) падали. Теперь для `filter_extend_*` берётся `table`.
- Добавлен тип `multiconnect_old` (старый `multicheckbox`, строка `;key;`):
  `lib/CRM/form/multiconnect_old.py`, `lib/core.py`, `get_values.py`,
  фронт `multiconnect_old.vue`.
- Подробнее — `13-field-types.md` и `docs-developer/field-types/filter_extend.md`.

## Исправлено (2026-09-28): autocomplete

- `routes/autocomplete.py` — ветка `filter_extend_text` безусловно читала
  `element['filter_table']` → `KeyError` (500), если в поле задан только
  `tablename` (например, `project.domain`). Теперь таблица ищется по
  `tablename` (алиас) или `filter_table`, и для `filter_extend_text` строится
  `SELECT DISTINCT db_name ... LIKE %s`.
- Там же `search_query` получал `limit 30` дважды (`limit 30 limit 30`) → SQL-
  ошибка и `list:null` у select-автокомплита. `limit` добавляется один раз.
- В `get_list` добавлен финальный `return []` (раньше мог вернуться `None`).

## Прочее по проекту

- `requirements.txt` — полный `pip freeze`, не минимальный набор.
- `.gitignore` — только `__pycache__` и `files/*`.
- Тестового фреймворка нет. Проверка — запустить uvicorn и `curl` по эндпоинту.
- `test.py`, `test_sync.py`, `test_resize.py` в корне — ручные скрипты.
  `testform.html` — ручная тест-страница.
- `js/Chart.bundle.min.js` — вендоренный Chart.js, из Python не подключается.
- `starlette==1.7.0`, `fastapi==0.141.1`; `TestClient` требует `httpx2`,
  которого нет в `.venv` — проверяйте реальным uvicorn и `curl`.
