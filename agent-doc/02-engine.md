# Контракт `Engine`

`lib/engine.py`. Экземпляр создаётся на каждый запрос в `main.py:51`,
кладётся в `request.state.engine`.

```python
s = request.state.engine
```

**Не используйте `from lib.engine import s`** — это module-level глобал
(`lib/engine.py:131`), оставшийся от старой реализации. Не потокобезопасен,
ломается при `--workers > 1` и параллельных запросах. В роутах его больше нет;
единственный живой импорт — мёртвый `lib/CRM/plugins/search/xlsx.py`.

## Атрибуты после `await engine.reset(request=..., status_code=200)`

- `s.db` / `s.db_read` / `s.db_write` — все три один и тот же объект `get_db()`.
- `s.request`
- `s.headers` — список пар `[имя, значение]` для заголовков ответа.
- `s.env` — заголовки запроса, ключи в lowercase.
- `s.manager` — `{...}` (менеджер из debug-обхода; per-request настройки —
  в `request.state.manager`).
- `s.errors`, `s.project`, `s.config`, `s._end`, `s._content`, `s._content_type`.
- `request.state.cookies` — **словарь** `имя -> {value, path, samesite, secure, httponly}`.
- `request.state.cookies_for_delete` — **словарь** `имя -> {path, samesite, secure, httponly}`.

## Методы

| Вызов | Что делает |
|---|---|
| `s.set_cookie(name=..., value=...)` или `s.set_cookie(name, value)` | кладёт значение в `request.state.cookies`; middleware выставит его в ответ |
| `s.set_cookie(..., value=None)` | удаляет cookie (складывает атрибуты в `cookies_for_delete`) |
| `s.set_cookie(..., samesite='none', secure=True)` | переопределяет атрибут для вызова, иначе берётся из `config['cookie']` |
| `s.get_cookie(name)` | читает **входящие** cookies |
| `s.headers.append(['X-Foo', 'bar'])` | добавить заголовок ответа (именно список из 2 элементов) |
| `s._content = {...}` + `s.end()` | короткое замыкание: middleware вернёт этот JSON |
| `s.to_json(data)` | `json.dumps` с `indent=4`, `ensure_ascii=False` |

## Осторожно

- `request.state.cookies` хранит **не значение, а словарь с атрибутами**.
  Middleware в `main.py:67-88` сам раскладывает его в `response.set_cookie`.
- Атрибуты удаляемой cookie должны совпадать с теми, что ставились при
  `set_cookie`, иначе браузер не удалит cookie (удаление — отдельный
  `Set-Cookie` с `Max-Age=0`).
- Короткое замыкание всегда отдаёт **HTTP 200**, `Content-Type: text/plain`
  (`_content_type` игнорируется) — в `main.py:62` возвращается голый `Response`.

## Порядок middleware

`main.py:104` регистрирует `CORSMiddleware` после `for_all_requests`, чтобы он
был внешним слоем. Starlette кладёт каждый `add_middleware` в начало стека:
последний добавленный выполняется первым. Иначе при `engine._end` заголовки
`Access-Control-Allow-*` не попадают в ответ (детали — `08-auth-cors-cookies.md`).
