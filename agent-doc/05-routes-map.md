# Карта роутов

Базовый `router` подключается в `main.py:122` без префикса, реальные URL —
как в таблице. Подключения — `routes/__init__.py`.

## Подключённые модули

| Модуль | Префикс | Основные эндпоинты | Назначение |
|---|---|---|---|
| `routes/mainpage/` | `/mainpage` | `GET ''`, `/birthdays`, `/notifications`, `/notifications/update/{max_id}`, `/notifications/set-readed/{_id}/{v}`, `/manager-load/init`, `/manager-load/save/{percent}` | Главная: менеджер, новости, уведомления, дни рождения |
| `routes/register.py` | — | `POST /register`, `/remember/get-access-code`, `/remember/check-access-code`, `/remember/change-password` | Регистрация и восстановление пароля по email-коду |
| `routes/password.py` | — | `POST /password/{config}/{field_name}/{id}` | Смена пароля менеджера + уведомление |
| `routes/core_routes.py` | — | `POST /core/get-manager` | Права/данные менеджера по логину |
| `routes/transfere_cards/` | `/transfere-cards` | `GET/POST /{config}` (action `transfere`) | Перенос карточек/записей |
| `routes/testing.py` | — | `GET /test-headers`, `/test-cookie-write`, `/test/quote`, `/test-cookie-read`, `/config`, `/test-query`, `/test/mailsend` | Отладочные эндпоинты (cookie, заголовки, SQL, почта). Подключён в прод |
| `routes/get_filters_routes.py` | — | `GET/POST /get-filters/{config}` | Фильтры списка для фронта |
| `routes/get_result_routes.py` | — | `POST /get-result` | Поиск/список записей: SQL, пагинация |
| `routes/admin_tree_routes.py` | — | `GET/POST /admin-tree/{config}` | Дерево разделов: ветки, сортировка, move |
| `routes/edit_form_routes.py` | — | `POST /edit-form/{config}`, `PUT/POST /edit-form/{config}/{id}`, `GET /delete-element/{config}/{id}`, `POST /multiconnect/{config}/{field_name}` | Карточка: создание/правка/удаление, multiconnect; сюда вложен wysiwyg |
| `routes/wysiwyg_routes.py` (вложен) | `/wysiwyg` | `POST /{config}/{field_name}/{_id}/upload`, `POST /{config}/{field_name}`, `GET /{config}/{field}/init_options`, `GET /load-template/{config}/{field}/{template_id}` | Файлы и операции WYSIWYG, опции, шаблоны |
| `routes/one_to_m_routes.py` | — | `GET /1_to_m/{config}/{field_name}/{id}`, `POST /1_to_m/insert|update|update_field|sort/...`, `GET /1_to_m/delete/...`, `POST /1_to_m/upload_file/...`, `GET /1_to_m/delete_file/...` | Дочерние записи «один-ко-многим», сортировка, файлы |
| `routes/memo.py` | `/memo` | `GET /get/{config}/{field_name}/{id}`, `POST /add/...`, `/update/...`, `GET /delete/...` | Заметки/комментарии к карточке |
| `routes/const_routes.py` | `/const` | `POST /get`, `/save_value` | Экран констант/настроек |
| `routes/multiaction_routes.py` | `/multiaction` | `POST /{config}` (subaction: `set_all_value_field`, `delete`, `change_price`) | Массовые операции над выбранными |
| `routes/docpack_routes/` | `/docpack` | `GET /load-dogovor/{docpack_id}/{ext}/{need_print}`, `/load-bill/...`, `/load-act/...`, `/load-app/...`, `POST /{config}/{field_name}` (list, create_docpack, create_bill, create_act, create_app, get_bills, link_sr, save_summ_bill и др.) | Пакет документов: договоры, счета, акты |
| `routes/parser_excel/` | `/parser-excel` | `POST /{config}` (action: `init`, `preload`, `load`) | Загрузка/предпросмотр Excel |
| `routes/messenger.py` | `/messenger` | `WS /ws/{socket_name}`, `GET ''`, `/chatlist`, `/chat/{user_id}`, `/chat-forward/{user_id}/{last_id}`, `POST /send`, `GET /connects`, `/get-socket-name`, `POST /local-send` | Мессенджер: WebSocket + REST |
| `routes/extend_routes.py` | — | `POST /extend/KLADR` | Поиск адресов через внешний API KLADR |
| `routes/documentation_routes.py` | `/documentation` | `GET /{config}` | Экран документации (дерево) |
| `routes/page_routes.py` | `/page` | `GET /{config}/{id}` | Произвольная страница из блоков |
| `routes/table_routes.py` | `/table` | `GET /{config}` | Простой табличный вывод |
| `routes/video_routes.py` | `/VideoList` | `POST /{config}`, `GET /{config}` | Список видео + статистика просмотров |
| `routes/news_routes.py` | `/NewsList` | `POST /{config}`, `GET /{config}` | Список новостей + статистика |
| `routes/autocomplete.py` | `/autocomplete` | `POST /{config}` | Автодополнение select-полей по `term` |
| `routes/stat_tool.py` | `/stat-tool` | `POST /{config}` (init), `POST /{config}/search` | Инструмент статистики |
| `routes/ajax.py` | — | `GET/POST /ajax/{config}/{ajax_name}` | Универсальный диспетчер AJAX-контроллеров |
| `routes/gptassist/` | `/gpt-assist` | `GET /init`, `POST /send-task`, `/daemon-result`, `WS /ws/{task_id}` | GPT-ассистент |
| `routes/svcms/` | `/svcms` | `GET /left-menu` | Левое меню SV-CMS (проект 5830) |
| `routes/svcmsadmin/` | `/svcmsadmin` | `GET /left-menu-admin` | Левое меню админки `config_svcms_admin` из `admin_menu_new` |

## Не подключены

| Модуль | Статус | Эндпоинты | Назначение |
|---|---|---|---|
| `routes/beeline/` | не включён нигде | `GET/POST /subscription` | Вебхук-заглушка Beeline (телефония) |
| `routes/core_routes/login.py` | мёртвый, никем не импортируется | `GET /login`, `POST /test`, `GET /left-menu`, `/left-menu/tree` | Устаревший модуль авторизации/меню |

## Пакеты-помощники без своих роутов

- `routes/edit_form/` — `process_edit_form`, `multiconnect`, `one_to_m`,
  `wysiwyg_process`, `one_to_m_routine/*`.
- `routes/get_result/` — `gen_query_search`, `process_result_list`.
- `routes/docpack_routes/*` — обработчики действий докпака.
- `routes/parser_excel/*` — `load_parser_from_config`, `load`, `go_parse`.
- `routes/admin_tree/` — `admin_tree_run`, `move`.
- `routes/gptassist/` — `models` (pydantic), `sockets_connector`.

## Замечания

- `routes/wysiwyg_routes.py` не импортируется в `__init__.py` напрямую: он
  вложен в `edit_form_routes` (`edit_form_routes.py:106`).
- `routes/ajax.py` вешает на одну функцию оба декоратора — `@router.post` и
  `@router.get`.
