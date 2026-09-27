# Формат ответа и ошибки

Почти все хендлеры возвращают один и тот же конверт:

```json
{"success": 1, "errors": [], "log": [], ...}
```

- `form.success()` возвращает `(True, False)[len(form.errors) > 0]`.
- **Ошибки не передаются HTTP-кодом.** Ответ почти всегда `200`, а неуспех
  обозначается `success: 0` и непустым `errors`.
- Исключения наружу не пробрасываются:
  `form.errors.append('текст')`, `lib/CRM/form/run_event.py` ловит ошибки и
  пишет в `errors`, `db/functions.py:out_error` пишет в `arg['errors']` и
  печатает в консоль.
- `lib/all_configs.py:read_config` при неудачном импорте конфига возвращает
  **объект `error`, а не `Form`** (см. `03-forms.md`). Код всё равно читает
  `form.errors` — это работает, но тип другой. Проверяйте.

## Типичный хендлер

```python
router = APIRouter()

@router.post('/get-result')
async def get_result(R: dict, request: Request):
  form = await read_config(request=request, R=R, config=R['config'], script='find_objects')
  ...
  return {'success': form.success(), 'results': form.SEARCH_RESULT, 'errors': form.errors}
```

## Правила

- `read_config` вызывается **только с `await`** и только с `request=`.
- Тело запроса — `R: dict` (имя с заглавной), нужен `request: Request` в
  сигнатуре; обращение к «глобальному» `request` даст `NameError`.
- Ответ собирается из `form.success()`, `form.errors`, `form.log` и полезной
  нагрузки (`form.SEARCH_RESULT`, `results`, `titles` и т.п.).
