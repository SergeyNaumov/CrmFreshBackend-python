# Константы сайта конструктора (сервис «Настройки»).
# Поля и порядок (табы) заданы здесь статически — единый источник для всех
# DS-проектов. Значения хранятся в таблице `const` (name/value/project_id).

# (tab, name, description, type)
CONST_FIELDS = [
    ('main',   'orgname',       'Название компании',              'text'),
    ('main',   'slogan',        'Слоган',                         'text'),
    ('main',   'logo',          'Логотип',                        'file'),
    ('main',   'favicon',       'Favicon (иконка сайта, .svg/.png/.ico)', 'file'),
    ('main',   'phone',         'Телефон',                        'text'),
    ('main',   'phone_raw',     'Телефон (для ссылки tel:)',      'text'),
    ('main',   'email',         'E-mail',                         'text'),
    ('main',   'phones',        'Доп. телефоны (через запятую)',  'text'),
    ('main',   'work_time',     'Режим работы',                   'text'),

    ('addr',   'address',       'Адрес',                          'textarea'),
    ('addr',   'map_lat',       'Широта',                         'text'),
    ('addr',   'map_lon',       'Долгота',                        'text'),

    ('social', 'vk',            'ВКонтакте',                      'text'),
    ('social', 'ok',            'Одноклассники',                  'text'),
    ('social', 'rutube',        'Rutube',                         'text'),
    ('social', 'dzen',          'Дзен',                           'text'),
    ('social', 'max',           'MAX',                            'text'),

    ('seo',    'ym_id',         'ID Яндекс.Метрики',              'text'),
    ('seo',    'counter',       'Счётчики сайта',                 'textarea'),
    ('seo',    'copyright',     'Копирайт',                       'text'),

    # Яндекс.Маркет: значения уходят в автогенерируемый /catalog.yml
    # (sites/lib/seo_files.py::catalog_yml), в коде ничего не хардкодим.
    ('shop',   'delivery_cost', 'Стоимость доставки, ₽ (catalog.yml; пусто — доставку не выгружать)', 'text'),
    ('shop',   'delivery_days', 'Срок доставки (например 1-3)',   'text'),
    ('shop',   'pickup',        'Самовывоз: 1 — да, 0 — нет',     'text'),

    ('req',    'legal_name',    'Полное наименование',            'text'),
    ('req',    'short_name',    'Сокращённое наименование',       'text'),
    ('req',    'inn',           'ИНН',                            'text'),
    ('req',    'ogrn',          'ОГРН / ОГРНИП',                  'text'),
    ('req',    'legal_address', 'Юридический адрес',              'textarea'),
    ('req',    'fact_address',  'Фактический адрес',              'textarea'),
    ('req',    'post_address',  'Почтовый адрес',                 'textarea'),
    ('req',    'director',      'Руководитель',                   'text'),
    ('req',    'bank',          'Банк',                           'text'),
    ('req',    'rs',            'Расчётный счёт',                 'text'),
    ('req',    'corr_account',  'Корр. счёт',                     'text'),
    ('req',    'bik',           'БИК',                            'text'),
]

# Порядок табов.
CONST_TABS = [
    ('main',   'Основное'),
    ('addr',   'Адрес и карта'),
    ('social', 'Соцсети'),
    ('seo',    'Счётчики и SEO'),
    ('shop',   'Магазин (Яндекс.Маркет)'),
    ('req',    'Реквизиты'),
]


async def permissions(form):
    project = form.request.state.project
    project_id = project['project_id']

    form.fields = [
        {'name': name, 'description': desc, 'type': ftype, 'tab': tab}
        for tab, name, desc, ftype in CONST_FIELDS
    ]
    form.tabs = [{'name': name, 'description': desc} for name, desc in CONST_TABS]

    form.filedir = f"./files/project_{project_id}"
    form.filedir_http = f"/files/project_{project_id}"
    form.foreign_key = 'project_id'
    form.foreign_key_value = project_id


events = {'permissions': permissions}
