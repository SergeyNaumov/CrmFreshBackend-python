# `password` — пароль

Специальный тип: значение не отдаётся на фронт, поддерживает генерацию и
отправку. На фронте — `src/components/fields/password.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `min_length` | минимальная длина (по умолчанию `6`) |
| `generate_len_pas` | длина генерируемого пароля |
| `symbols` | алфавит для генерации |
| `methods_send` | варианты действия: `[{'description': '...', 'method_send': func}]` |
| `enctypt_method` | способ шифрования (удаляется перед отдачей на фронт) |

## Пример

```python
async def without_send(form):
    # «сохранить и никуда не отправлять»
    return

{'description': 'Пароль', 'type': 'password', 'name': 'password',
 'min_length': 8,
 'symbols': '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
 'methods_send': [
     {'description': 'сохранить и никуда не отправлять', 'method_send': without_send},
     # {'description': 'сохранить и отправить письмом', 'method_send': send_new_password},
 ],
 'tab': 'main'}
```

## Особенности

- В `get_values` значение **вырезается** из данных, отдаваемых на фронт.
- Пароль сохраняется только при `action == 'insert'`; шифрование — по
  `config['auth']['encrypt_method']` (`save_form.py`).
- `methods_send` описывает, что делать после ввода (отправить/не отправлять).
