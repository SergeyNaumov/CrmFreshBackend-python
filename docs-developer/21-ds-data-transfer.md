# Импорт/экспорт данных проекта (ds-data)

Инструмент менеджера для переноса данных DS-проекта (таблицы `ds_*`, `const`)
и файлов `files/project_<id>` между проектами одним zip-архивом. Отдельные
инструменты-парсеры Excel описаны в `20-excel-import.md` — это другой
механизм (парсер по конфигу). Здесь перенос «как есть», таблицами.

## Где живёт

| Файл | Назначение |
|---|---|
| `lib/svcmsmanager/ds_data_transfer.py` | реестр таблиц + константы формата |
| `lib/svcmsmanager/ds_data_export.py` | сборка архива, задача `svcmsmanager/project_export` |
| `lib/svcmsmanager/ds_data_import.py` | dry-run + импорт, задача `svcmsmanager/project_import` |
| `routes/svcms/data_transfer.py` | HTTP-эндпоинты, очистка `files/tmp` |
| `routes/svcms/left_menu.py` | пункт меню `value='ds-data'` |
| `CrmFreshFront/src/components/svcmsManager/ProjectDataTransfer.vue` | интерфейс |
| `CrmFreshFront/src/router/index.js` | маршруты `/vue/ds-data`, `/ds-data` |

## Эндпоинты

Все под `/svcms`, обычный конверт `{success, errors}` (HTTP всегда 200).

| Метод | Путь | Тело / ответ |
|---|---|---|
| GET | `/svcms/data/tables` | список таблиц проекта: `table`, `title`, `rows`, `natural_key`, `service` |
| POST | `/svcms/data/export/start` | `{tables:[...]}` → `{task_id}` |
| POST | `/svcms/data/import/preview` | multipart `file` (`.zip`) → dry-run план + `import_id` |
| POST | `/svcms/data/import/start` | `{import_id, mode}` → `{task_id}`, `mode`: `replace`\|`merge` |

Прогресс — стандартный каркас `lib/background.py`:
`GET /background/status/{task_id}`, WS `/background/ws/{task_id}`.

## Формат архива

```
manifest.json          # format, format_version, created, source_project_id, tables, files
data/<table>.json      # {"table":..., "columns":[...], "rows":[...]}
files/<путь>           # содержимое files/project_<src> БЕЗ сегмента project_<src>
```

- `format = "ds-project-data"`, `format_version = 1`. Импорт отклоняет
  незнакомый `format` и версию выше поддерживаемой.
- **`project_id` в строки не пишется.** Целевой проект известен по домену
  (`after_create_engine`), архив переносим между проектами.
- **Исходный `id` сохраняется**, но при импорте INSERT идёт **без `id`**:
  `id` нужен только как ключ для ремапа ссылок (`refs`), т.к. AUTO_INCREMENT
  в другом проекте другой.
- Файлы упаковываются целиком, **включая ресайзы** (`_mini1..3`) — архив
  подходит для быстрого восстановления без пересборки через PIL.

## Реестр таблиц

Единственное место, где описаны переносимые таблицы, — `TABLES` в
`ds_data_transfer.py`. Запись на таблицу:

| Поле | Назначение |
|---|---|
| `order` | порядок вставки (родители раньше детей: `ds_params` → `ds_catalog` → ... → `ds_good` → `ds_good_galery`) |
| `title` | человеческое название для интерфейса |
| `natural_key` | ключ поиска существующей строки в режиме `merge`; пустые значения ключа → строка вставляется, а не ищется |
| `parent_col` | самоссылка (дерево): вставка в два прохода |
| `refs` | ссылки на другие таблицы: `колонка -> таблица` (ремап id) |
| `upsert` | вставка через `ON DUPLICATE KEY` (`const` по `(name, project_id)`) |
| `service` | служебная таблица: по умолчанию не выгружается |
| `project_col` / `where_tpl` | выборка строк (по умолчанию `project_id=%s`; `ds_zakaz_good` — через подзапрос по `zakaz_id`) |

`FILE_COLS` (там же) — колонки файла → папка внутри `files/project_<id>`
(нужна для сверки/счётчика файлов; сами файлы копируются целиком).

Отдельно в реестре есть не-`ds_*` таблица `files` («Файлы для поисковиков»,
`order=185`, `natural_key=['url']`): произвольные файлы домена (`/robots.txt`,
`/sitemap.xml`, `/AGENTS.md`, …), которые движок отдаёт из БД. Содержимое
хранится в БД, поэтому переносится вместе с проектом; файлы на диске
(`files/project_<id>/`) тут не при чём.

Порядок, `natural_key` и `refs` выведены из реальной схемы БД
(`SHOW CREATE TABLE`) и конфигов `configs/svcmsmanager/ds_*`:
`ds_good.rubricator_id → ds_catalog.id`, `ds_good.brand → ds_brands.id`,
`ds_good_galery.good_id → ds_good.id`, `ds_params_*.* → ds_params/ds_catalog/ds_good`,
`ds_zakaz_good.* → ds_zakaz/ds_good`. Деревья `parent_id` — у `ds_catalog`,
`ds_service`, `ds_top_menu`, `ds_bottom_menu`.

## Режимы импорта

| Режим | Поведение |
|---|---|
| `replace` | очистка строк выбранных таблиц проекта (в обратном порядке вставки) + вставка из архива |
| `merge` | без удаления: поиск по `natural_key` → `UPDATE`, иначе `INSERT` |

- Таблицы без `natural_key` (например `ds_news`) в `merge` вставляются
  заново — повторный импорт дублирует строки. Это осознанно: ключа дедупликации нет.
- Разрешение ссылок при импорте — цепочка: карта вставленных строк
  (`src_id → new_id`) → натуральный ключ источника в целевой БД → прямое
  совпадение `id` в проекте (с предупреждением) → сброс значения (NULL/0 + предупреждение).
- Тексты: пути `/files/project_<src>/` → `/files/project_<dst>/` (регулярно, по всем строковым значениям).

## Транзакция и файлы

Импорт — **одна** DB-транзакция через `db.pool.acquire()` (ручной
COMMIT/ROLLBACK). Файлы распаковываются в `files/tmp/`, сверяются по md5 и
подменяются в `files/project_<dst>/` **только после COMMIT**. При ошибке БД —
откат, файлы проекта не тронуты.

- `replace`: существующие файлы перезаписываются.
- `merge`: файл с тем же именем, но другим содержимым **не перезаписывается**
  (счётчик `conflicts`), чтобы не испортить чужой контент проекта.
- Совпадающие по md5 файлы пропускаются (`skipped_same`).

После успеха — `clear_cache_for_domain(host)` (сброс memcached сайта).

## Защита

- Только `.zip`; лимит загрузки 600 МБ (`MAX_UPLOAD`).
- Zip-slip: отклоняются пути с `..`, абсолютные и с буквой диска.
- Проверка `format`/`format_version` манифеста.
- `import_id` — только `[a-zA-Z0-9_-]`, файл должен существовать.
- Очистка `files/tmp`: `ds_import_*.zip` — через 24 ч, `ds_data_export_*.zip` —
  через 7 дней; «ленивая», при следующем экспорте/загрузке (cron на хосте нет).

## Чек-лист: добавили новую структуру `ds_*`

1. Создали таблицу + конфиг в `configs/svcmsmanager/<table>/`.
2. **Прописали таблицу в `lib/svcmsmanager/ds_data_transfer.py`** (иначе в
   экспорт/импорт она не попадёт):
   - `title` — человеческое название;
   - `order` — позиция вставки (родители раньше детей);
   - `natural_key` — если у таблицы есть осмысленный ключ для `merge`
     (иначе `None`);
   - `parent_col='parent_id'` — если это дерево;
   - `refs={колонка: таблица}` — для каждой ссылки на другую таблицу;
   - `file_cols` в `FILE_COLS` — если есть колонки файла;
   - `service=True` — если данные служебные/персональные (по умолчанию не выгружаются);
   - для таблицы без колонки `project_id`: `project_col=''` + `where_tpl`.
3. Проверили: экспорт проекта → импорт в тестовый проект (`replace` и `merge`)
   → 0 битых ссылок (`LEFT JOIN` по `refs`), пути `/files/project_<dst>/`
   переписаны, файлы на месте.

## Тестирование

Запуск только из корня репозитория:

```bash
export config=config_svcms_manager && .venv/bin/uvicorn --reload --port=5000 --workers 1 main:app
```

Dev-обход авторизации: заголовок `Host: dev-crm.test` (проект 5844).
Проверяется `curl`-ом: `/svcms/data/tables`, экспорт → статус задачи →
скачивание `/download_tmp/<file>`, `import/preview` (план), `import/start`.
Юнит-тестов в проекте нет — проверка на реальном uvicorn.
