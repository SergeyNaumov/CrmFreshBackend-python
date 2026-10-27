# Реестр таблиц DS-проекта для инструмента «Импорт / экспорт данных»
# (svcms manager). Общая логика — ds_data_export.py / ds_data_import.py.
#
# Контракт архива — см. ds_data_export.py (manifest.json + data/*.json + files/).
#
# В реестре хранится только то, что нельзя получить из БД:
#   order         -- порядок вставки (родители раньше детей: FK ON DELETE CASCADE
#                    не даст вставить ребёнка в несуществующего родителя);
#   natural_key   -- «натуральный» ключ строки для режима «совместить»
#                    (пустые значения ключа => строка вставляется, а не ищется);
#   parent_col    -- самоссылка (дерево): вставка в два прохода;
#   refs          -- ссылки на другие таблицы: колонка -> таблица (id переносится
#                    между проектами заново, поэтому id всегда ремапится);
#   upsert        -- вставка через ON DUPLICATE KEY (const: уникальный
#                    ключ (name, project_id));
#   service       -- служебные данные (заявки/заказы): по умолчанию не выгружаются;
#   where_tpl     -- выборка строк для таблиц без project_id (%s = project_id).
#
# project_id в выгрузке НЕ сохраняется: целевой проект известен по хосту
# (after_create_engine), это позволяет переносить архив между проектами.

import os

FILES_ROOT = 'files'
TMP_DIR = 'files/tmp'
IMPORT_PREFIX = 'ds_import_'   # files/tmp/ds_import_<id>.zip -- загруженный архив
EXPORT_PREFIX = 'ds_data_export_'  # files/tmp/ds_data_export_<pid>_<дата>.zip -- готовый архив

FORMAT = 'ds-project-data'
FORMAT_VERSION = 1

# Служебные настройки API DS-сайта (ключ, scope, лимиты) -- префикс имени
# в const. По умолчанию в архив не попадают: ключ доступа не должен уезжать
# при переносе контента между проектами (в интерфейсе -- флаг «включить ключ»).
API_CONST_PREFIX = 'api_'
API_CONST_EXCLUDE = "`name` NOT LIKE 'api\\_%'"

# Имена колонок файла -> папка внутри files/project_<id> (только file-поля
# конфигов; нужна при подсчёте/сверке файлов). Пустой список колонок в
# текстовых значениях не проверяется: пути /files/project_<N>/ переписываются
# везде по регулярному выражению.
FILE_COLS = {
  'ds_advantages': {'icon': 'advantages'},
  'ds_article': {'photo': 'articles'},
  'ds_brands': {'logo': 'brands'},
  'ds_catalog': {'photo': 'catalog'},
  'ds_certificates': {'photo': 'certificates'},
  'ds_clients': {'photo': 'clients'},
  'ds_doc': {'attach': 'docs'},
  'ds_employee': {'photo': 'employee'},
  'ds_galery': {'photo': 'galery'},
  'ds_good_galery': {'photo': 'good_galery'},
  'ds_news': {'photo': 'news'},
  'ds_service': {'photo': 'services'},
  'ds_slider': {'photo': 'block-images/slider'},
  # у const filedir -- корень files/project_<id>, значения в value часто без папки
}

TABLES = {
  'ds_params': dict(order=10, title='Характеристики товаров (справочник)', natural_key=None),
  'ds_catalog': dict(order=20, title='Каталог (рубрики)', natural_key=['header'], parent_col='parent_id',
                     refs={'parent_id': 'ds_catalog'}),
  'ds_service': dict(order=30, title='Услуги', natural_key=None, parent_col='parent_id',
                     refs={'parent_id': 'ds_service'}),
  'ds_top_menu': dict(order=40, title='Верхнее меню', natural_key=None, parent_col='parent_id',
                      refs={'parent_id': 'ds_top_menu'}),
  'ds_bottom_menu': dict(order=50, title='Нижнее меню', natural_key=None, parent_col='parent_id',
                         refs={'parent_id': 'ds_bottom_menu'}),
  'ds_brands': dict(order=60, title='Бренды', natural_key=['name']),
  'ds_clients': dict(order=70, title='Клиенты', natural_key=None),
  'ds_employee': dict(order=80, title='Сотрудники', natural_key=None),
  'ds_filials': dict(order=90, title='Филиалы', natural_key=None),
  'ds_advantages': dict(order=100, title='Преимущества', natural_key=None),
  'ds_certificates': dict(order=110, title='Сертификаты', natural_key=None),
  'ds_galery': dict(order=120, title='Фотогалерея сайта', natural_key=None),
  'ds_slider': dict(order=130, title='Слайдер', natural_key=None),
  'ds_video': dict(order=140, title='Видео', natural_key=None),
  'ds_article': dict(order=150, title='Статьи', natural_key=None),
  'ds_news': dict(order=160, title='Новости', natural_key=None),
  'ds_reviews': dict(order=170, title='Отзывы', natural_key=None),
  'ds_text': dict(order=180, title='Текстовые страницы', natural_key=['url']),
  # Произвольные файлы домена (сервис «Файлы для поисковиков»): robots.txt,
  # sitemap.xml, AGENTS.md и прочее. Содержимое живёт в БД, поэтому переносится
  # вместе с проектом; ключ — url внутри проекта.
  'files': dict(order=185, title='Файлы для поисковиков', natural_key=['url']),
  'ds_doc': dict(order=190, title='Документы', natural_key=None),
  # const -- «Настройки сайта», уникальный ключ (name, project_id)
  # const -- «Настройки сайта», уникальный ключ (name, project_id)
  'const': dict(order=200, title='Настройки сайта', natural_key=['name'], upsert=True,
                exclude_tpl=API_CONST_EXCLUDE),
  'ds_good': dict(order=210, title='Товары', natural_key=['artikul'],
                  refs={'rubricator_id': 'ds_catalog', 'brand': 'ds_brands'}),
  'ds_good_galery': dict(order=220, title='Фотогалерея товаров', natural_key=None, refs={'good_id': 'ds_good'}),
  'ds_params_catalog': dict(order=230, title='Характеристики по рубрикам', natural_key=None,
                            refs={'param_id': 'ds_params', 'catalog_id': 'ds_catalog'}),
  'ds_params_good': dict(order=240, title='Значения характеристик товаров', natural_key=['param_id', 'good_id'],
                         refs={'param_id': 'ds_params', 'good_id': 'ds_good'}),
  # Служебные таблицы (персональные данные, заказы): по умолчанию не выгружаются
  'ds_zakaz': dict(order=250, title='Заказы', natural_key=None, service=True),
  'ds_zakaz_good': dict(order=260, title='Товары в заказах', natural_key=None, service=True, project_col='',
                        where_tpl='zakaz_id IN (SELECT id FROM ds_zakaz WHERE project_id=%s)',
                        refs={'zakaz_id': 'ds_zakaz', 'good_id': 'ds_good'}),
  'ds_form_submit': dict(order=270, title='Заявки с форм', natural_key=None, service=True),
}


def get_table(name):
  return TABLES.get(name)


def table_pk(name):
  # const использует собственный первичный ключ
  return 'const_id' if name == 'const' else 'id'


def table_title(name):
  # Человеческое название для интерфейса; если не задано -- имя таблицы
  return (TABLES.get(name) or {}).get('title') or name


def is_service(name):
  return bool((TABLES.get(name) or {}).get('service'))


def default_tables():
  # Контентные таблицы (без заказов/заявок)
  return [n for n, t in sorted(TABLES.items(), key=lambda x: x[1]['order'])
          if not t.get('service')]


def sorted_tables(names):
  # names=None -> все таблицы; пустой список -> пустой список
  return [n for n, _ in sorted(
    ((n, t) for n, t in TABLES.items() if names is None or n in names),
    key=lambda x: x[1]['order'])]


def project_dir(project_id):
  return os.path.join(FILES_ROOT, f'project_{project_id}')
