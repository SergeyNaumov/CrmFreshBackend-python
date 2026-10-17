# Панель SV-CMS admin (`config_svcms_admin`)

Глобальная админка (админы, проекты, домены, шаблоны). Запуск:
`start/svcms_admin.sh` (`export config=config_svcms_admin && .venv/bin/uvicorn
--reload --port=5000 --workers 1 main:app`). Только из корня репозитория.

Разбор для разработчиков — `docs-developer/18-svcms-admin.md`.

## Конфиг

`config_svcms_admin.py`:

- `BaseUrl:''` (фронт с корня домена); `system_url` adminbot;
- `controllers.left_menu = '/svcmsadmin/left-menu-admin'`;
- `config_folder = 'configs/svcmsadmin'`;
- `use_project:False`, но `after_create_engine` ставит `request.state.project`
  (иначе `read_config` падает);
- авторизация: `manager_table='admin'`, `manager_table_id='admin_id'`,
  `session_table='admin_session'`, `session_fails_table='admin_session_fails'`,
  `encrypt_method='mysql_encrypt'` (пароли админов — старый MySQL `ENCRYPT`),
  `use_permissions:False`;
- `after_all_change_action` — заглушка (см. `config_svcms_admin.py`).

> `request.state.project['project_id']` читается в `lib/all_configs.py`
> безусловно → админке нужен `after_create_engine` (или фикс инициализации
> `form` в `read_config`, уже сделан).

## Меню

`routes/svcmsadmin/left_menu_admin.py` — `GET /svcmsadmin/left-menu-admin`:
читает `admin_menu_new` (`enabled=1`), строит дерево по `parent_id`, парсит
`params` (JSON) и отдаёт фронтовый формат. Регистрация:
`routes/__init__.py` (`router_svcmsadmin`, prefix `/svcmsadmin`).

## `admin_menu_new`

Формат фронтового меню: `header, type(vue|src|newtab),
value(admin-table|admin-tree|const|…), params(JSON), icon, parent_id, path,
sort, enabled, legacy_id`.

Миграция `db/migrate_admin_menu_new.py` (пересоздаёт таблицу, читает
`admin_menu`):

- `admin_table.pl?config=X` → `admin-table` + `{"config":"X"}`;
- `admin_menu` → `admin-tree` (единственное настоящее дерево);
- `landing_block_type`/`landing_block_options` → `admin-table` (плоские списки);
- категории (пустой `url`/`config_name`) → группы;
- старые perl/утилиты (`fast_create.pl`, `template_editor/navigator.pl`,
  `construct/construct.pl`, `zpa.pl`, `tools/*`) → `enabled=0`.

Запуск: `config=config_svcms_admin .venv/bin/python db/migrate_admin_menu_new.py`.

## Инструменты

`configs/svcmsadmin/` — 54 папки, портированы все legacy-конфиги:
`admin`, `admin_group`, `admin_menu`, `manager`, `project`, `domain` (DNS
`1_to_m`), `template`, `const`, `content`, `struct*`, `bot`/`bot_rules`,
`works`/`workers`/`work_types`, `landing_block*`, `form_*`, `adm_*`, `good`,
`rubricator`, `permissions` и т.д. В меню ссылки через `params.config`.

### Vue-инструменты (страницы `/vue/...`)

Инструмент-страница (а не карточка-форма) подключается четырьмя шагами:

1. бэкенд-роутер — `routes/svcmsadmin/<tool>.py` + `include_router` в
   `routes/svcmsadmin/__init__.py`;
2. компонент — `src/components/svcmsAdmin/<Tool>.vue`;
3. маршруты — `src/router/index.js`: shell `/vue/<tool>` и full-screen
   `/<tool>` (`meta:{blank:true}`);
4. пункт меню — строка в `admin_menu_new` (`type='vue'`, `value='<tool>'`,
   `parent_id/path/sort`, `enabled=1`) + маппинг `value → URL` в
   `src/LeftMenu.vue::get_link`.

Долгие операции идут **фоновой задачей** (`lib/background`: `register_task` +
`enqueue`), фронт показывает прогресс через `WS /background/ws/{id}` и поллинг
`GET /background/status/{id}`.

| Инструмент | Файлы | Что делает |
|---|---|---|
| Создание проекта | `routes/svcmsadmin/project_create.py`, `CreateProject.vue`, `admin_menu_new.value='svcmsadmin-createproject'` | Режимы «новый»/«на базе существующего», DS-конструктор, опции, порт, менеджер; задача `project_create` |
| Перенос на другой домен | `routes/svcmsadmin/domain_sync.py` + `domain_scope.py`, `DomainSync.vue`, `admin_menu_new.value='svcmsadmin-domainsync'` | Копирование/перенос настроек конструктора между доменами; задача `domain_sync` |
| Клонирование проекта (легаси) | `project_clone.py`, `ProjectClone.vue` | Старый клон: свой `template` + папка + `template_const`/`url_run_code`/`url_rules`; задача `project_clone` |
| Структуры / экспорт / sitemap | `project_struct.py`, `project_export.py`, `project_sitemap.py` (+ компоненты) | Уникальные структуры, выгрузка проекта, карта сайта |

### Поля-компоненты в карточках

Поле конфига с типом-компонентом (`project_clone`, `project_export`,
`project_struct`, `project_sitemap`, `domain_sync`, `page_blocks`) — виртуальное:
в БД не сохраняется, а рендерится Vue-компонентом. Цепочка:
`configs/.../<field>.type` → `EditForm/FormBlock.vue` (`case '<type>'` →
`field-<type>`) → `src/dynamic_component_loader.js`
(`app.component('field-<type>', defineAsyncComponent(...))`). Компонент получает
пропсы `form` и `field`; `form.id` — id записи (`work_table_id`), напр. в
карточке домена это `domain_id`.

### «Перенос на другой домен» (`domain_sync`)

Настройки конструктора привязаны к **`domain_id`** (домен = сайт), а рантайм
DS-сайтов — к `project_id` (systemd `svcms.sites<id>`); домен запроса движок
выбирает по `Host`. Инструмент переносит/копирует доменные данные на другой
домен — существующий или только что созданный.

| Method | Path | Параметры | Ответ |
|---|---|---|---|
| GET | `/domain/sync/preview` | `src_domain_id`, `dst_domain_id?` | `{success, src, dst, src_counts, dst_counts, warnings}` |
| POST | `/domain/sync/start` | `{src_domain_id, mode:'copy'\|'move', dst_domain_id?, new_domain?, new_folder?, template_mode:'inherit'\|'clone', parts?, pages_mode:'replace'\|'merge', delete_old?, port?}` | `{success, task_id}` |

Логика (`domain_scope.py` — общий слой, им же пользуется клонирование проекта):

- **Конструктор** (`template.type=6`): `domain_page`, `domain_constructor`,
  `domain_theme_*` (только доменные, `domain_id>0`), `domain_rkn`.
  `copy` → `INSERT … SELECT` (страницы: `replace` чистит приёмник, `merge` —
  `INSERT IGNORE`); `move` → `UPDATE domain_id` (приёмник предварительно
  очищается). Новый домен наследует общий `template_id`.
- **Обычные проекты** (`template.type≠6`): конструкторских таблиц нет — копируются
  `domain_rkn`, `project_hosting`, `domain_dns_records_*`, `for_robots_id`; при
  `template_mode='clone'` создаётся отдельная запись `template` (папка
  `new_folder`) с `template_const`/`url_run_code`/`url_rules` и копией папки на
  диске (`paths.templates`).
- Новый домен создаётся копией полей источника (`project_id`, `template_id`,
  `server_type`, `not_cache_nginx`, `is_adaptive`, `user_id`, …); для
  `server_type=4` — свободный порт; SSL-поля сбрасываются,
  `need_clean_cache=1`.
- `move` отказывается работать, если у приёмника уже есть данные конструктора;
  `delete_old` доступен только при `move`. Транзакций в db-слое нет → при
  ошибке выполняется компенсация (перенесённое возвращается, созданный домен и
  `template` удаляются).
- Вне БД остаётся: DNS, SSL, vhost nginx, сброс кэша. Старый домен выводится из
  обслуживания через `project_hosting.disabled=1` («Сайт выключен!»); редиректа
  301 old→new в движке нет.

Данные конструктора — `routes/svcmsadmin/page_constructor/TABLES.md`.

## Таблицы

Часть legacy-таблиц пришлось дампить с прод-стенда
(`ssh -p7725 naumov@178.57.220.192 ... | mysql -u svcms svcms`). Список и
команда — `docs-developer/18-svcms-admin.md`. На проде отсутствуют `adm_*`,
`design`, `project_1_comp`, `struct_42_comp`, `for_robots` — их конфиги не
задействованы.

Дев-БД **неполная** относительно прода: 106 «общих» таблиц есть на проде и нет
локально (мультитенантные `struct_<pid>_*` не считаем). Для инструментов клона
нужны три из них — `portfolio`, `service_rubricator`, `left_menu_tree`
(перечислены в `COLS`/`CLONE_COLS`, `routes/svcmsadmin/project_clone.py`); без
них `SHOW COLUMNS` сыпет ошибками. Структуру брали с прода:

```bash
# 1) DDL с прода (структура, без данных)
ssh -p 7725 naumov@178.57.220.192 \
  'for t in portfolio service_rubricator left_menu_tree; do
     mysql -h 185.76.252.12 -u svcms -N -e "SHOW CREATE TABLE $t\G" svcms; done' \
  > /tmp/missing_ddl.sql
# 2) применить локально (в MySQL 8 у text/longtext снять DEFAULT NULL,
#    AUTO_INCREMENT — с 1)
mysql -u svcms svcms < /tmp/missing_ddl.sql
```

Проверка: `SHOW COLUMNS FROM portfolio` (11 колонок), `service_rubricator` (14),
`left_menu_tree` (7).

## Деплой (прод)

Админка живёт на web-хосте `naumov@178.57.220.192:7725` (там же движок сайтов и
менеджер); фронт — `admin3.design-b2b.com`:

| Слой | Локально | Прод |
|---|---|---|
| Фронт | `~/projects/CrmFreshFront` | `/var/www/svcms/admin/frontend` (root vhost `admin3.design-b2b.com`) |
| Бэкенд | `~/projects/CrmFreshBackend-python-async` | `/var/www/svcms/admin/backend` (сервис `svcms.admin`, `uvicorn main:app --port=3011`) |
| API | `http://dev-crm.test/backend` | `https://admin3.design-b2b.com/backend/` → nginx `location /backend/` → `127.0.0.1:3011/` |

```bash
# фронт (сборка + rsync dist/ в /var/www/svcms/admin/frontend)
cd ~/projects/CrmFreshFront && ./build/svcms.admin

# бэкенд: configs/svcmsadmin/ → conf/, lib/, routes/, db/ (rsync --delete)
cd ~/projects/CrmFreshBackend-python-async && printf 'n\n' | bash sync/svcmsadmin.py
sudo -n systemctl restart svcms.admin      # или дождаться --reload

# проверка
sudo -n systemctl is-active svcms.admin
curl -m 8 -k -s -o /dev/null -w '%{http_code}\n' \
  -H 'Host: admin3.design-b2b.com' https://127.0.0.1/backend/svcmsadmin/project/create/init
```

Особенности:

- `sync/svcmsadmin.py` **не** синкает `config.py` (серверный: на проде
  `connects.*.host=185.76.252.12`) и не трогает `files` (на проде это симлинк);
  перед прогоном полезно смотреть dry-run: `rsync -avzn --delete …`.
- Зависимости бэкенда — `requirements.txt`; при появлении нового импорта его
  нужно поставить в прод-venv (`.venv3.11`), иначе воркер падает и порт не
  отвечает. Уже наступали: `routes/parser_excel/*` требует `openpyxl` (и
  `xlrd`) — `pip install openpyxl==3.1.5`.
- Правки движка сайтов деплоятся отдельно (`svcms-async/tools/sync_engine_to_prod.sh`
  или точечным `rsync` файла); `sites/lib/config.py` там **исключён** — он
  серверный (см. `agent-doc/18_prod_runtime.md` в репо `svcms-async`).

## Проверка

```bash
curl -s http://dev-crm.test/backend/startpage
curl -s http://dev-crm.test/backend/svcmsadmin/left-menu-admin
curl -s -X POST http://dev-crm.test/backend/admin-tree/admin_menu -H 'Content-Type: application/json' -d '{}'
```
