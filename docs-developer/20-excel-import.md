# Импорт/экспорт Excel (инструменты-парсеры)

Серверный инструмент может читать `.xls`/`.xlsx` (импорт) и отдавать выгрузку
(экспорт). Роут — `POST /parser-excel/<config>`, файлы на скачивание —
`GET /download_tmp/<filename>`.

В отличие от обычного инструмента, конфиг парсера — это **async-функция
`get_parser(arg)`**, возвращающая словарь, а не `form = {...}`:

```python
# conf_projects/project_5830/good_import/__init__.py
FIELDS=[
  {'description':'Артикул (artikul)','name':'artikul','type':'text'},
  {'description':'Заголовок (header)','name':'header','type':'text'},
  {'description':'Цена (price)','name':'price','type':'text'},
  {'description':'Название рубрики (rubricator_name)','name':'rubricator_name','type':'text','required':0},
]

async def get_parser(arg):
  project_id=arg['project_id']          # из request.state
  return {
    'title':'Импорт товаров',
    'work_table':'ds_good', 'work_table_id':'id', 'foreign_key':'project_id',
    'tmp_dir':'./files/tmp/good_import',
    'parser_engine':'xlsx',
    'unique_fields':['project_id','artikul'],   # по чем искать существующую запись
    'const_values':{'project_id':project_id},   # серверные значения, перекрывают файл
    'fields':FIELDS,
    'before_loopback':before_loopback,          # async
    'after_item':after_item,                    # async
    'after_load':after_load,                    # async
  }
```

`arg` = `{config, project_id, admin_id}`.

## Действия

| Действие | Что делает |
|---|---|
| `init` | отдаёт конфиг (поля, справочники, правила) |
| `preload` | принимает файл (base64), кладёт во временную папку, возвращает первые строки для сопоставления колонок |
| `load` | разбирает файл и делает insert/update в `work_table` |
| `check_refs` | **только чтение**: каких значений справочников нет в проекте |
| `create_refs` | создаёт отсутствующие значения справочников по названию |

## Соответствие колонок

Заголовок колонки в файле должен **совпадать** с `description` поля
(`autofill_preload` на фронте подбирает соответствие автоматически; руками
можно переопределить). Поэтому экспорт и импорт используют одинаковые
заголовки.

`required:0` — колонка необязательна. `require_any_of:[['A','B']]` — из группы
должна быть выбрана хотя бы одна колонка (пример: `id` **или** название рубрики).

Пустая ячейка при `update` **не трогает** поле (в `before_loopback` пустые
значения вырезаются).

## Справочники: id или название, только своего проекта

Если значения в файле — это ссылки (рубрика, бренд) и в разных проектах id
разные, объявите их в `refs`. Тогда фронт перед загрузкой покажет отсутствующие
значения и предложит создать их (в текущем проекте).

```python
refs=[
  {
    'key':'rubric', 'label':'рубрики', 'one':'рубрика',
    'table':'ds_catalog', 'name_col':'header',
    'id_field':'rubricator_id', 'name_field':'rubricator_name',
    'scope':{'project_id':project_id},                 # только свой проект
    'create':{'path':'','anons':'','photo':'','sort':0,'enabled':1,'reset_filters':0},
    'chpu':{'in_url':'/catalog/<%id%>','prefix':'/catalog/'},   # ещё и ЧПУ
  },
  {
    'key':'brand', 'label':'бренды', 'one':'бренд',
    'table':'ds_brands', 'name_col':'name',
    'id_field':'brand', 'name_field':'brand_name',
    'scope':{'project_id':project_id}, 'allow_zero':1,           # 0 = «без бренда»
    'create':{'logo':'','country':'','url':'','sort':0,'enabled':1},
  },
]
```

Правило разбора: число в колонке id проверяется на принадлежность проекту; если
не подошло — берётся название; чужой/несуществующий id и ненайденное название
в БД **не пишутся**, а показываются замечанием. Если в колонке одна (только id
или только название) — достаточно `id_field`, `name_field` можно не задавать.

## Хуки (все — async)

- `before_loopback(data, db)` — нормализовать значения строки (`data`) до
  записи: обрезка пробелов, числа, чекбоксы, резолв справочников.
- `after_item(data, record_id, db, errors)` — после записи строки: связанные
  данные (характеристики, сбор фото и т.п.).
- `after_load(db, ctx)` — после всего файла: итоговое сообщение, постановка
  фоновых задач. `ctx` содержит `stats` (`insert`/`update`).

## Экспорт

Кнопка-выгрузка — через `form.search_plugin` и события `before_search` /
`after_search` (`before_search` ставит `form.not_perpage=1`, чтобы выгрузить
всё). В `after_search` формируется `xlsx` (openpyxl) в `files/tmp` и отдаётся
ответ `{'format':'file','url':'/download_tmp/<файл>'}`; фронт скачивает по
ссылке. Заголовки колонок — те же `description`, что у импорта.

## Пример целиком

Товары `ds_good`: экспорт — `conf/ds_good/plugins.py`; импорт —
`conf/ds_good_import/__init__.py` (upsert по `project_id+artikul`,
характеристики → `ds_params*`, фото — фоновой задачей). Механику подробно см.
`agent-doc/07-core-routes.md` и `agent-doc/12-configs.md`.
