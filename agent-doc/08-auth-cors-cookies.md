# Авторизация, CORS, cookies

## Авторизация и сессии

`lib/session.py`. При обычном запросе `Engine.reset` (`lib/engine.py:52-91`)
проверяет путь по `config['login']['not_login_access']`; если путь не в
whitelist — либо debug-обход, либо `session_start(s, request)`.

- `session_create(s, ...)` — логин по `config['auth']`. `encrypt_method`:
  `mysql_sha2`, `mysql_encrypt` или plain. Проверяет лимиты неудачных попыток
  по логину/IP (`max_fails_*`), создаёт запись в `session_table`, ставит
  cookies `auth_user_id` и `auth_key`.
- **MySQL 8 и пароли.** В MySQL 8 удалена функция `ENCRYPT()`, поэтому SQL-ветка
  `mysql_encrypt` (`password=encrypt(%s,password)`) падает. После неудачной/пустой
  SQL-проверки `session_create` делает резервную проверку на стороне Python
  (`lib/password.py: verify_password`): поддерживает plaintext, sha2-256 (64),
  md5 (32) и crypt — DES/ENCRYPT (13 символов, исторические `admin`/`manager`)
  и `$1$/$5$/$6$`. Хэширование при записи — `lib/password.py: hash_password`
  (`mysql_encrypt` → DES-совместимый crypt, `mysql_sha2` → sha2-256); используется
  в `save_form.py`, `routes/password.py` и создании проекта
  (`routes/svcmsadmin/project_create.py`).
- `session_start(s, request)` — читает `auth_user_id`/`auth_key`, сверяет с
  `auth['session_table']`, кладёт менеджера в `request.state.manager`, иначе
  `s.end()` с `redirect` на `/login`.
- `session_logout(s)` — удаляет запись сессии.
- `get_permissions_for` / `project_get_permissions_for` — права, группы,
  `files_dir` по умолчанию (`./files`, `/files`).

Whitelist без авторизации — `config['login']['not_login_access']`
(в svcms_manager: `/login`, `/register`, `/remember/*`, `/gpt-assist/daemon-result`).

## Cookies

Атрибуты session-cookie берутся из `config['cookie']` и пробрасываются
`Engine.set_cookie` → `main.py:67-88` в `response.set_cookie`.
В `config_test.py` и `config_svcms_manager.py`: `samesite='none'`, `secure=True`,
`httponly=True`.

Почему `SameSite=None` + `Secure`:

- Chrome не отправляет `SameSite=Lax` cookie в кросс-сайтном XHR, поэтому при
  dev-раскладке «фронт `127.0.0.1:8081`, бэк `localhost:5000`» авторизация
  молча теряется.
- Chrome **требует** `Secure` вместе с `SameSite=None`, иначе cookie
  отбрасывается целиком.
- `Secure`-cookie Chrome принимает на `http://localhost` и `http://127.0.0.1`
  (trustworthy origins), но **не** на `http://<LAN-IP>`. Для http-деплоя вернуть
  `samesite='lax'`, `secure=False`.
- `httponly=True` закрывает `auth_key` от чтения из JS.

Удаление cookie — отдельный `Set-Cookie` с `Max-Age=0`; атрибуты удаляемой
cookie должны совпадать с теми, что ставились, иначе браузер её не удалит.

**Парная правка во фронте:** у axios-инстанса в `CrmFreshFront-v3/src/main.js:50`
нет `withCredentials: true`. Без него кросс-доменный cookie не отправить/не
принять. Пока фронт ходит на `/backend/...` relative через nginx — не нужно.

## CORS (`main.py`)

Три части:

1. `dev_origin_regex = r"^https?://(localhost|127\.0\.0\.1|\[::1\])(:\d+)?$"`
   (`main.py:18`) — петля на любом порту (vite при занятом 8081 сам уходит на 8082).
2. `allow_origins=config.get('cors_origins', [])` — прод-домены из `config_*.py`.
   Если ключа нет — запросы same-origin через nginx (`location /backend/`).
3. `allow_private_network=True` — Chrome Private Network Access. Без него preflight
   с `Access-Control-Request-Private-Network: true` получает
   `400 Disallowed CORS private-network`.

`expose_headers` (`main.py:29`): `Content-Disposition`, `Content-Length`,
`Content-Range`, `Accept-Ranges`, `Last-Modified`, `ETag`.

### Грабли CORS

- **`"*:*"` ≠ `"*"`.** Starlette проверяет `"*" in allow_origins`; `"*:*"` не
  включает `allow_all_origins` и не совпадёт ни с одним `Origin`.
- **`localhost` и `127.0.0.1` — разные Origin'ы.**
- **Порядок middleware.** `add_middleware` кладёт в начало стека. `CORSMiddleware`
  регистрируется **после** `for_all_requests` (`main.py:104`), чтобы быть внешним.
  Иначе при `engine._end` заголовки `Access-Control-Allow-*` не попадают в ответ.
- **Дубликат ACAO.** `settings/nginx_section.txt:29,39,46` добавляет
  `Access-Control-Allow-Origin: *` через `add_header`; вместе с CORS из приложения
  браузер получит заголовок дважды и отклонит ответ.
- Запрещённый Origin → **`400 Disallowed CORS origin`**, не 401.

## Известные дефекты авторизации

- `lib/session.py:2` — `from db import db`, но `db/__init__.py` экспортирует
  мемоизированный `db = None`; в `session_create` обращение `db.query`
  (`session.py:50`, не awaited) сломано. Используйте `s.db`.
- `lib/session.py:137` — `session_table=auth['manager_table']` (похоже на опечатку),
  `session_start` использует `auth["session_table"]` напрямую.
- Debug-обход (см. `01-run-config.md`) маскирует кросс-сайтовую авторизацию:
  на `sv-home` все запросы авторизуются как `manager_id 5520`.
