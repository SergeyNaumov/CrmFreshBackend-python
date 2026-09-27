# `file` — загрузка файла

Загрузка файла(ов) в `filedir`. Бэкенд: `lib/CRM/form/upload_file.py`,
`lib/CRM/form/delete_file.py`. Фронт: `src/components/fields/file.vue`.

## Атрибуты

| Атрибут | Смысл |
|---|---|
| `description`, `name` | базовые |
| `filedir` | папка для файлов, обязательно (`./files/<project>/<tool>`) |
| `resize` | список вариантов ресайза |
| `crops` | включить кроппер (пропорции берутся из `resize`) |
| `cropper` | включить кроппер |
| `preview` | `'WxH'` — какой из `resize` считать превью (для `1_to_m`/списков) |
| `max_size` | максимальный размер файла (байт) |
| `accept` | `accept` для input (MIME/расширения) |
| `keep_orig_filename` | хранить оригинальное имя (`attach_name;filename`) |
| `required` | файл обязателен |
| `read_only` | только чтение (ссылка «скачать») |

## `resize`

```python
'resize': [
    {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '156x117', 'quality': '100'},
    {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '355x215', 'quality': '100'},
]
```

Плейсхолдеры: `<%filename_without_ext%>`, `<%ext%>`. Опции ресайза:
`quality`, `grayscale`, `composite_file`, `composite_gravity`, `composite_resize`.
Исходный файл тоже сохраняется.

## Пример

```python
{'description': 'Фото товара', 'type': 'file', 'name': 'photo',
 'filedir': './files/project_5830/good',
 'preview': '156x117',
 'resize': [
     {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '156x117', 'quality': '100'},
     {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '355x215', 'quality': '100'},
 ]}

{'description': 'Фото', 'type': 'file', 'name': 'photo',
 'filedir': './files/project_5830/news'}
```

## Особенности

- Значение в БД — имя файла (или `attach_name;filename` при
  `keep_orig_filename`).
- Путь на фронте: `BaseUrl + filedir.replace('./','/') + '/' + filename`.
- В `1_to_m` бэк формирует `<name>_filename` и `preview_img`
  (`lib/get_1_to_m_data.py`).
- Наличие/отсутствие файла фильтруется значениями `1`/`2` в фильтре `file`.
- `filedir` часто подставляют в `events.permissions` (например, по `project_id`).

## Вычисляемый `filedir`

```python
async def permissions(form):
    pid = form.request.state.project['project_id']
    for f in form.fields:
        if f.get('filedir'):
            f['filedir'] = f['filedir'].replace('[project_id]', str(pid))
```
