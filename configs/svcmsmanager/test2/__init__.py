# Тестовый конфиг зависимостей полей.
# Таблица: test2 (см. комментарий ниже).
"""
CREATE TABLE `test2` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sort` int unsigned NOT NULL DEFAULT 0,
  `dep1` varchar(50) NOT NULL DEFAULT '',
  `dep2` varchar(50) NOT NULL DEFAULT '',
  `dep3` varchar(255) NOT NULL DEFAULT '',
  `dep4` varchar(255) NOT NULL DEFAULT '',
  `x` varchar(255) NOT NULL DEFAULT '',
  `y` varchar(255) NOT NULL DEFAULT '',
  `title` varchar(255) NOT NULL DEFAULT '',
  `slug` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""

import re


def _translit(s):
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
         'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm',
         'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
         'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
         'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '_'}
    for k, v in d.items():
        s = s.replace(k, v)
        s = s.replace(k.upper(), v.upper())
    s = re.sub(r'[^a-zA-Z0-9\-_]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.lower().strip('-_')


# --- локальная зависимость: dep1 управляет dep2/dep3/dep4 ---
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

# --- цикл: x -> y -> x (движок должен сойтись) ---
x_js = "v=>(['y',{value: v.x||''}])"
y_js = "v=>(['x',{value: v.y||''}])"


# --- ajax-зависимости (цикл title -> slug -> title, должен сойтись + TTL-кэш) ---
async def gen_slug(form, values):
    return ['slug', {'value': _translit(values.get('title') or '')}]


async def echo_title(form, values):
    return ['title', {'value': values.get('slug') or ''}]


form = {
    'work_table': 'test2',
    'work_table_id': 'id',
    'title': 'Зависимости (тест)',
    'sort': True,
    'tree_use': True,
    'header_field': 'dep1',
    'default_find_filter': '',
    'ajax': {'gen_slug': gen_slug, 'echo_title': echo_title},
    'cols': [
        [
            {'description': 'Локальные', 'name': 'a'},
            {'description': 'Цикл x/y', 'name': 'b'},
        ],
        [
            {'description': 'Ajax', 'name': 'c'},
        ],
    ],
    'tabs': [
        {'name': 'a', 'description': 'Локальные'},
        {'name': 'b', 'description': 'Цикл x/y'},
        {'name': 'c', 'description': 'Ajax'},
    ],
    'fields': [
        {
            'description': 'dep1 (управляет другими)',
            'name': 'dep1',
            'type': 'select_values',
            'values': [
                {'v': 1, 'd': 'скрыть dep2, dep3, dep4'},
                {'v': 2, 'd': 'показать dep2'},
                {'v': 3, 'd': 'показать dep2, dep3, dep4'},
                {'v': 4, 'd': 'заполнить dep3/dep4 случайно'},
            ],
            'frontend': {'fields_dependence': dep1_js},
            'tab': 'a',
        },
        {
            'description': 'dep2',
            'name': 'dep2',
            'type': 'select_values',
            'values': [{'v': 1, 'd': 'один'}, {'v': 2, 'd': 'два'}],
            'tab': 'a',
        },
        {
            'description': 'dep3',
            'name': 'dep3',
            'type': 'text',
            'tab': 'a',
        },
        {
            'description': 'dep4',
            'name': 'dep4',
            'type': 'text',
            'tab': 'a',
        },
        {
            'description': 'x (цикл)',
            'name': 'x',
            'type': 'text',
            'frontend': {'fields_dependence': x_js},
            'tab': 'b',
        },
        {
            'description': 'y (цикл)',
            'name': 'y',
            'type': 'text',
            'frontend': {'fields_dependence': y_js},
            'tab': 'b',
        },
        {
            'description': 'title',
            'name': 'title',
            'type': 'text',
            'frontend': {'ajax': {'name': 'gen_slug', 'timeout': 200}},
            'tab': 'c',
        },
        {
            'description': 'slug',
            'name': 'slug',
            'type': 'text',
            'frontend': {'ajax': {'name': 'echo_title', 'timeout': 200}},
            'tab': 'c',
        },
    ],
}
