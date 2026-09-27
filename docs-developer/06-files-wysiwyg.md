# 06. Файлы и wysiwyg

## Тип `file`

Загрузка файла в `filedir`. На бэке — `lib/CRM/form/upload_file.py`,
удаление — `lib/CRM/form/delete_file.py`.

| Атрибут | Смысл |
|---|---|
| `filedir` | папка для файлов, обязательно. Формат `./files/<project>/<tool>` |
| `resize` | список вариантов ресайза |
| `crops` | массив кропов (приходит с фронта при `cropper`) |
| `cropper` | включить кроппер на фронте |
| `preview` | `'WxH'` — какой из `resize` считать превью (для `1_to_m`, списков) |
| `size` | размер по умолчанию (если нет `resize`) |
| `quality` | качество JPEG |
| `not_delete` | запретить удаление (см. `fields/file.vue`) |

### `resize`

Каждый элемент — ресайз исходника в отдельный файл. Плейсхолдеры в имени:
`<%filename_without_ext%>`, `<%ext%>`.

```python
'resize': [
    {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '156x117', 'quality': '100'},
    {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '355x215', 'quality': '100'},
]
```

`size` — `"WxH"`. Ресайз делает `lib.resize.resize_one` с опциями `grayscale`,
`composite_file`, `composite_gravity`, `composite_resize`, `quality`.

### `preview` и `1_to_m`

В `1_to_m` (`lib/get_1_to_m_data.py`) для файла формируется:
- `<name>_filename` — имя файла;
- `preview_img` — путь к превью: если задан `preview`, берётся соответствующий
  вариант из `resize`, иначе — исходный файл.

Поэтому для миниатюр в слайдах удобно держать в `resize` вариант с тем же
`size`, что и `preview`.

### Путь к файлу на фронте

Фронт строит `src` как `BaseUrl + filedir.replace(/\.\//,'/') + '/' + filename`
(см. `fields/file.vue`). Для галереи путь формирует бэк (`admin_tree_run.py`).

### Значение в БД

В колонке хранится имя файла (иногда `attach_name;filename`). Наличие файла
фильтруется значениями `1`/`2` в фильтре `file` (`get_search_where.py`).

### Константы (`const`)

Для `script='const'` поле `file` сохраняется иначе (`routes/const_routes.py`):
используются `filedir` и `filedir_http`, имя файла = `<name>.<ext>`, старый
файл удаляется.

## Тип `wysiwyg`

Визуальный редактор TinyMCE + загрузка файлов/изображений.

| Атрибут | Смысл |
|---|---|
| `filedir` | папка для файлов редактора |
| `edit_mode` | `1` — сразу режим редактирования |
| `plugins` | список плагинов, например GPTAssist |

```python
{'description': 'Описание', 'type': 'wysiwyg', 'name': 'body',
 'filedir': './files/project_5830/news'}
```

Загрузка файла из редактора — `/wysiwyg/<config>/<field>` (см.
`routes/edit_form/wysiwyg_process.py`, `routes/wysiwyg_routes.py`).

### GPTAssist как плагин

```python
{'description': 'Описание', 'type': 'wysiwyg', 'name': 'body',
 'filedir': './files/project_5830/good',
 'plugins': [{'type': 'GPTAssist', 'set_value_button': 'Отправить в описание'}]}
```

`set_value_button` — текст кнопки, которая подставляет ответ GPT в поле.
Компонент: `src/components/GPTAssist/GPTAssist`.

## Хитрости

- Для картинок в карточке достаточно `resize` без `preview`; `preview` нужен
  только для миниатюр в `1_to_m`/списках.
- `filedir` можно вычислять в `events.py` (например, подставить `project_id`) —
  так делают `good`, где папка зависит от проекта. В `__init__.py` пишут
  заглушку `./files/project_[project_id]/good`, а в `events.permissions`
  заменяют `[project_id]` фактическим значением.
- В `wysiwyg` можно подключить `style`: массив URL CSS для iframe редактора
  (например, шрифт FontAwesome).
