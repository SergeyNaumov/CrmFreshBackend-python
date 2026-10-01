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

## Таблицы

Часть legacy-таблиц пришлось дампить с прод-стенда
(`ssh -p7725 naumov@178.57.220.192 ... | mysql -u svcms svcms`). Список и
команда — `docs-developer/18-svcms-admin.md`. На проде отсутствуют `adm_*`,
`design`, `project_1_comp`, `struct_42_comp`, `for_robots` — их конфиги не
задействованы.

## Проверка

```bash
curl -s http://dev-crm.test/backend/startpage
curl -s http://dev-crm.test/backend/svcmsadmin/left-menu-admin
curl -s -X POST http://dev-crm.test/backend/admin-tree/admin_menu -H 'Content-Type: application/json' -d '{}'
```
