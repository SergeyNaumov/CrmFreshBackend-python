# Контракт с фронтендом (CrmFreshFront)

Фронт — отдельный репозиторий `~/projects/CrmFreshFront` (Vue 3 + Vite +
Vuetify 3). Конфиг бэкенда — это **схема администрируемой таблицы**, из которой
фронт рендерит AdminTable / AdminTree / EditForm / Const. Фоновые скрипты в
конфиге не описываются.

Пользовательская версия с примерами и скринами —
`docs-developer/17-frontend-contract.md`.

## Левое меню

`GET {BackendBase}<left_menu_controller>` → `{left_menu:[...], manager, success}`.

Пункт: `{header, type, value, params, icon, child[], id}`.

| `type`/`value` | Роут фронта | Компонент |
|---|---|---|
| `vue` + `admin-table` | `/vue/admin_table/<params.config>` | `AdminTable.vue` |
| `vue` + `admin-tree` | `/vue/admin_tree/<params.config>` | `AdminTree.vue` |
| `vue` + `const` | `/vue/const/<params.config>` | `Const.vue` |
| `src` | — | произвольная страница |
| `newtab` | URL | новая вкладка |

См. `src/App.vue`, `src/LeftMenu.vue`, `src/components/left_menu_item.vue`,
`src/router/index.js`.
Для `config_svcms_admin` меню генерирует `routes/svcmsadmin/left_menu_admin.py`
из `admin_menu_new` (см. `15-svcms-admin.md`).

## AdminTable (список)

- `POST /get-filters/<config>` → `{title, filters, permissions, search_plugin, log, errors}`.
- `POST /get-result` `{config, query, params}` → `{results:{headers, output,...}, errors}`.
- Фильтры: `src/components/AdminTable/OnFilters.vue`; результаты:
  `AdminTable/FindResults.vue`.
- Бэкенд: `routes/get_filters_routes.py`, `routes/get_result_routes.py`,
  `routes/get_result/process_result_list.py`.
- Особенность фронта (`AdminTable.vue:333-341`): фильтр `checkbox`/`switch` без
  `values` → `select` «Не использовать/Да/Нет».

## AdminTree (дерево/галерея)

- `GET`/`POST /admin-tree/<config>` → `{form, tree, log, errors}`.
- `form.*`: `title, config, header_field, tree_use, sort, sort_field, max_level,
  not_create, read_only, make_delete, changed_in_tree, view_type ('gallery'),
  cols, wide_form, card_format`.
- `item.*`: `id, header, sort, childs, photo`.
- Действия: `add_branch_plain`, `delete_branch`, `move`, `sort`, `get_branch`,
  `load_many_childs`.
- Бэкенд: `routes/admin_tree_routes.py`, `routes/admin_tree/admin_tree_run.py`;
  фронт: `src/components/AdminTree.vue`, `AdminTree/branch.vue`,
  `AdminTree/FormInBranch.vue`.
- Для дерева нужны колонки `parent_id` (+ `path` при `tree_use`), сортировка —
  по `sort_field`.

## EditForm (карточка)

`FormBlock.dynamic_component` (`src/components/EditForm/FormBlock.vue:117`)
отображает `type` → компонент:

| type | компонент |
|---|---|
| `text`,`textarea` | `field-text` |
| `checkbox`,`switch`,`1_to_1_checkbox` | `field-checkbox` |
| `select` (в т.ч. из select_*) | `field-select` |
| `multiconnect` | `field-multiconnect` |
| `date`,`time`,`datetime`,`yearmon`,`daymon` | `field-<type>` |
| `wysiwyg` | `field-wysiwyg` |
| `password` | `field-password` |
| `code` | `field-code` |
| `memo` | `field-memo` |
| `1_to_m` | `field-1_to_m` |
| `file` | `field-file` |
| `docpack` | `field-docpack` |
| `in_ext_url` | `field-in_ext_url` |
| `time_table` | `field-time_table` |
| `font-awesome` | `field-font-awesome` |
| `component` | `field-component` |
| `accordion` | `field-accordion` |
| `project_sitemap`/`export`/`clone`/`struct` | `field-project_*` (svcms) |

Префикс `1_to_1_` отбрасывается. Компонента для `filter_extend_*` нет → поле не
рисуется. `field-chart`/`field-table` работают только внутри `field-accordion`.

## Фильтры

`OnFilters.dynamic_component` (`AdminTable/OnFilters.vue:128-152`) понимает:
`text/textarea/wysiwyg` → `filter-text`; `checkbox/switch` → `filter-checkbox`
(**не зарегистрирован**); `file/select/date/datetime/yearmon/memo/in_ext_url/
multiconnect` → `filter-*`. `filter_extend_*` на фронте **отсутствуют**
(0 вхождений в `src/`). Регистрация — `src/dynamic_component_loader.js`.

## 1_to_m: быстрые кнопки (`values`, `presets`)

Вложенные поля 1_to_m пробрасываются бэкендом как есть. В диалоге
`1_to_m/form.vue`:

- `fields[].values` — «варианты» одного поля (рендер в `fields/text.vue`,
  `set_new_value`); пример — A-записи (`w01`/`w02_n`).
- `fields[].presets` — кнопки, заполняющие **несколько** полей дочерней записи
  (`form.vue:apply_preset`, `<%поле%>` резолвится из `form.fields` родителя);
  пример — SPF в TXT-записях (`configs/svcmsadmin/domain`).
- `field.frontend.buttons` (`fields/frontend/buttons.vue`) — другой механизм:
  только `button.ajax` → `POST /ajax/<config>/<action>`, результат применяется к
  полям **главной** формы; для диалога 1_to_m не подходит.

## Const

`routes/const_routes.py`; фронт `src/components/Const.vue` понимает `header`,
`text`, `textarea`, `wysiwyg`, `file`, `checkbox`, `switch`, `select`.

## Скрины

`docs-developer/assets/screenshots/` (`admintable-const.png`,
`admintable-filters.png`, `admintree-admin-menu.png`, `editform-project.png`,
`editform-domain.png`, `login.png`).
