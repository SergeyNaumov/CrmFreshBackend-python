# 14. Готовые рецепты

Полные (или почти полные) примеры под типовые задачи. Все — из реальных
конфигов, ссылки на файлы указаны.

## 1. Плоский список с редактированием в дереве (`news`)

`conf_projects/project_5830/news/__init__.py`

```python
async def before_code_top(form, field):
    if form.action == 'new':
        field['value'] = 1

form = {
    'work_table': 'struct_5830_news',
    'work_table_id': 'id',
    'title': 'Новости',
    'sort': 0,
    'tree_use': False,
    'header_field': 'header',
    'default_find_filter': 'header',
    'changed_in_tree': True,
    'fields': [
        {'description': 'Название новости', 'type': 'text', 'name': 'header'},
        {'description': 'Дата (для сортировки)', 'type': 'date', 'name': 'registered'},
        {'description': 'Анонс', 'type': 'textarea', 'name': 'anons',
         'regexp_rules': ['/^.{3,255}$/', 'длина анонса должна быть не менее 3 символов']},
        {'description': 'Описание', 'type': 'wysiwyg', 'name': 'body'},
        {'description': 'Название-2', 'type': 'text', 'name': 'header2',
         'add_description': 'выводится под анонсом новости белым шрифтом'},
        {'description': 'Фото', 'type': 'file', 'name': 'photo',
         'filedir': './files/project_5830/news'},
        {'description': 'Ссылка на новость', 'type': 'text', 'name': 'url_old',
         'add_description': 'если не стандартная'},
        {'description': 'TOP', 'type': 'checkbox', 'name': 'top'},
        {'description': 'Вкл', 'type': 'checkbox', 'name': 'enabled',
         'before_code': before_code_top},
    ],
}
```

`news/events.py` подставляет `work_table` по проекту, добавляет ЧПУ-поле
плагином `InExtUrl` и регистрирует ajax-контроллеры. `news/ajax.py` содержит
`in_ext_url` (генерация ЧПУ) и `url` (проверка занятости). См. [09](09-ajax.md).

## 2. Галерея (`advantages`)

`conf_projects/project_5830/advantages/__init__.py`

```python
form = {
    'work_table': 'struct_5830_advantages',
    'title': 'Наши преимущества',
    'view_type': 'gallery',
    'photo_for_gallery': 'photo',
    'sort': 1,          # разрешает перетаскивание
    'tree_use': False,
    'header_field': 'header',
    'changed_in_tree': False,
    'cols': 3,          # 3 колонки
    'fields': [
        {'description': 'Преимущество', 'type': 'textarea', 'name': 'header'},
        {'description': 'Иконка', 'type': 'file', 'name': 'photo',
         'filedir': './files/project_5830/advantages'},
    ],
}
```

## 3. Дерево + дочерние записи (`catalog`)

`conf_projects/project_5830/catalog/__init__.py` (сокращённо)

```python
form = {
    'work_table': 'struct_5830_catalog',
    'title': 'Каталог товаров',
    'sort': True,
    'tree_use': True,
    'max_level': 3,
    'header_field': 'header',
    'wide_form': True,
    'cols': [
        [{'description': 'SEO', 'name': 'promo', 'hide': True},
         {'description': 'Основное', 'name': 'main'}],
        [{'description': 'Вендоры', 'name': 'vendors'},
         {'description': 'Описание', 'name': 'desc'}],
    ],
    'fields': [
        {'description': 'Заголовок', 'type': 'text', 'name': 'header', 'tab': 'main'},
        {'description': 'Наименование в меню', 'type': 'text', 'name': 'header_menu', 'tab': 'main'},
        {
            'description': 'Вендоры', 'type': '1_to_m', 'name': 'vendors',
            'table': 'struct_5830_catalog_vendor', 'table_id': 'id',
            'foreign_key': 'catalog_id', 'sort': 1, 'tab': 'vendors',
            'fields': [
                {'description': 'Вендор', 'type': 'select_from_table',
                 'name': 'vendor_id', 'table': 'struct_5830_vendor',
                 'header_field': 'header', 'value_field': 'id'},
                {'description': 'Лого', 'type': 'file', 'name': 'logo',
                 'filedir': './files/project_5830/catalog/vendor'},
            ],
        },
    ],
}
```

## 4. Карточка с вкладками, зависимостями и ресайзом фото (`good`)

`conf_projects/project_5830/good/__init__.py` (сокращённо)

```python
form = {
    'work_table': 'struct_5830_good',
    'title': 'Список товаров',
    'wide_form': True,
    'cols': [
        [{'description': 'SEO', 'name': 'promo', 'hide': True},
         {'description': 'Основное', 'name': 'main'}],
        [{'description': 'Фотогалерея', 'name': 'gal'},
         {'description': 'Описание', 'name': 'desc'}],
    ],
    'fields': [
        {'description': 'Наименование', 'type': 'text', 'name': 'header',
         'tab': 'main', 'filter_on': 1},
        {'description': 'Акция', 'type': 'checkbox', 'name': 'action', 'tab': 'main',
         'frontend': {'fields_dependence': '''
            v => { window.EditForm.get_field_by_name('price').hide = !v.action }
         '''}},
        {'description': 'Цена', 'type': 'text', 'name': 'price', 'hide': True,
         'regexp_rules': ['/^[0-9]*$/', 'Укажите целое число'], 'tab': 'main'},
        {'description': 'Фотогалерея', 'type': '1_to_m', 'name': 'gal',
         'table': 'struct_5830_good_galery', 'table_id': 'id',
         'foreign_key': 'good_id', 'sort': 1, 'tab': 'gal',
         'fields': [
             {'description': 'Название', 'type': 'text', 'name': 'header'},
             {'description': 'Фото', 'type': 'file', 'name': 'photo',
              'filedir': './files/project_5830/good/galery'},
         ]},
        {'description': 'Фото товара', 'type': 'file', 'name': 'photo',
         'filedir': './files/project_5830/good',
         'preview': '156x117',
         'resize': [
             {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '156x117', 'quality': '100'},
             {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '355x215', 'quality': '100'},
         ],
         'tab': 'main'},
        {'description': 'Описание', 'type': 'wysiwyg', 'name': 'body', 'tab': 'desc',
         'plugins': [{'type': 'GPTAssist', 'set_value_button': 'Отправить в описание'}]},
    ],
}
```

## 5. Зависимости полей: полный тест (`test2`)

`configs/svcmsmanager/test2/__init__.py` — эталон локальных и ajax-зависимостей
(есть и цикл `x → y → x`, и ajax-цикл `title → slug → title`).

```python
dep1_js = '''
v=>{
  let d2={},d3={},d4={};
  let n=parseInt(v.dep1||0);
  if(n==1){ d2.hide=true; d3.hide=true; d4.hide=true; }
  if(n==2){ d2.hide=false; d3.hide=true; d4.hide=true; }
  if(n==3){ d2.hide=false; d3.hide=false; d4.hide=false; }
  if(n==4){ d3.hide=false; d4.hide=false;
    d3.value='r'+Math.random().toString(36).slice(2,8);
    d4.value='r'+Math.random().toString(36).slice(2,8);
  }
  return ['dep2',d2,'dep3',d3,'dep4',d4];
}
'''

async def gen_slug(form, values):
    return ['slug', {'value': translit(values.get('title') or '')}]

form = {
    'work_table': 'test2',
    'title': 'Зависимости (тест)',
    'ajax': {'gen_slug': gen_slug, 'echo_title': echo_title},
    'cols': [
        [{'description': 'Локальные', 'name': 'a'}, {'description': 'Цикл', 'name': 'b'}],
        [{'description': 'Ajax', 'name': 'c'}],
    ],
    'fields': [
        {'description': 'dep1', 'name': 'dep1', 'type': 'select_values',
         'values': [{'v': 1, 'd': 'скрыть'}, {'v': 2, 'd': 'показать dep2'}],
         'frontend': {'fields_dependence': dep1_js}, 'tab': 'a'},
        {'description': 'dep2', 'name': 'dep2', 'type': 'select_values',
         'values': [{'v': 1, 'd': 'один'}, {'v': 2, 'd': 'два'}], 'tab': 'a'},
        {'description': 'dep3', 'name': 'dep3', 'type': 'text', 'tab': 'a'},
        {'description': 'title', 'name': 'title', 'type': 'text',
         'frontend': {'ajax': {'name': 'gen_slug', 'timeout': 200}}, 'tab': 'c'},
        {'description': 'slug', 'name': 'slug', 'type': 'text',
         'frontend': {'ajax': {'name': 'echo_title', 'timeout': 200}}, 'tab': 'c'},
    ],
}
```

## 6. Константы (`template_const`)

`conf_projects/project_5830/template_const/__init__.py`

```python
form = {
    'work_table': 'const',
    'work_table_id': 'const_id',
    'work_table_foreign_key': 'template_id',
    'work_table_foreign_key_value': 'id',
    'title': 'Константы для сайта',
    'filedir': './files',
    'filedir_http': '/files',
    'name_field': 'name',
    'value_field': 'value',
    'default_find_filter': 'header',
    'fields': [
        # ...
    ],
}
```

## 7. multiconnect (M2M)

`configs/beyeezy/good/__init__.py` (сокращённо)

```python
{
  'description': 'Доп. категории',
  'type': 'multiconnect',
  'name': 'good_category',
  'relation_table': 'category',
  'relation_save_table': 'good_category',
  'relation_table_header': 'header',
  'relation_save_table_header': 'header',
  'relation_table_id': 'id',
  'relation_save_table_id_worktable': 'good_id',
  'relation_save_table_id_relation': 'category_id',
  'tree_use': 1,
  'tree_table': 'category',
  'tablename': 'gc',
}
```

## 8. 1_to_1 (поле в отдельной таблице)

`configs/beyeezy/category/__init__.py`

```python
{'description': 'Таблица размеров', 'type': '1_to_1_wysiwyg',
 'save_table': 'category_sizes', 'foreign_key': 'id',
 'name': 'size_table', 'db_name': 'body'}

{'description': 'Опция', 'type': '1_to_1_checkbox',
 'foreign_key': 'id', 'name': 'opt_germes', 'db_name': 'opt_germes',
 'save_table': 'category_options'}
```
