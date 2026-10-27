# API управления контентом DS-сайта (v1)

HTTP-API для внешних интеграций с DS-сайтом: чтение и запись контента тех же
таблиц, с которыми работает движок (`ds_good`, `ds_catalog`, `ds_docs`, …),
загрузка файлов и статистика обращений. Ключ и права хранятся в константах
проекта, отдельной БД/таблиц не требуется.

Панель управления ключом и просмотр документации — в менеджере, пункт меню
**«API и интеграции»** (`/vue/ds-api`), описание методов открывается на
`/vue/documentation/ds_api` (можно скачать как один HTML-файл).

## Где живёт код

| Файл | Назначение |
|---|---|
| `/var/www/svcms-async/sites/lib/api/router.py` | маршрутизатор `POST /api/v1/<метод>`, изоляция проектов, статистика/аудит |
| `/var/www/svcms-async/sites/lib/api/auth.py` | ключ, scopes, лимиты, IP-белый список |
| `/var/www/svcms-async/sites/lib/api/crud.py` | `select/insert/update/replace/delete`, WHERE/ORDER, характеристики, ЧПУ |
| `/var/www/svcms-async/sites/lib/api/entities.py` | реестр сущностей и целей загрузки файлов |
| `/var/www/svcms-async/sites/lib/api/schema.py` | типы/длины/NOT NULL/enum из `DESC таблицы` |
| `/var/www/svcms-async/sites/lib/api/upload.py` | `POST /api/v1/upload` (multipart), webp, пресеты миниатюр |
| `/var/www/svcms-async/sites/lib/api/stats.py` | статистика и журнал запросов |
| `/var/www/svcms-async/sites/lib/api/errors.py` | конверт ошибок |
| `/var/www/svcms-async/sites/main.py` | middleware-ветка `/api/` (до движка сайта) |
| `lib/svcmsmanager/ds_api.py` | работа менеджера с ключом/статистикой |
| `lib/svcmsmanager/api_doc.py` | генерация HTML-документации для админки |
| `routes/svcms/api_keys.py` | эндпоинты панели `/vue/ds-api` |
| `routes/documentation_routes.py` | ветка `/vue/documentation/ds_api` |
| `db/migrate_ds_api.py` | создание таблиц статистики/журнала |

## Включение

API отвечает только если задана константа проекта `api_key` (иначе — `403`).
Настройки — константы проекта (таблица `const`):

| Константа | Смысл |
|---|---|
| `api_key` | сам ключ (обязателен). Хранится открытым текстом — так интеграцию можно завести без дополнительных таблиц; в журнал/статистику пишется маска |
| `api_scopes` | через запятую: `select,insert,update,replace,delete,upload`. Пусто = только `select` |
| `api_rate_limit` | `"600/60"` — запросов/секунд. По умолчанию `600/60` |
| `api_rate_limit_day` | суточный лимит запросов. По умолчанию `20000` |
| `api_allow_ips` | через запятую/пробел; пусто = любые IP |

Настройки кешируются в процессе на 60 секунд — смена/отзыв ключа действует в
пределах минуты. Ключи `api_*` исключены из ds-data-архива
(`21-ds-data-transfer.md`), если не включён флаг «включить ключ».

## Аутентификация

Ключ передаётся в заголовке `X-API-Key` либо `Authorization: Bearer <ключ>`.
Сравнение — `hmac.compare_digest`. Метод `ping` ключа не требует.

```bash
curl -s -X POST https://demo1.digitalstrateg.ru/api/v1/ping
# {"ok":true,"data":{"pong":true,"api":"v1","host":"demo1.digitalstrateg.ru"}}

curl -s -X POST https://demo1.digitalstrateg.ru/api/v1/select \
  -H 'X-API-Key: <ключ>' -H 'Content-Type: application/json' \
  -d '{"entity":"good","limit":5,"order":"id desc"}'
```

**Изоляция проектов.** Процесс сайта обслуживает один проект (`env project_id`),
и запросу разрешён только он: `project_id` берётся из домена (`Host`), из тела
запроса **не принимается**. Несовпадение `Host` с проектом процесса — `403`.

## Конверт ответа

Успех (обычный HTTP 200):

```json
{"ok": true, "data": { … }}
```

Ошибка (HTTP-код соответствует ошибке, в отличие от конверта менеджера с
`success: 0`):

```json
{"ok": false, "error": {"code": "validation", "message": "исправьте поля",
                        "fields": {"artikul": "поле обязательно"}}}
```

| `code` | HTTP | Когда |
|---|---|---|
| `bad_request` | 400 | нет/битые параметры, неизвестная колонка, превышен батч |
| `unauthorized` | 401 | нет/неверный ключ |
| `forbidden` | 403 | нет `api_key`, scopes, чужой IP/проект |
| `not_found` | 404 | сущность/строки не найдены |
| `conflict` | 409 | конфликт естественного ключа |
| `validation` | 422 | ошибки полей (`error.fields`) |
| `rate_limit` | 429 | превышен лимит (в заголовке — текст лимита) |
| `internal` | 500 | непредвиденная ошибка (в лог — traceback) |

## Методы

Все методы — `POST /api/v1/<метод>`, тело — JSON-объект. `info` требует scope
`select`, `upload` — `upload`, остальные — одноимённый scope.

### `info`

Список сущностей, целей загрузки и лимитов (для самодокументируемого клиента).

```json
{"entity": "…", "table": "ds_good", "title": "Товары",
 "primary_key": "id", "natural_key": ["artikul"], "tree": null,
 "chpu_prefix": "/good/", "params": "good",
 "refs": {"rubricator_id": "catalog", "brand": "brands"},
 "files": {"photos": {"target": "good_galery", "webp": true,
                      "resize": ["…"], "kinds": ["image"]}},
 "read_only": false}
```

### `select`

```json
{"entity": "good", "ids": [1,2,3], "where": {"rubricator_id": 5},
 "limit": 50, "offset": 0, "order": "id desc",
 "fields": ["id","header","price"], "with": {"params": true, "photos": true}}
```

- `ids` — список id; `where` — объект условий (можно оба).
- `order` — `"<колонка> [asc|desc], …"` (только реальные колонки).
- `fields` — подмножество колонок.
- `with.params` — добавить краткую запись характеристик в `data.params`;
  `with.photos` — фотографии (для `good`).
- `limit` — по умолчанию 50, максимум 500; `offset` — смещение.
- Ответ: `{"rows": [...], "total": N, "limit": L, "offset": O}`. Для сущностей
  с ЧПУ в строки добавляются `url`/`slug` (из `in_ext_url`).

### `insert`

```json
{"entity": "good", "data": {"header": "Товар", "artikul": "A-1", "price": 100}}
{"entity": "good", "items": [ {…}, {…} ]}
```

Батч — до 100 строк (`items`). Ответ: `{"ids": [...], "inserted": N}`.
Для сущностей с характеристиками в `data.params` передаётся краткая запись,
она синхронизируется с `ds_params_good`. Для сущностей с ЧПУ поле `slug`
пишется в `in_ext_url`.

### `update`

```json
{"entity": "good", "id": 5, "data": {"price": 120}}
{"entity": "good", "ids": [5,6], "data": {"published": 1}}
{"entity": "good", "where": {"rubricator_id": 5}, "data": {"published": 0}}
```

Меняются только переданные поля. Ответ: `{"updated": N, "ids": [...]}`.
Под условие должно попадать не более 500 записей.

### `replace` (upsert по естественному ключу)

```json
{"entity": "good", "data": {"artikul": "A-1", "header": "Товар", "price": 100}}
{"entity": "params_catalog",
 "items": [{"param_id": 1, "catalog_id": 2, "value": "…"}]}
```

Ищет строку по `natural_key` (см. `info`): нашлась — обновляет переданные поля,
нет — вставляет. `DELETE+INSERT` сознательно не используется — потомки не
должны уходить каскадом. Ответ: `{"ids": [...], "inserted": N}`.

### `delete`

```json
{"entity": "good", "ids": [5,6]}
{"entity": "catalog", "where": {"parent_id": 5}, "recursive": true}
```

Ответ: `{"deleted": N, "ids": [...]}`. Для `ds_good` подчищаются галерея
(`ds_good_galery`), характеристики (`ds_params_good`) и ЧПУ. Для дерева
(`catalog`, `top_menu`, `bottom_menu`) потомки удаляются **только** при
`"recursive": true`; глубина дерева ограничена 5.

### `upload`

`multipart/form-data`, ключ — в заголовке.

| Поле | Смысл |
|---|---|
| `file` | файл (обязателен) |
| `target` | цель: `catalog`, `wysiwyg` или `entity.field` (`good.photos`, `doc.attach`) |
| `entity`, `field` | альтернатива `target` |
| `ref_id` | id записи: файл сразу привязывается (колонка или строка галереи) |

Имя файла генерирует сервер (`<время>_<2 символа>`), исходное сохраняется как
`orig_name`. Тип определяется по содержимому (Pillow), для документов —
белый список расширений. Лимиты: 15 МБ, 40 Мпикс. Изображения конвертируются
в webp и нарезаются по пресетам цели. Ответ:

```json
{"file": "…", "url": "/files/project_5837/good/…webp",
 "attachment": {"column": "photo", "value": "…"}}
```

### `delete` / прочие методы

Неизвестный метод → `404` с `code: not_found`.

## WHERE-условия

`where` — объект `{колонка: значение}`. Значения-объекты задают операторы:

| Оператор | SQL | Пример |
|---|---|---|
| (число/строка) | `=` | `{"published": 1}` |
| `null` | `IS NULL` | `{"brand": null}` |
| `in` | `IN` | `{"id": {"in": [1,2,3]}}` |
| `ne` | `<>` | `{"published": {"ne": 0}}` |
| `gt`, `gte` | `>` `>=` | `{"price": {"gte": 100}}` |
| `lt`, `lte` | `<` `<=` | `{"price": {"lt": 1000}}` |

Запрещены в `where` (и не принимаются в `data`): `project_id`, первичный ключ и
скрытые колонки. В `in` — не более 500 значений. `where`, попадающий более чем
на 500 записей в `update`/`delete`, отклоняется.

## Сущности

| `entity` | Таблица | Ключ (`nk`) | Особенности |
|---|---|---|---|
| `good` | `ds_good` | `artikul` | фото (`photos`), характеристики (`params`), ЧПУ `/good/`, бренд, рубрика |
| `good_photos` | `ds_good_galery` | — | фотографии товара |
| `catalog` | `ds_catalog` | `header` | дерево (`parent_id`), характеристики рубрик, ЧПУ `/catalog/` |
| `params` | `ds_params` | `header` | справочник характеристик |
| `params_catalog` | `ds_params_catalog` | `param_id`,`catalog_id` | характеристика ↔ рубрика |
| `params_good` | `ds_params_good` | `param_id`,`good_id` | значение характеристики товара |
| `brands` | `ds_brands` | `name` | логотип |
| `news` | `ds_news` | `header` | фото, ЧПУ `/news/` |
| `article` | `ds_article` | `header` | фото, ЧПУ `/article/` |
| `service` | `ds_service` | `header` | дерево (`parent_id`), ЧПУ `/service/` |
| `text` | `ds_text` | `url` | текстовые страницы |
| `slider` | `ds_slider` | — | слайды главной |
| `advantages` | `ds_advantages` | — | иконки (без webp) |
| `employee` | `ds_employee` | — | сотрудники |
| `clients` | `ds_clients` | — | клиенты |
| `reviews` | `ds_reviews` | — | отзывы |
| `certificates` | `ds_certificates` | — | сертификаты |
| `galery` | `ds_galery` | — | фотогалерея |
| `video` | `ds_video` | — | видео |
| `doc` | `ds_doc` | — | вложения (`docs`) |
| `filials` | `ds_filials` | — | филиалы |
| `top_menu` / `bottom_menu` | `ds_top_menu` / `ds_bottom_menu` | — | дерево (`parent_id`) |
| `const` | `const` | `name` | **только чтение** (запись сломала бы сайт/ключ) |

Полный перечень с полями — из `POST /api/v1/info` (или из `DESC`-схемы).
Служебные таблицы API не отдаёт никогда: `ds_zakaz`, `ds_zakaz_good`,
`ds_form_submit`, `capture`, `manager`, `manager_session`, `domain`, `project`.

## Загрузка файлов: цели (`target`)

| `target` | Папка в `files/project_<id>` | Флаги |
|---|---|---|
| `good_galery` | `good_galery` | webp + миниатюры, строка галереи |
| `catalog` | `catalog` | webp + миниатюры |
| `articles` / `services` | `articles` / `services` | webp + миниатюры |
| `slider` | `block-images/slider` | webp + миниатюры |
| `employee`, `clients`, `certificates`, `galery`, `brands` | одноимённая | webp |
| `advantages` | `advantages` | без webp (svg/png иконки) |
| `docs` | `docs` | документы (pdf/офис/архивы) |
| `wysiwyg` | `wysiwyg` | картинки для wysiwyg-полей, без привязки к записи |

## Лимиты

| Параметр | Значение |
|---|---|
| `select.limit` | по умолчанию 50, максимум 500 |
| `insert.items` | ≤ 100 строк |
| `update`/`delete` | ≤ 500 записей |
| `where.in` | ≤ 500 значений |
| глубина дерева | ≤ 5 |
| файл | ≤ 15 МБ, ≤ 40 Мпикс |

## Статистика и журнал

Каждый вызов (кроме `ping`) пишется в статистику и журнал (`db/migrate_ds_api.py`):

- агрегат по методу/суткам: количество, успешные/неуспешные, строки, байты;
- журнал последних запросов: время, метод, сущность, маска ключа, IP, превью
  тела (усечено), код/текст ошибки, длительность.

Панель `/vue/ds-api` показывает статистику за период, журнал и позволяет
создать/сменить ключ, задать scopes/лимиты/IP. Сам ключ в статистике и журнале
никогда не показывается целиком — только маска.

## Проверка вручную

```bash
# ключ для проекта 5837 (dev)
KEY=$(cat /tmp/k5837.txt)

# список сущностей
curl -s -X POST http://localhost:3010/api/v1/info -H "X-API-Key: $KEY" | head -c 400

# чтение
curl -s -X POST http://localhost:3010/api/v1/select -H "X-API-Key: $KEY" \
  -H 'Content-Type: application/json' \
  -d '{"entity":"catalog","with":{"params":true},"limit":3}'

# запись (нужен scope insert)
curl -s -X POST http://localhost:3010/api/v1/insert -H "X-API-Key: $KEY" \
  -H 'Content-Type: application/json' \
  -d '{"entity":"brands","data":{"name":"Тестовый бренд"}}'
```
