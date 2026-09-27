# Запуск и конфигурация

## Запуск

**Обязательно из корня репозитория**: `lib/engine.py:9` захватывает
`os.getcwd()` на импорте (используется для debug-обхода авторизации).

Основной деплой: `start/svcms_manager.sh`

```bash
export config=config_svcms_manager && uvicorn --reload --port=5000 --workers 1 main:app
```

Бинарники — `.venv/bin/uvicorn`, `.venv/bin/python` (Python 3.12).
В системе несколько конфигов, но сейчас рабочий — только svcms_manager.

## env `config`

`config.py` целиком:

```python
conf_file = os.getenv('config')      # ИМЯ МОДУЛЯ, не имя файла
config = importlib.import_module(conf_file).config
```

- Значение env `config` — **dotted-путь до модуля**, не имя файла. Модуль обязан
  экспортировать словарь `config = {...}`.
- Без env `config` модуль печатает инструкцию и делает `quit()` на импорте.
- Модули: `config_test`, `config_beyeezy`, `config_crimea`, `config_teleweb`,
  `config_trade`, `config_svcms_manager`, `config_svcms_admin`.
- Все настройки деплоя живут в `config_*.py`, общих значений по умолчанию нет.
- Конфиг импортируется очень рано (`main.py` → `routes` → `lib.engine` →
  `config`), поэтому модули конфига **не должны** импортировать `routes` или
  `lib.engine` на уровне модуля — циклический импорт. `lib.*` и другие
  `configs.*` импортировать можно.

## Ключи `config`

| Ключ | Смысл |
|---|---|
| `BaseUrl`, `system_url`, `BaсkendBase` | URL'ы. В `BaсkendBase` кириллическая **с** |
| `config_folder` | папка конфигов инструментов, напр. `configs/test` |
| `cors_origins` | список Origin'ов для CORS (`08-auth-cors-cookies.md`) |
| `cookie` | атрибуты session-cookie: `path`, `samesite`, `secure`, `httponly` |
| `auth` | таблица менеджеров, поля логина/пароля, `encrypt_method`, таблицы сессий, лимиты, `use_roles`/`use_permissions` |
| `login.not_login_access` | whitelist путей без авторизации |
| `connects.crm_read` / `connects.crm_write` | параметры MySQL |
| `debug` | обход авторизации, см. ниже |
| `after_create_engine(s)` | хук после создания Engine (резолв проекта по Host) |
| `after_read_form_config(form)` | хук после чтения конфига инструмента |
| `after_all_change_action(form)` | хук после каждой insert/update/delete |
| `const`, `events`, `controllers`, `telegram`, `mail`, `wysiwyg`, `messenger_rules`, `gptassist_rules`, `docpack`, `stat_log` | прочее |

## Debug-обход авторизации

`lib/engine.py:52-91`: если `hostname` есть в `config['debug']['hosts']`
(и, если задан `pwd`, текущий каталог в `config['debug']['pwd']`), авторизация
не проверяется и подставляется фиксированный менеджер (`manager_id` или `login`).
Если ключа `hosts` нет — условие считается выполненным, т.е. **все запросы
авторизуются как manager_id 0**.

В `config_test.py:168` перечислены хосты разработчиков, включая `sv-home`.
В `config_svcms_manager.py:180` debug: `hosts: ['sv-home']`, `manager_id: 5520`.

Следствие: на машине разработчика запросы проходят без cookies, поэтому по
локальным логам нельзя судить о работоспособности авторизации.

## Startup

`main.py:38-44` — `@app.on_event("startup")` вызывает `db.create_pool()`.
Shutdown-хука нет, `db.close_pool()` нигде не вызывается (`10-known-issues.md`).
