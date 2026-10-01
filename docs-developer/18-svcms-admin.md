# 18. Панель SV-CMS admin

Глобальная админка (админы, проекты, домены, шаблоны) на конфиге
`config_svcms_admin`, деплой `~/svcms/admin/frontend` (фронт `svcms.admin`,
`vite build --mode default`, `base: '/'`).

Запуск:

```bash
start/svcms_admin.sh
# или
export config=config_svcms_admin && .venv/bin/uvicorn --reload --port=5000 --workers 1 main:app
```

> Запускать **только из корня репозитория** (`lib/engine.py:9` захватывает
> `os.getcwd()` для debug-обхода авторизации).

## Ключевые моменты конфига

| Ключ | Значение | Почему |
|---|---|---|
| `BaseUrl` | `''` | фронт админки отдаётся с корня домена |
| `controllers.left_menu` | `/svcmsadmin/left-menu-admin` | меню из `admin_menu_new` |
| `config_folder` | `configs/svcmsadmin` | папка инструментов админки |
| `encrypt_method` | `mysql_encrypt` | пароли админов хранятся в старом MySQL `ENCRYPT` |
| `auth.manager_table` | `admin` | таблица админов |
| `auth.manager_table_id` | `admin_id` | |
| `auth.session_table` | `admin_session` | |
| `auth.session_fails_table` | `admin_session_fails` | |
| `after_create_engine` | своя функция | `read_config` всегда читает `request.state.project['project_id']` |

`after_create_engine` обязателен, иначе любой инструмент падает:

```python
async def after_create_engine(s, request, errors=[]):
  if not getattr(request.state, 'project', None):
    request.state.project = {'project_id': None, 'template_id': None, 'access_for_cur_domain': 1}
```

`after_all_change_action` — заглушка (сброс кэша клиентских сайтов здесь не нужен).

## Контроллер меню

`routes/svcmsadmin/left_menu_admin.py` — `GET /svcmsadmin/left-menu-admin`.
Читает `admin_menu_new` (только `enabled=1`), собирает дерево по `parent_id` и
отдаёт фронтовый формат (см. [17-frontend-contract.md](17-frontend-contract.md)):

```json
{"left_menu":[{"id":2,"header":"Сайты","type":"vue","value":"",
  "params":{},"icon":"fas fa-folder","child":[...]}],
 "manager":{"id":51,"login":"naumov"},"errors":[],"success":1}
```

## `admin_menu_new` и миграция

Старая таблица `admin_menu` хранила только `name/config_name/url` — фронт это
не понимает. Поэтому заводится `admin_menu_new`:

```sql
CREATE TABLE admin_menu_new (
  id int unsigned NOT NULL AUTO_INCREMENT,
  header varchar(255) NOT NULL,
  type varchar(20) NOT NULL DEFAULT 'vue',   -- vue | src | newtab
  value varchar(255) NOT NULL DEFAULT '',    -- admin-table | admin-tree | const
  params text,                               -- JSON, например {"config":"project"}
  icon varchar(100) NOT NULL DEFAULT '',
  parent_id int unsigned DEFAULT NULL,
  path varchar(255) NOT NULL DEFAULT '',
  sort int unsigned NOT NULL DEFAULT 1,
  enabled tinyint unsigned NOT NULL DEFAULT 1,
  legacy_id int unsigned DEFAULT NULL,
  PRIMARY KEY (id), KEY parent_id (parent_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

Миграция: `db/migrate_admin_menu_new.py`

```bash
config=config_svcms_admin .venv/bin/python db/migrate_admin_menu_new.py
```

Правила переноса (`map_row`):

- `admin_table.pl?config=X` → `admin-table` + `{"config":"X"}`;
- `admin_tree.pl?config=X` → `admin-tree` (кроме плоских — см. ниже);
- `admin_menu` → всегда `admin-tree` (единственное настоящее дерево);
- `landing_block_type` / `landing_block_options` → `admin-table` (плоские списки);
- строки-категории (пустой `url`/`config_name`) → узлы-группы;
- старые perl/утилиты (`fast_create.pl`, `template_editor/navigator.pl`,
  `construct/construct.pl`, `zpa.pl`, `tools/*`) → `enabled=0`.

Поле `path` заполняется как путь родителя (`''` для корней, `/<parent_id>` для
детей) — нужно для `AdminTree`.

## Инструменты `configs/svcmsadmin/`

Портированы все legacy-конфиги (54 папки): `admin`, `admin_group`, `admin_menu`,
`manager`, `project`, `domain` (с DNS `1_to_m`), `template`, `const`, `content`,
`struct*`, `bot`/`bot_rules`, `works`/`workers`/`work_types`, `landing_block*`,
`form_*`, `adm_*`, `good`, `rubricator` и т.д.

Список в меню (включённые пункты `admin_menu_new`) ссылается на конфиги через
`params.config`; `admin_menu` — единственный `admin-tree`.

## Таблицы для дампа

Часть legacy-таблиц отсутствует в dev-БД; для полноценной работы их дампят с
прод-стенда и импортируют:

```bash
ssh -p7725 naumov@178.57.220.192 'mysqldump -u svcms --no-tablespaces --force --single-transaction svcms \
  adm_client adm_client_add_balance adm_client_service adm_money adm_purse adm_service \
  adm_task adm_task_attach bot bot_rules bot_rules_webapp buzy_dns capture_setting \
  content design design_img domain_dns_records_a domain_dns_records_cname \
  domain_dns_records_mx domain_dns_records_ns domain_dns_records_txt \
  fast_rule for_robots form_data form_field_types form_form_fields form_forms good group2admin \
  landing_block landing_block_type landing_block_options landing_block_options_sub \
  landing_block_subvars landing_block_tmpl_opt manager_menu manager_menu_icons \
  otdels otr otrasl project_1_comp project_group_site project_hosting project_menu \
  project_permission promo pxls redirect rkn_template rubricator rubricator_good \
  site_redirect struct struct_1_region struct_42_comp template_group_promoblock \
  url_generator wikidict work_type_coef work_types worker_oklads worker_percent \
  worker_plan workers works' | mysql -u svcms svcms
```

На проде **тоже отсутствуют** `adm_*`, `design`, `project_1_comp`,
`struct_42_comp`, `for_robots` — соответствующие конфиги не задействованы в меню.

## Проверка

```bash
curl -s http://dev-crm.test/backend/startpage
curl -s http://dev-crm.test/backend/svcmsadmin/left-menu-admin
curl -s -X POST http://dev-crm.test/backend/get-filters/admin_menu -H 'Content-Type: application/json' -d '{}'
curl -s -X POST http://dev-crm.test/backend/admin-tree/admin_menu -H 'Content-Type: application/json' -d '{}'
```

Всё должно вернуть `success: 1` (или `success: true` для `startpage`).
