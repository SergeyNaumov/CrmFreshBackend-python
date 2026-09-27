# `wysiwyg` — визуальный редактор

Редактор TinyMCE с загрузкой изображений/файлов.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `filedir` | папка для файлов редактора (обязательно для загрузки файлов) |
| `edit_mode` | `1` — сразу открыть в режиме редактирования |
| `plugins` | список плагинов, напр. `[{'type':'GPTAssist','set_value_button':'...'}]` |
| `style` | список URL CSS для iframe редактора (напр. шрифт FontAwesome) |
| `read_only` | только чтение |

## Примеры

```python
{'description': 'Описание', 'type': 'wysiwyg', 'name': 'body',
 'filedir': './files/project_5830/news'}

# с GPTAssist (кнопка подставляет ответ в поле)
{'description': 'Описание', 'type': 'wysiwyg', 'name': 'body',
 'filedir': './files/project_5830/good',
 'plugins': [{'type': 'GPTAssist', 'set_value_button': 'Отправить в описание'}]}

# подключить FontAwesome внутри редактора
{'description': 'Text', 'type': 'wysiwyg', 'name': 'anons', 'tab': 'desc',
 'style': ['/templates/2026/arm-it/assets/fonts/font-awesome/font-awesome.min.css']}
```

## Особенности

- Значение сохраняется как HTML.
- Загрузка файлов из редактора — `/wysiwyg/<config>/<field>`
  (`routes/edit_form/wysiwyg_process.py`, `routes/wysiwyg_routes.py`).
- TinyMCE инициализируется лениво при входе в режим редактирования;
  редактор корректно переинициализируется при повторном открытии формы.
- `GPTAssist` — именно плагин, отдельного поля типа `GPTAssist` нет
  (см. [gptassist.md](gptassist.md)).

## Где в коде

- Фронт: `src/components/fields/wysiwyg.vue`
