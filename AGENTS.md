# AGENTS.md — CrmFreshBackend-python-async

## Что это

Асинхронный JSON-бэкенд на FastAPI, портированный со старого Perl/PG-style CRM.
Фронтенд — отдельное Vue 3 + Vuetify приложение (`../CrmFreshFront-v3`), бэкенд
отдаёт только JSON. Своих html-шаблонов нет; Jinja2 используется ровно в одном
месте — `lib/CRM/form/template.py`.

Ветка `async` (текущая), `v1` — старая версия.

## Запуск

**Обязательно из корня репозитория**: `lib/engine.py:9` захватывает
`os.getcwd()` на импорте (используется для debug-обхода авторизации).

```bash
export config=config_test && uvicorn --reload --port=5000 --workers 1 main:app
# или готовые скрипты:
./start/test.sh          # config_test
./start/svcms_manager.sh # config_svcms_manager
./start/beyeezy.sh  ./start/crimea.sh  ./start/teleweb.sh  ./start/trade.sh
```

`--workers 1` обязателен: `db.get_db()` — мемоизированный process-wide
синглтон, а в `lib/engine.py:117` остался module-level объект `s`. При
нескольких воркерах общее мутабельное состояние ломается.

В виртуальном окружении проекта: `.venv/bin/uvicorn`, `.venv/bin/python`
(Python 3.12).

## Конфигурация

`config.py` целиком:

```python
conf_file = os.getenv('config')      # ИМЯ МОДУЛЯ, не имя файла
config = importlib.import_module(conf_file).config
```

- Значение env `config` — **dotted-путь до модуля**, а не имя файла. Модуль обязан
  экспортировать словарь `config = {...}`.
- Без env `config` модуль печатает инструкцию и делает `quit()` на этапе импорта —
  приложение не поднимется.
- Модули: `config_test`, `config_beyeezy`, `config_crimea`, `config_teleweb`,
  `config_trade`, `config_svcms_manager`, `config_svcms_admin`.
- Все настройки деплоя живут в `config_*.py`. Общих настроек "по умолчанию" нет.
- Конфиг импортируется очень рано (`main.py` → `routes` → `lib.engine` →
  `config`), поэтому модули конфига **не должны** импортировать `routes` или
  `lib.engine` на уровне модуля — получится циклический импорт. `lib.*` и другие
  `configs.*` импортировать можно.

Ключи `config` (на примере `config_test.py`):

| Ключ | Смысл |
|---|---|
| `BaseUrl`, `system_url`, `BaсkendBase` | URL'ы. Внимание: в `BaсkendBase` кириллическая **с** |
| `config_folder` | папка с конфигами инструментов, напр. `configs/test` |
| `cors_origins` | список Origin'ов для CORS (см. раздел «CORS») |
| `cookie` | атрибуты session-cookie: `path`, `samesite`, `secure`, `httponly` |
| `auth` | таблица менеджеров, поля логина/пароля, `encrypt_method` (`mysql_encrypt`/`mysql_sha2`/plain), таблицы сессий и неудачных попыток, лимиты, `use_roles`/`use_permissions` |
| `login.not_login_access` | whitelist путей, которые проходят **без** авторизации |
| `connects.crm_read` / `connects.crm_write` | параметры подключения к MySQL |
| `debug` | обход авторизации, см. ниже |
| `after_create_engine(s)` | хук после создания Engine (резолв проекта по Host) |
| `after_read_form_config(form)` | хук после чтения конфига инструмента |
| `after_all_change_action(form)` | хук после каждой insert/update/delete |
| `const`, `events`, `controllers`, `telegram`, `mail`, `wysiwyg`, `messenger_rules`, `gptassist_rules`, `docpack`, `stat_log` | прочее |

### Debug-обход авторизации

`lib/engine.py:53-58`: если `hostname` есть в `config['debug']['hosts']`
(и, если задан `pwd`, текущий каталог — в `config['debug']['pwd']`), авторизация
не проверяется и подставляется фиксированный менеджер (`manager_id` или `login`).
Если ключа `hosts` нет — условие считается выполненным, т.е. **все запросы
авторизуются как manager_id 0**. В `config_test.py:148` перечислены хосты
разработчиков, включая `sv-home`.

Следствие: на машине разработчика запросы проходят без cookies, поэтому
нельзя по локальным логам судить о работоспособности авторизации.

## Структура

| Путь | Назначение |
|---|---|
| `main.py` | точка входа: FastAPI, CORS, startup-пул, middleware `for_all_requests` |
| `config.py` | загрузка конфига по env `config` |
| `config_*.py` | настройки конкретных деплоев |
| `routes/` | HTTP-роуты, 31 модуль (27 подключены в `routes/__init__.py`) |
| `configs/<проект>/<инструмент>/__init__.py` | `form = {...}` — схема экрана/инструмента |
| `configs/<проект>/<инструмент>/events.py` | хуки `before_insert`/`after_save`/... |
| `configs/<проект>/<инструмент>/events_for_fields.py` | хуки, привязанные к полю |
| `lib/engine.py` | класс `Engine` — контекст запроса |
| `lib/all_configs.py` | `read_config()` — фабрика `Form` по имени инструмента |
| `lib/session.py` | логин, сессии, права |
| `lib/core.py`, `lib/core_crm.py` | утилиты и CRM-логика |
| `lib/CRM/form/` | класс `Form` + сохранение, загрузка файлов, поиск, шаблоны |
| `db/` | `FreshDB` (async, aiomysql) и `FreshDBSync` (sync, pymysql) |
| `files/` | загруженные файлы (в gitignore), раздаёт nginx, не FastAPI |
| `conf_projects/project_<id>/` | пер-проектные переопределения для SV-CMS |
| `settings/nginx_section.txt` | пример nginx-конфига (справка, Python его не читает) |
| `daemons/`, `dbd_creator/`, `dbf_daemon/` | фоновые задачи и выгрузка в XBase |
| `models/` | **мёртвый код** (Peewee), нигде не импортируется |
| `confsvcmsmanager/` | **пустая папка**, актуальный аналог — `configs/svcmsmanager/` |
| `tasks/` | **пустая папка**, под Celery (сам Celery не используется) |

### Инструменты (`configs/`)

`configs/<проект>/<инструмент>/` — это «экран» CRM: списки, карточки, справочники.
Проекты: `beyeezy` (18 инструментов), `crimea` (13), `teleweb` (15), `test` (6),
`svcmsmanager` (9). Загрузка: `lib/all_configs.py:load_form_from_dir` делает
`importlib.import_module(f"{config_folder_as_module}.{config}")`.

Тяжёлая логика вынесена из роутов в соседние модули: `routes/edit_form/`,
`routes/get_result/`, `routes/docpack_routes/`, `routes/parser_excel/`.

## Контракт `Engine`

`lib/engine.py`. Экземпляр на запрос создаётся в `main.py:48`, кладётся в
`request.state.engine`.

```python
s = request.state.engine
```

**Не используйте `from lib.engine import s`** — это module-level глобал
(`lib/engine.py:117`), оставшийся от старой реализации. Он не потокобезопасен и
ломается при `--workers > 1` и при параллельных запросах.

Атрибуты после `await engine.reset(request=..., status_code=200)`:
`s.db` / `s.db_read` / `s.db_write` (все три — один и тот же объект), `s.request`,
`s.headers` (список пар `[имя, значение]`), `s.env` (заголовки запроса, ключи в
lowercase), `s.manager`, `s.errors`, `s.project`, `s.config`, `s._end`,
`s._content`, `request.state.cookies` (**словарь** `имя -> {value, path, samesite,
secure, httponly}`), `request.state.cookies_for_delete` (**словарь**
`имя -> {path, samesite, secure, httponly}`).

Методы:

| Вызов | Что делает |
|---|---|
| `s.set_cookie(name=..., value=...)` или `s.set_cookie(name, value)` | кладёт значение в `request.state.cookies`; middleware выставит его в ответ |
| `s.set_cookie(..., value=None)` | удаляет cookie (складывает атрибуты в `cookies_for_delete`) |
| `s.set_cookie(..., samesite='none', secure=True)` | переопределяет атрибут для этого вызова, иначе берётся из `config['cookie']` |
| `s.get_cookie(name)` | читает **входящие** cookies |
| `s.request.state.cookies_for_delete[name] = {...}` | ручное удаление cookie |
| `s.headers.append(['X-Foo', 'bar'])` | добавить заголовок ответа (именно список из 2 элементов) |
| `s._content = {...}` + `s.end()` | короткое замыкание: middleware вернёт этот JSON |
| `s.to_json(data)` | `json.dumps` с `indent=4`, `ensure_ascii=False` |

Осторожно:

- `request.state.cookies` хранит **не значение, а словарь с атрибутами**.
  Читать его напрямую из роутов не нужно — middleware в `main.py` сам разложит
  его в `response.set_cookie`.
- Атрибуты удаляемой cookie должны совпадать с теми, что ставились при
  `set_cookie`, иначе браузер не удалит cookie (удаление — это отдельный
  `Set-Cookie` с `Max-Age=0`).
- Короткое замыкание всегда отдаёт **HTTP 200**, `Content-Type: text/plain`
  (`_content_type` игнорируется), потому что в `main.py` возвращается голый
  `Response`.

## Формат ответа и ошибки

Почти все хендлеры возвращают один и тот же конверт:

```json
{"success": 1, "errors": [], "log": [], ...}
```

- `form.success()` возвращает `(True, False)[len(form.errors) > 0]`.
- **Ошибки не передаются HTTP-кодом.** Ответ почти всегда `200`, а неуспех
  обозначается `success: 0` и непустым `errors`.
- Исключения наружу не пробрасываются: `form.errors.append('текст')`,
  `lib/CRM/form/run_event.py` ловит всё и пишет в `errors`,
  `db/functions.py:out_error` пишет в `arg['errors']` и печатает в консоль.
- `lib/all_configs.py:read_config` при неудачном импорте конфига возвращает
  **объект `error`, а не `Form`**. Вызывающий код всё равно делает
  `form.errors` — это работает, но тип другой. Всегда проверяйте.

Типичный хендлер:

```python
router = APIRouter()

@router.post('/get-result')
async def get_result(R: dict, request: Request):
  form = await read_config(request=request, R=R, config=R['config'], script='find_objects')
  ...
  return {'success': form.success(), 'results': form.SEARCH_RESULT, 'errors': form.errors}
```

## Соглашения

- **Отступ 2 пробела** во всём проекте, включая `lib/`, `db/`, `routes/`.
- Типовых аннотаций нет (кроме пары path-параметров).
- Имена: `R` (с заглавной) — тело запроса, `s` — engine, `form` — конфиг
  инструмента, `f` — словарь поля, `arg`/`**arg` — kwargs, `config` внутри роута —
  строка-имя инструмента, `sysconfig` — системный конфиг.
- `exists_arg('key', data)` из `lib/core.py:40` — идиома «получить или False»,
  поддерживает вложенные пути `'a;b;c'`.
- Комментарии и все пользовательские строки — **на русском**.
- Закомментированный код и `print()` для отладки оставлены повсеместно — это
  текущий стиль, не мусор, который надо вычищать.
- Имена маршрутов и функций внутри модуля часто дублируются (`insert`,
  `wysiwyg_upload`, `get_chatlist`) — норма.

## CORS

Настроен в `main.py`. Три части:

1. `dev_origin_regex = r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$"` —
   разрешает петлю на любом порту. Нужно потому, что vite при занятом 8081
   молча переключается на 8082, и перечислять порты списком бессмысленно.
2. `allow_origins=config.get('cors_origins', [])` — прод-домены, задаются
   ключом `cors_origins` в `config_*.py`. Если ключа нет, запросы идут
   same-origin через nginx (`location /backend/`), и CORS не нужен.
3. `allow_private_network=True` — для Chrome Private Network Access. Без этого
   любой preflight с `Access-Control-Request-Private-Network: true` получает
   `400 Disallowed CORS private-network`. Флаг добавляет только
   `Access-Control-Allow-Private-Network: true` в ответ, проверку Origin он не
   отключает.

`expose_headers` — `Content-Disposition` (имя файла из `FileResponse`),
`Content-Length`, `Content-Range`, `Accept-Ranges`, `Last-Modified`, `ETag`.

Грабли, на которые уже наступали:

- **`"*:*"` — не то же самое, что `"*"`.** Starlette проверяет `"*" in
  allow_origins`; `"*:*"` не включает режим `allow_all_origins` и не совпадёт ни
  с одним значением заголовка `Origin`. Если нужен явный wildcard — писать `"*"`.
- **`localhost` и `127.0.0.1` — разные Origin'ы.** Список origins должен
  содержать именно то, что присылает браузер. Vite печатает
  `http://127.0.0.1:8081/`, значит `Origin` будет `http://127.0.0.1:8081`.
- **Порядок middleware.** Starlette кладёт каждый `add_middleware` в начало
  стека: последний добавленный выполняется первым. `CORSMiddleware` намеренно
  регистрируется **после** `for_all_requests`, чтобы быть внешним слоем. Иначе
  при `engine._end` (например, неавторизованный запрос → redirect из
  `session_start`) `for_all_requests` возвращает `Response` напрямую, не
  вызывая вложенное приложение, и заголовки `Access-Control-Allow-*` в ответ
  не попадают — браузер покажет CORS-ошибку вместо 401.
- **Дубликат ACAO.** `settings/nginx_section.txt:29,39,46` добавляет
  `Access-Control-Allow-Origin: *` через `add_header`. Если nginx и приложение
  отвечают одновременно, браузер получит заголовок дважды и отклонит ответ.
  В проде либо убрать `add_header` из nginx, либо не отдавать CORS из приложения.
- Starlette на запрещённый Origin отвечает **`400` с телом
  `Disallowed CORS origin`** — в devtool браузера это выглядит не как 401.

### Cookies и кросс-доменный логин

Атрибуты session-cookie берутся из `config['cookie']` и пробрасываются
`Engine.set_cookie` → `main.py` в `response.set_cookie`. В `config_test.py` и
`config_svcms_manager.py` выставлено `samesite='none'`, `secure=True`,
`httponly=True`.

Почему `SameSite=None` + `Secure`:

- Chrome не отправляет `SameSite=Lax` cookie в кросс-сайтном XHR, поэтому при
  dev-раскладке «фронт на `127.0.0.1:8081`, бэк на `localhost:5000`» авторизация
  молча теряется. Раньше cookie вообще ставились без атрибутов, то есть
  получали `SameSite=Lax`.
- Chrome **требует** `Secure` вместе с `SameSite=None` — иначе cookie
  отбрасывается целиком.
- `Secure`-cookie Chrome принимает на `http://localhost` и `http://127.0.0.1`
  (это trustworthy origins), но **не** примет на `http://<LAN-IP>`. Если деплой
  идёт по обычному http — вернуть `samesite='lax'`, `secure=False`.
- `httponly=True` закрывает `auth_key` от чтения из JS. Фронт cookie в JS не
  читает, так что это ничего не ломает.

**Обязательная парная правка во фронте:** у axios-инстанса в
`CrmFreshFront-v3/src/main.js:50` нет `withCredentials: true`. Без него браузер
не будет ни отправлять, ни принимать cookie при кросс-доменном запросе, и
`allow_credentials=True` на бэкенде останется бесполезным. Пока фронт ходит на
`/backend/...` относительными путями через nginx, всё работает same-origin и
эта правка не нужна.

Сейчас кросс-сайтовая авторизация замаскирована debug-обходом (см. выше) — на
`sv-home` все запросы авторизуются как manager_id 1, и cookie не нужны.

## Известные проблемы

Не чинить, пока не понадобится; здесь список, чтобы не тратить время на
повторное открытие.

**Не запускается на чистом Python 3.12** — исправлено: в `db/freshdb.py` убран
module-level `asyncio.get_event_loop()` и аргумент `loop=loop` в
`aiomysql.create_pool`. Uvicorn импортирует приложение до запуска event loop,
поэтому старый код создавал второй loop и падал с
`got Future attached to a different loop`.

Отсутствует `await` на `read_config` (вместо `Form` возвращается coroutine):

- `routes/page_routes.py:14`
- `routes/table_routes.py:14`
- `routes/documentation_routes.py:14`
- `routes/wysiwyg_routes.py` (`init_options`, `load_template`)
- `routes/ajax.py:17`
- `routes/extend_routes.py:41`
- `routes/multiaction_routes.py:114`

Обращается к несуществующему глобалу `request` (нужен `request: Request` в
сигнатуре) — `NameError` в рантайме:

- `routes/core_routes.py:12,18,200` (`/test`, `/left-menu`, `/login`)
- `routes/core_routes.py:30` — `await s.db(...)`, синхронный вызов async-метода
- `routes/mainpage/__init__.py:13,41,54,71,81` — использует `s` и `config`, у
  которых импорт закомментирован

Прочее:

- `lib/session.py:2` и `lib/send_mes.py:7` — `from db import db`; такого имени
  больше нет (`db/__init__.py` экспортирует только `get_db`).
- `start/translab.sh` ссылается на несуществующий `config_translab`.
- `start/svcms_admin.sh` делает `export config=svcms_manager` — модуля с таким
  именем нет.
- `routes/svcms` импортируется, но `include_router` закомментирован, поэтому
  `conf_projects/` фактически не используется.
- `routes/beeline/` создан, но нигде не подключён.
- `models/` — нерабочий Peewee-код, `peewee` нет в `requirements.txt`.
- `lib/CRM/plugins/search/xlsx.py` импортирует `pandas`, `lib/seo.py` —
  `transliterate`, `lib/svcmsmanager/cache_pages.py` — `pymemcache`. Ни одного
  из них в `requirements.txt` нет, модули падают на импорте.
- `celery`, `redis`, `kombu`, `amqp`, `billiard` в `requirements.txt` не
  используются — импортов нет нигде. `tasks/` пуста.
- `db/functions.py:get_query` — `query_count += " WHERE {where}"` без `f`:
  WHERE не попадает в count-запрос (ломается `maxpage`).
- `SET lc_time_names='ru_RU'` выполняется на **каждом** запросе
  (`db/freshdb.py:72`) — лишний round-trip.
- `db.close_pool()` нигде не вызывается, shutdown-хука нет.
- `lib/multiconnect.py` — устаревшая копия `lib/CRM/form/multiconnect.py`,
  смешивает sync/await и не работает.
- `lib/run_event.py` и `lib/run_event.py.back` — заглушки.
- `lib/save_url_file.py` — заглушка (`pass`).
- `lib/CRM/form/multiconnect_save.py` — пустой файл.
- `db/freshdbs.py:19` переопределяет `exists_arg`; `db/freshdbs.py` дублирует
  `out_error`/`get_query`/`rez_to_str`/`get_func` из `db/functions.py`.
  Импортировать из `db/functions.py`.

## Безопасность

Стоит знать перед любыми правками:

- SQL собирается f-строками — интерполируются имена таблиц и колонок
  (`f'select * from {form.work_table} where ...'`). Параметризуются только
  значения. `where=` — это сырой SQL по замыслу.
- Значения вида `'func:now()'`, `'func:(NULL)'` подставляются в INSERT/UPDATE
  дословно (`lib/core.py:get_func`) — намеренный, но опасный обход.
- Cookies: атрибуты задаются в `config['cookie']` (см. раздел «Cookies и
  кросс-доменный логин»), значение сессии — само значение cookie. В проде за
  nginx cookie same-origin, так что `SameSite=None` там избыточен.
- `set_cookie(value=None)` раньше не удалял cookie — условие в `lib/engine.py`
  было всегда истинным, ветка с `cookies_for_delete` недостижима. Исправлено.
- Debug-обход авторизации включается по имени хоста, см. выше.
- CORS для петли разрешён всегда. Для продакшена это не опасно (regexp
  ограничен `localhost`/`127.0.0.1`/`[::1]` и якорями + `fullmatch`), но
  полагаться на CORS как на защиту нельзя.

## Прочее

- `requirements.txt` — полный `pip freeze`, а не минимальный набор. Синхронизируйте
  с `uv.lock`/`poetry.lock`, если они появятся.
- `.gitignore` содержит только `__pycache__` и `files/*`.
- Тестового фреймворка в проекте нет. Проверка изменений — запустить uvicorn и
  ударить curl'ом по эндпоинту.
- `test.py`, `test_sync.py`, `test_resize.py`, `test_sync.py` в корне — ручные
  скрипты, не автотесты. `testform.html` — ручная тест-страница.
- `js/Chart.bundle.min.js` — вендоренный Chart.js, из Python не подключается.
- `starlette==1.7.0` и `fastapi==0.141.1` — свежие версии; `starlette.testclient`
  требует `httpx2`, которого нет в `.venv`, поэтому `TestClient` не работает —
  проверяйте через реальный uvicorn и `curl`.

# Инструкции для Агентов
- Для планирования (plan), исследования (explore) и архитектурных мыслей ВСЕГДА использовать локальную модель `openai/r1-coder` (endpoint http://localhost:11434/v1).
- Для непосредственного написания кода и мелкого багфикса использовать образ `rafw007/ornith-claude-coder:latest`.
