# -*- coding: utf-8 -*-
"""Документация API управления контентом DS-сайта.

Из одного описания собираются:
  * doc_tree() -- разделы для вкладки «Документация» админки
                  (routes/documentation_routes.py, config == 'ds_api');
  * doc_html() -- самодостаточный HTML-файл (стили внутри, без внешних
                  зависимостей) для скачивания/печати
                  (GET /svcms/api/doc.html).

Реестр сущностей и целей загрузки повторяет движок
(sites/lib/api/entities.py). При изменении движка поправить и здесь.
"""

import html

DOC_TITLE = 'API управления контентом DS-сайта'
DOC_VERSION = 'v1'

# --- реестр сущностей (см. sites/lib/api/entities.py) -----------------------
# (сущность, таблица, название, бизнес-ключ, чпу-префикс, params, только чтение)
ENTITIES = [
  ('good', 'ds_good', 'Товары', 'artikul', '/good/', 'good', False),
  ('good_photos', 'ds_good_galery', 'Фотографии товара', '—', '—', '—', False),
  ('catalog', 'ds_catalog', 'Рубрики каталога', 'header', '/catalog/', 'catalog', False),
  ('params', 'ds_params', 'Характеристики (справочник)', 'header', '—', '—', False),
  ('params_catalog', 'ds_params_catalog', 'Характеристики рубрик', 'param_id+catalog_id', '—', '—', False),
  ('params_good', 'ds_params_good', 'Значения характеристик товаров', 'param_id+good_id', '—', '—', False),
  ('brands', 'ds_brands', 'Бренды', 'name', '—', '—', False),
  ('news', 'ds_news', 'Новости', 'header', '/news/', '—', False),
  ('article', 'ds_article', 'Статьи', 'header', '/article/', '—', False),
  ('service', 'ds_service', 'Услуги', 'header', '/service/', '—', False),
  ('text', 'ds_text', 'Текстовые страницы', 'url', '—', '—', False),
  ('slider', 'ds_slider', 'Слайдер', '—', '—', '—', False),
  ('advantages', 'ds_advantages', 'Преимущества', '—', '—', '—', False),
  ('employee', 'ds_employee', 'Сотрудники', '—', '—', '—', False),
  ('clients', 'ds_clients', 'Клиенты', '—', '—', '—', False),
  ('reviews', 'ds_reviews', 'Отзывы', '—', '—', '—', False),
  ('certificates', 'ds_certificates', 'Сертификаты', '—', '—', '—', False),
  ('galery', 'ds_galery', 'Фотогалерея', '—', '—', '—', False),
  ('video', 'ds_video', 'Видео', '—', '—', '—', False),
  ('doc', 'ds_doc', 'Документы', '—', '—', '—', False),
  ('filials', 'ds_filials', 'Филиалы', '—', '—', '—', False),
  ('top_menu', 'ds_top_menu', 'Верхнее меню', '—', '—', '—', False),
  ('bottom_menu', 'ds_bottom_menu', 'Нижнее меню', '—', '—', '—', False),
  ('const', 'const', 'Настройки сайта', 'name', '—', '—', True),
]

# --- цели загрузки (POST /api/v1/upload) ------------------------------------
# (цель, папка, типы, webp, миниатюры)
FILE_TARGETS = [
  ('good_galery', 'good_galery', 'image', 'да', '200x200, 320x320, 600x600'),
  ('catalog', 'catalog', 'image', 'да', '400x400, 800x800'),
  ('news', 'news', 'image', 'да', '400x225, 800x450'),
  ('articles', 'articles', 'image', 'да', '400x300, 800x600'),
  ('services', 'services', 'image', 'да', '400x300, 800x600, 1260x945'),
  ('slider', 'block-images/slider', 'image', 'да', '800x600, 1600x900'),
  ('employee', 'employee', 'image', 'да', '300x300, 600x600'),
  ('clients', 'clients', 'image', 'да', '—'),
  ('certificates', 'certificates', 'image', 'да', '360x260, 720x520'),
  ('galery', 'galery', 'image', 'да', '600x0, 1200x0'),
  ('brands', 'brands', 'image', 'да', '—'),
  ('advantages', 'advantages', 'image', 'нет', '—'),
  ('docs', 'docs', 'документ', 'нет', '—'),
  ('wysiwyg', 'wysiwyg', 'image', 'да', '—'),
]

DOC_EXT = 'pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, zip, rar, 7z, odt, ods'


def _e(text):
  return html.escape(str(text))


def _code(text):
  return f'<pre class="code">{_e(text.strip())}</pre>'


def _table(headers, rows):
  head = ''.join(f'<th>{_e(h)}</th>' for h in headers)
  body = ''
  for r in rows:
    body += '<tr>' + ''.join(f'<td>{c if str(c).startswith("<") else _e(c)}</td>' for c in r) + '</tr>'
  return f'<table class="tbl"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def _entities_table():
  rows = []
  for name, table, title, nk, chpu, params, ro in ENTITIES:
    rows.append([f'<code>{_e(name)}</code>', f'<code>{_e(table)}</code>', _e(title),
                 _e(nk), _e(chpu), _e(params), 'да' if ro else ''])
  return _table(['Сущность', 'Таблица', 'Название', 'Бизнес-ключ (replace)',
                 'ЧПУ-префикс', 'params', 'только чтение'], rows)


def _targets_table():
  rows = [[f'<code>{_e(t)}</code>', f'<code>{_e(d)}</code>', _e(k), _e(w), _e(rz)]
          for t, d, k, w, rz in FILE_TARGETS]
  return _table(['Цель (target)', 'Папка в files/project_&lt;id&gt;', 'Типы',
                 'webp', 'Миниатюры'], rows)


def sections(base_url='https://<домен>/api/v1'):
  """Разделы документации: [{'header', 'body', 'child':[...]}]."""
  base = html.escape(base_url)

  s = []

  s.append(dict(header='Обзор', body=f'''
    <p>API предназначен для обмена контентом DS-сайта с внешними системами:
    товары, рубрики каталога, характеристики, новости, статьи, услуги,
    текстовые страницы, слайдер, галереи, сотрудники, документы и др.</p>
    <p>API работает <b>на домене самого сайта</b>, поэтому данные изолированы по
    проекту: запрос к домену проекта A никогда не видит данных проекта B.
    Идентификатор проекта <code>project_id</code> в теле запроса не принимается —
    он определяется по домену (заголовок <code>Host</code>) и сверяется с
    проектом, обслуживаемым сервером.</p>
    <ul>
      <li>Базовый адрес: <code>{base}</code></li>
      <li>Формат: JSON (<code>application/json; charset=utf-8</code>); загрузка
        файлов — <code>multipart/form-data</code>.</li>
      <li>Все методы, кроме <code>ping</code>, вызываются методом <b>POST</b>.</li>
      <li>Кодировка ответа — UTF-8, ответы без BOM.</li>
    </ul>
  ''', child=[
    dict(header='Проверка доступности (ping)', body=f'''
      <p>Публичный метод без ключа: проверяет, что API поднят на домене.</p>
      {_code('GET ' + base_url + '/ping')}
      {_code('{"ok": true, "data": {"service": "ds-api", "version": "v1"}}')}
    '''),
    dict(header='Список сущностей (info)', body=f'''
      <p>Требует ключ. Возвращает версию API, список сущностей, целей загрузки
      и действующие лимиты.</p>
      {_code('POST ' + base_url + '/info')}
      {_code('{"ok": true, "data": {"version": "v1", "entities": [...], "targets": {...}, "limits": {...}}}')}
    '''),
  ]))

  s.append(dict(header='Авторизация', body='''
    <p>Ключ доступа задаётся в админке сайта («API и интеграции») и хранится в
    настройках проекта. Передавайте его одним из способов:</p>
    <ul>
      <li>заголовок <code>X-API-Key: &lt;ключ&gt;</code>;</li>
      <li>заголовок <code>Authorization: Bearer &lt;ключ&gt;</code>.</li>
    </ul>
    <p>Ключ сравнивается безопасно (сравнение с постоянным временем). Права
    задаются списком <b>scopes</b>: пусто = только чтение (<code>select</code>),
    иначе — перечисленные методы (<code>select, insert, update, replace, delete,
    upload</code>). Ограничение по IP — необязательное.</p>
  ''', child=[
    dict(header='Пример запроса с ключом', body=_code('''
curl -X POST https://<домен>/api/v1/select
  -H "X-API-Key: <ключ>"
  -H "Content-Type: application/json"
  -d '{"entity": "good", "limit": 10}'
    ''')),
  ]))

  s.append(dict(header='Ответы и ошибки', body=
    '<p>Успешный ответ:</p>' +
    _code('{"ok": true, "data": {"rows": [ ... ], "total": 12}}') +
    '<p>Ошибка:</p>' +
    _code('{"ok": false, "error": {"code": "validation", "message": "исправьте поля",\n'
          '  "fields": {"price": "ожидается число"}}}') +
    '<p>Коды ошибок:</p>' +
    _table(['Код', 'HTTP', 'Когда'], [
      ['unauthorized', '401', 'ключ не передан или неверен'],
      ['forbidden', '403', 'API выключено, нет scope, IP не разрешён, домен чужого проекта'],
      ['not_found', '404', 'неизвестная сущность или запись не найдена'],
      ['conflict', '409', 'конфликт (удаление рубрики с потомками без recursive, дубль ключа)'],
      ['validation', '422', 'ошибки в полях (в error.fields)'],
      ['bad_request', '400', 'некорректное тело запроса'],
      ['payload_too_large', '413', 'файл больше лимита'],
      ['unsupported_media_type', '415', 'недопустимый тип файла'],
      ['rate_limit', '429', 'превышен лимит запросов'],
      ['internal', '500', 'внутренняя ошибка сервера'],
    ])))

  s.append(dict(header='Метод select — чтение', body='''
    <p>Выборка строк. Возвращает <code>rows</code>, <code>total</code>,
    <code>limit</code>, <code>offset</code>.</p>
    <p>Параметры:</p>
    <ul>
      <li><code>entity</code> — имя сущности (обязательно);</li>
      <li><code>ids</code> — список id конкретных строк;</li>
      <li><code>where</code> — объект условий: <code>{"artikul": "A-1", "enabled": 1}</code>
        (<code>null</code> — IS NULL); значение-список → <code>IN</code>;</li>
      <li><code>fields</code> — список возвращаемых колонок;</li>
      <li><code>order</code> — колонка сортировки (по убыванию: <code>"id desc"</code>);</li>
      <li><code>limit</code> (по умолчанию 50, максимум 500), <code>offset</code>;</li>
      <li><code>with</code> — связанные данные: <code>{"params": true, "photos": true}</code>
        (характеристики и фотографии товара/рубрики).</li>
    </ul>
  ''', child=[
    dict(header='Пример: товары по рубрике с характеристиками', body=_code('''
POST /api/v1/select
X-API-Key: <ключ>

{
  "entity": "good",
  "where": {"rubricator_id": 611, "enabled": 1},
  "order": "id desc",
  "limit": 20,
  "with": {"params": true, "photos": true}
}
    ''')),
    dict(header='Ответ', body=_code('''
{
  "ok": true,
  "data": {
    "rows": [
      {"id": 2232, "header": "Товар", "artikul": "A-1", "price": 999,
       "url": "/good/tovar", "slug": "tovar",
       "params": [{"param_id": 3, "header": "Вес", "value": "1.5 кг"}],
       "photos": [{"id": 8518, "photo": "1792306178_9u.webp",
                   "url": "/files/project_5837/good_galery/1792306178_9u.webp"}]}
    ],
    "total": 1, "limit": 20, "offset": 0
  }
}
    ''')),
  ]))

  s.append(dict(header='Метод insert — добавление', body='''
    <p>Добавить одну строку (<code>data</code>) или пакет (<code>items</code>,
    не более 100 строк за запрос). Возвращает <code>ids</code> созданных строк.</p>
    <p>Поля, отличные от колонок таблицы, отклоняются (422). NOT NULL-колонки без
    значения и без DEFAULT заполняются безопасным значением (43706 для дат).</p>
  ''', child=[
    dict(header='Пример: товар с характеристиками и ЧПУ', body=_code('''
POST /api/v1/insert
{
  "entity": "good",
  "data": {
    "header": "Смартфон X",
    "artikul": "SP-X-1",
    "rubricator_id": 611,
    "price": 79990,
    "anons": "Краткое описание",
    "slug": "smartfon-x",
    "params": {"1": "БрендX", "3": "0.35 кг"}
  }
}
    ''')),
    dict(header='Ответ', body=_code('{"ok": true, "data": {"ids": [2233], "inserted": 1}}')),
  ]))

  s.append(dict(header='Метод update — изменение', body='''
    <p>Изменяет строки, выбранные одним из способов:
    <code>id</code> (одна строка), <code>ids</code> (список), <code>where</code>
    (объект условий). Максимум 500 строк за запрос.</p>
    <p>Меняются только переданные поля. Возвращает <code>updated</code> и
    <code>ids</code> затронутых строк.</p>
  ''', child=[
    dict(header='Пример', body=_code('''
POST /api/v1/update
{
  "entity": "good",
  "where": {"artikul": "A-1"},
  "data": {"price": 1290, "enabled": 1}
}
    ''')),
  ]))

  s.append(dict(header='Метод replace — замена/upsert', body='''
    <p>Найти строку по бизнес-ключу (<code>nk</code>, см. справочник) и обновить
    переданные поля, иначе добавить новую. Удобно для синхронизации каталога из
    внешней системы: повторный вызов не создаёт дубликатов.</p>
    <p>Для таблиц с зависимыми строками (<code>ds_good</code>, <code>ds_params</code>,
    <code>ds_catalog</code>) выполняется безопасный upsert (UPDATE + INSERT), а не
    REPLACE — дочерние записи не теряются.</p>
  ''', child=[
    dict(header='Пример по артикулу', body=_code('''
POST /api/v1/replace
{
  "entity": "good",
  "data": {"artikul": "A-1", "header": "Товар A-1", "price": 1290, "rubricator_id": 611}
}
    ''')),
  ]))

  s.append(dict(header='Метод delete — удаление', body='''
    <p>Удаляет строки по <code>id</code>, <code>ids</code> или <code>where</code>
    (не более 500 за запрос). Каскадно подчищаются связанные данные: значения
    характеристик, фотографии товара, ЧПУ.</p>
    <p>Удаление рубрики каталога/услуги с потомками или товарами требует
    <code>recursive: true</code>; иначе — 409. При рекурсивном удалении товары
    рубрики не удаляются, а отвязываются от неё.</p>
  ''', child=[
    dict(header='Пример', body=_code('''
POST /api/v1/delete
{"entity": "catalog", "id": 1304, "recursive": true}
    ''')),
  ]))

  s.append(dict(header='Метод upload — загрузка файлов', body=f'''
    <p>Загрузка файла методом <code>multipart/form-data</code>. Поля формы:</p>
    <ul>
      <li><code>file</code> — файл (обязательно);</li>
      <li><code>target</code> — цель загрузки: ключ из таблицы ниже или пара
        <code>сущность.поле</code> (например, <code>good.photos</code>,
        <code>catalog.photo</code>, <code>doc.attach</code>);</li>
      <li><code>ref_id</code> — id записи, к которой привязать файл
        (для галереи — добавляется строка, для колонки — записывается имя файла);</li>
      <li><code>orig_name</code> — необязательное исходное имя (по умолчанию из файла).</li>
    </ul>
    <p>Тип определяется по содержимому (изображения — Pillow; документы — по
    расширению из белого списка). Изображения конвертируются в webp и получают
    миниатюры. Имя файла на сервере — <code>&lt;время&gt;_&lt;2 символа&gt;</code>,
    оригинальное имя санитизируется.</p>
  ''', child=[
    dict(header='Пример: фотография товара', body=_code('''
curl -X POST https://<домен>/api/v1/upload \\
  -H "X-API-Key: <ключ>" \\
  -F "file=@photo.jpg" -F "target=good.photos" -F "ref_id=2232"
    ''')),
    dict(header='Ответ', body=_code('''
{
  "ok": true,
  "data": {
    "target": "good_galery", "filename": "1792306178_9u.webp",
    "orig_name": "photo.jpg", "width": 1200, "height": 800, "size": 15630,
    "url": "/files/project_5837/good_galery/1792306178_9u.webp",
    "resizes": [{"name": "mini1", "file": "1792306178_9u_mini1.webp",
                 "width": 200, "height": 200}],
    "attachment": "gallery"
  }
}
    ''')),
    dict(header='Цели загрузки', body=_targets_table() +
         f'<p>Документы (цель <code>docs</code>) принимаются с расширениями: {_e(DOC_EXT)}.</p>'),
  ]))

  s.append(dict(header='Характеристики товаров и рубрик', body='''
    <p>Характеристики хранятся в отдельных таблицах. В API есть «краткая» запись
    через <code>data.params</code>:</p>
    <ul>
      <li>для товара (<code>entity: good</code>) — объект
        <code>{"&lt;param_id&gt;": "значение"}</code>. Значение <code>null</code>
        удаляет характеристику у товара.</li>
      <li>для рубрики (<code>entity: catalog</code>) — список
        <code>[param_id, ...]</code>: какие характеристики показывать в рубрике.</li>
    </ul>
    <p>Связи синхронизируются в <code>ds_params_good</code> /
    <code>ds_params_catalog</code>. Справочник характеристик — сущность
    <code>params</code> (поля <code>header</code>, <code>type</code>).</p>
    <p>На чтение используйте <code>with: {"params": true}</code>.</p>
  ''', child=[
    dict(header='Пример: задать характеристики товару', body=_code('''
POST /api/v1/update
{"entity": "good", "id": 2232, "data": {"params": {"1": "Samsung", "3": "0.5 кг"}}}
    ''')),
  ]))

  s.append(dict(header='ЧПУ (человекопонятные ссылки)', body='''
    <p>Публичный адрес страницы формируется автоматически при добавлении и
    изменении заголовка:</p>
    <ul>
      <li>префиксы: <code>/good/</code>, <code>/catalog/</code>,
        <code>/news/</code>, <code>/article/</code>, <code>/service/</code>;</li>
      <li>слаг транслитерируется из <code>header</code>; при совпадении
        добавляется <code>-1</code>, <code>-2</code> и т. д.;</li>
      <li>можно задать свой слаг полем <code>slug</code> (без префикса) при
        добавлении; при обычном изменении заголовка слаг не меняется;</li>
      <li>при удалении записи её ЧПУ удаляется.</li>
    </ul>
    <p>При чтении строки ЧПУ отдаются как <code>url</code> (с префиксом) и
    <code>slug</code> (без префикса).</p>
  '''))

  s.append(dict(header='Справочник сущностей', body=
    '<p>Перечень сущностей API. Бизнес-ключ используется методом '
    '<code>replace</code>; <code>params</code> — поддержка краткой записи '
    'характеристик; «только чтение» — запись запрещена (403).</p>' + _entities_table()))

  s.append(dict(header='Лимиты и правила', body='''
    <ul>
      <li>пакет <code>insert</code>/<code>replace</code> — не более 100 строк за запрос;</li>
      <li><code>select</code> — не более 500 строк за запрос (по умолчанию 50);</li>
      <li><code>update</code>/<code>delete</code> — не более 500 строк за запрос;</li>
      <li>глубина дерева (рубрики, меню) — 5 уровней;</li>
      <li>файлы: до 15 МБ, изображения — до 40 мегапикселей;</li>
      <li>частота запросов и суточный лимит — настраиваются в админке;</li>
      <li>тело запроса — до 2 МБ (кроме загрузки файлов).</li>
    </ul>
  '''))

  s.append(dict(header='Безопасность и изоляция', body='''
    <p>Ключ доступа привязан к конкретному сайту (домену) и проверяется на
    стороне движка; данные изолированы по <code>project_id</code>, поэтому через
    API одного проекта невозможно прочитать или изменить данные другого.
    Служебные таблицы (заказы, заявки, менеджеры, домены) через API недоступны.</p>
    <p>В статистике и журнале ключ показывается только маской
    (<code>9f4c…71d2</code>); IP-адреса хранятся вместе с хэшем.</p>
    <p>При переносе данных проекта («Импорт / экспорт данных») настройки
    <code>api_*</code> (в т.ч. ключ) в архив по умолчанию не попадают.</p>
  '''))

  s.append(dict(header='Примеры интеграции', body='''
    <p>Ниже — минимальные примеры на разных языках. Ключ и домен подставьте свои.</p>
  ''', child=[
    dict(header='PHP (curl)', body=_code(r'''
<?php
$base = 'https://example.ru/api/v1';
$key  = 'ВАШ_КЛЮЧ';

function api($base, $key, $method, $payload) {
  $ch = curl_init("$base/$method");
  curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST => true,
    CURLOPT_HTTPHEADER => [
      'X-API-Key: ' . $key,
      'Content-Type: application/json; charset=utf-8',
    ],
    CURLOPT_POSTFIELDS => json_encode($payload, JSON_UNESCAPED_UNICODE),
  ]);
  $res = curl_exec($ch);
  if ($res === false) { throw new RuntimeException(curl_error($ch)); }
  curl_close($ch);
  $data = json_decode($res, true);
  if (empty($data['ok'])) {
    throw new RuntimeException($data['error']['message'] ?? 'API error');
  }
  return $data['data'];
}

// Пример: upsert товара по артикулу
$data = api($base, $key, 'replace', [
  'entity' => 'good',
  'data' => [
    'artikul' => 'A-1',
    'header'  => 'Товар A-1',
    'price'   => 1290,
    'rubricator_id' => 611,
  ],
]);
print_r($data);
''')),
    dict(header='Python', body=_code(r'''
import requests

BASE = 'https://example.ru/api/v1'
KEY = 'ВАШ_КЛЮЧ'

def api(method, payload):
    r = requests.post(f'{BASE}/{method}', json=payload, timeout=30,
                      headers={'X-API-Key': KEY})
    data = r.json()
    if not data.get('ok'):
        raise RuntimeError(data['error'])
    return data['data']

# upsert товара по артикулу
print(api('replace', {'entity': 'good', 'data': {
    'artikul': 'A-1', 'header': 'Товар A-1', 'price': 1290, 'rubricator_id': 611,
}}))

# загрузка фото товара
with open('photo.jpg', 'rb') as f:
    up = requests.post(f'{BASE}/upload', headers={'X-API-Key': KEY},
                       files={'file': f},
                       data={'target': 'good.photos', 'ref_id': 2232}, timeout=60)
print(up.json())

# выборка с характеристиками
print(api('select', {'entity': 'good', 'limit': 5,
                     'with': {'params': True, 'photos': True}}))
''')),
    dict(header='JavaScript (fetch)', body=_code(r'''
const BASE = 'https://example.ru/api/v1';
const KEY = 'ВАШ_КЛЮЧ';

async function api(method, payload) {
  const r = await fetch(`${BASE}/${method}`, {
    method: 'POST',
    headers: { 'X-API-Key': KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await r.json();
  if (!data.ok) throw new Error(data.error.message);
  return data.data;
}

api('select', { entity: 'catalog', limit: 100 })
  .then(d => console.log(d.rows));
''')),
    dict(header='1С (HTTP-запрос)', body=_code(r'''
// Общий модуль: вызов метода API DS-сайта
Функция ДС_API(Метод, Данные)
    Адрес = "https://example.ru/api/v1/" + Метод;
    Заголовки = Новый Соответствие;
    Заголовки.Вставить("X-API-Key", "ВАШ_КЛЮЧ");
    Заголовки.Вставить("Content-Type", "application/json; charset=utf-8");

    Тело = НаписатьJSONСтроку(Данные); // сериализация в UTF-8

    HTTP = Новый HTTPСоединение("example.ru", 443, , , , 30, Новый ЗащищенноеСоединениеOpenSSL());
    Запрос = Новый HTTPЗапрос("/api/v1/" + Метод, Заголовки);
    Запрос.УстановитьТелоИзСтроки(Тело, КодировкаТекста.UTF8);

    Ответ = HTTP.ВызватьHTTPМетод("POST", Запрос);
    Возврат Ответ.ПолучитьТелоКакСтроку("UTF-8");
КонецФункции
''')),
  ]))

  return s


def _flatten(sections_list, prefix='s'):
  """Пронумеровать разделы и вернуть плоский список + дерево."""
  tree, flat = [], []
  for i, sec in enumerate(sections_list, 1):
    sid = f'{prefix}{i}'
    item = {'id': sid, 'header': sec['header'], 'body': sec.get('body') or '', 'child': []}
    flat.append(item)
    for j, ch in enumerate(sec.get('child') or [], 1):
      cid = f'{sid}_{j}'
      citem = {'id': cid, 'header': ch['header'], 'body': ch.get('body') or '', 'child': []}
      item['child'].append(citem)
      flat.append(citem)
    tree.append(item)
  return tree, flat


def doc_tree(base_url=''):
  """Разделы для вкладки документации админки."""
  if not base_url:
    base_url = 'https://<домен>/api/v1'
  tree, _ = _flatten(sections(base_url))
  return {
    'title': DOC_TITLE,
    'links': [],
    'list': tree,
  }


_HTML_STYLE = '''
  :root { --fg:#1f2430; --muted:#5b6472; --line:#dfe3ea; --accent:#1e6fd9; --bg:#fff; --code:#f5f7fa; }
  * { box-sizing: border-box; }
  body { margin:0; padding:0; color:var(--fg); background:var(--bg);
         font: 15px/1.55 -apple-system, Segoe UI, Roboto, Arial, sans-serif; }
  .wrap { max-width: 1040px; margin: 0 auto; padding: 32px 20px 80px; }
  h1 { font-size: 28px; margin: 0 0 4px; }
  h2 { font-size: 22px; margin: 34px 0 10px; border-bottom: 1px solid var(--line); padding-bottom: 6px; }
  h3 { font-size: 17px; margin: 24px 0 8px; color: var(--accent); }
  p, li { color: var(--fg); }
  code { background: var(--code); padding: 1px 5px; border-radius: 4px;
         font-family: Consolas, "SF Mono", Menlo, monospace; font-size: 13px; }
  pre.code { background: #0f172a; color: #e6edf3; padding: 12px 14px; border-radius: 8px;
             overflow: auto; font-family: Consolas, "SF Mono", Menlo, monospace;
             font-size: 13px; line-height: 1.45; }
  table.tbl { border-collapse: collapse; width: 100%; margin: 10px 0 18px; font-size: 13.5px; }
  table.tbl th, table.tbl td { border: 1px solid var(--line); padding: 7px 9px; text-align: left; vertical-align: top; }
  table.tbl th { background: #f0f3f8; }
  .meta { color: var(--muted); font-size: 13px; margin-bottom: 18px; }
  .toc { background: #f8fafc; border: 1px solid var(--line); border-radius: 8px; padding: 14px 18px; margin: 18px 0 26px; }
  .toc a { display: block; text-decoration: none; color: var(--accent); padding: 2px 0; }
  .toc a.l1 { padding-left: 16px; font-size: 13.5px; color: var(--muted); }
  a { color: var(--accent); }
  hr { border: none; border-top: 1px solid var(--line); margin: 26px 0; }
  @media print { pre.code { background:#f5f7fa; color:#111; } .toc { page-break-after: always; } }
'''


def doc_html(base_url=''):
  """Самодостаточный HTML-файл документации (стили внутри)."""
  if not base_url:
    base_url = 'https://<домен>/api/v1'
  tree, _flat = _flatten(sections(base_url))
  toc = [f'<a href="#header{s["id"]}">{_e(s["header"])}</a>' for s in tree]
  body = []
  for sec in tree:
    body.append(f'<h2 id="header{sec["id"]}">{_e(sec["header"])}</h2>')
    body.append(sec['body'])
    for ch in sec['child']:
      body.append(f'<h3 id="header{ch["id"]}">{_e(ch["header"])}</h3>')
      body.append(ch['body'])
  return f'''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{_e(DOC_TITLE)}</title>
<style>{_HTML_STYLE}</style>
</head>
<body>
<div class="wrap">
  <h1>{_e(DOC_TITLE)}</h1>
  <div class="meta">Версия {_e(DOC_VERSION)} · базовый адрес <code>{_e(base_url)}</code></div>
  <div class="toc">{''.join(toc)}</div>
  <hr>
  {''.join(body)}
</div>
</body>
</html>
'''
