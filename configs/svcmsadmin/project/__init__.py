from lib.CRM.form.idn import domain_to_unicode


# Ссылка на настройки группового шаблона (legacy поле links).
def links_code(form, field):
  if not form.id:
    return
  
  #form.pre(form.old_values)

  field['after_html'] = (
    f'<a href="/edit_form/project_group_site/{form.id}" target="_blank">'
    'Настройки привязки к групповому шаблону</a>'
  )


SSL_NAMES = {1: 'платный SSL', 2: "let's encrypt"}
SMALL = 'font-size: 12px; color: gray;'


# slide_code для домена в 1_to_m (ссылка на сайт, статус, ссылки на админки).
async def domain_slide_code(form, field, data):
  domain = data.get('domain') or ''
  if not domain:
    return ''
  label = f'{domain_to_unicode(domain)}'
  is_ssl = int(data.get('is_ssl') or 0)
  protocol = 'https' if is_ssl else 'http'
  manager = '/manager2' if str(data.get('server_type')) == '3' else '/manager'
  paid_till = str(data.get('paid_till') or '')
  if paid_till.startswith('0000'):
    paid_till = ''
  else:
    paid_till = f'оплачен до {paid_till}'
  status = [protocol]
  if is_ssl:
    status.append(SSL_NAMES.get(is_ssl, 'SSL'))
  if paid_till:
    status.append(paid_till)
  return (
    f'<a href="{protocol}://{domain}" target="_blank">{label}</a>'
    f'<div style="{SMALL}">{" &middot; ".join(status)}</div>'
    f'<div style="{SMALL}">'
    f'<a href="/edit_form/domain/{data.get("domain_id")}" target="_blank">админка домена</a>'
    f' &middot; <a href="{protocol}://{domain}{manager}" target="_blank">админка сайта</a>'
    '</div>'
  )


# slide_code для шаблона в 1_to_m (ссылка на шаблон + папка с файлами).
async def template_slide_code(form, field, data):
  tid = data.get('template_id')
  if not tid:
    return '-'
  tpl = await form.db.query(
    query='SELECT header, folder FROM template WHERE template_id=%s',
    values=[tid],
    onerow=1,
    errors=form.errors,
  )
  header = (tpl or {}).get('header') or str(tid)
  folder = (tpl or {}).get('folder') or ''
  nav = (
    f'/admin2/template_editor/navigator.pl?fname={folder}'
    if str(data.get('server_type')) == '3'
    else f'/filenavigator/filenavigator?dir={folder}'
  )
  return (
    f'<a href="/edit_form/template/{tid}" target="_blank">{header}</a>'
    f'<div style="{SMALL}">'
    f'<a href="{nav}" target="_blank">файлы:</a> {folder}'
    '</div>'
  )


form={
  'work_table':'project',
  'work_table_id':'project_id',
  'title':'Проект',
  'make_delete':1,
  'read_only':0,
  'wide_form':1,
  'header_field':'header',
  'default_find_filter':'header',
  
  'QUERY_SEARCH_TABLES':[
    {'t':'project','a':'wt'},
    {'t':'domain','a':'d','l':'d.project_id=wt.project_id','lj':1},
    {'t':'template','a':'t','l':'d.template_id=t.template_id','lj':1},
    {'t':'project_hosting','a':'ph','l':'ph.domain_id=d.domain_id','lj':1},
    {'t':'admin_project_v','a':'apv','l':'apv.project_id=wt.project_id','lj':1},
  ],
  'cols':[
    [
      {'description':'Ссылки','name':'links'},
      {'description':'Общая информация','name':'info'},
      {'description':'Работа с сущностями','name':'struct'},
      {'description':'Доп. инструменты','name':'project_menu'},
    ],
    [
      {'description':'Инструменты','name':'tools'},
      {'description':'Работа с редиректами','name':'add_info'},
      {'description':'Опции','name':'opt'},
    ],
  ],
  'fields':[
    {
      'description':'Ссылки',
      'type':'code',
      'name':'links',
      'full_str':True,
      'code':links_code,
      'tab':'links',
    },
    {
      'description':'Название проекта',
      'type':'text',
      'name':'header',
      'autocomplete':True,
      'filter_on':True,
      'regexp_rules':['^.+$','Заполните название проекта'],
      'tab':'info',
    },
    {
      'description':'project_id',
      'type':'text',
      'name':'project_id',
      'read_only':True,
      'filter_on':True,
      'tab':'info',
    },
    {
      'description':'Upstream для /files',
      'add_description':'будет работать только для сайтов с сертификатами',
      'name':'upstream',
      'type':'select_values',
      'value':1,
      'values':[
        {'v':1,'d':'С текущего сервера'},
        {'v':2,'d':'С stg_w03'},
      ],
      'tab':'info',
    },
    {
      'description':'Дата создания проекта',
      'type':'date',
      'name':'registered',
      'tab':'info',
    },
    {
      'description':'Комментарий',
      'type':'textarea',
      'name':'comment',
      'tab':'info',
    },
    {
      'description':'crm_id',
      'type':'filter_extend_text',
      'name':'user_id',
      'tablename':'d',
      'db_name':'user_id',
      'tab':'info',
    },
    {
      'description':'Хостинг выключен',
      'type':'filter_extend_checkbox',
      'name':'disabled',
      'tablename':'ph',
      'db_name':'disabled',
      'tab':'info',
    },
    {
      'description':'Размер папки files, Мб',
      'type':'code',
      'name':'size_project',
      'tab':'info',
    },
    {
      'description':'Размер папки templates, Мб',
      'type':'code',
      'name':'size_template',
      'tab':'info',
    },
    {
      'description':'Стоимость хостинга в год',
      'type':'code',
      'name':'paid_on_year',
      'tab':'info',
    },
    {
      'description':'Программист',
      'type':'filter_extend_select_values',
      'name':'author',
      'tablename':'apv',
      'db_name':'login',
      'values':[
        {'v':'isavnin','d':'Исавнин'},
        {'v':'antonov','d':'Антонов'},
        {'v':'naumov','d':'Наумов'},
      ],
      'tab':'info',
    },
    {
      'description':'Домен',
      'type':'filter_extend_text',
      'name':'domain',
      'filter_table':'domain',
      'tablename':'d',
      'db_name':'domain',
      'punycode':True,
      'filter_on':True,
      'autocomplete':True,
      'tab':'info',
    },
    {
      'description':'Домен у нас',
      'type':'filter_extend_checkbox',
      'name':'our_domain',
      'tablename':'d',
      'db_name':'our_domain',
      'tab':'info',
    },
    {
      'description':'Шаблон',
      'type':'filter_extend_select_from_table',
      'name':'template_id',
      'tablename':'t',
      'filter_table':'template',
      'table':'template',
      'header_field':'header',
      'value_field':'template_id',
      'db_name':'template_id',
      'autocomplete':True,
      'filter_on':True,
      'tab':'info',
    },
    {
      'description':'Тип шаблона',
      'type':'filter_extend_select_values',
      'name':'tmp_type',
      'tablename':'t',
      'db_name':'type',
      'values':[
        {'v':0,'d':'общий'},
        {'v':1,'d':'индивидуальный'},
        {'v':2,'d':'Эталон'},
        {'v':3,'d':'Создан на основе эталона'},
        {'v':4,'d':'эталон Landing'},
        {'v':5,'d':'создан на основе эталона Landing'},
      ],
      'tab':'info',
    },
    {
      'description':'Опции проекта',
      'type':'multiconnect_old',
      'name':'options',
      'full_str':True,
      'not_filter':1,
      'tab':'opt',
      'extended':'service_searchfiles;файлы для поисковиков;'
        'cache_promo;<span style="color: green">кешировать promo для страниц</span>;'
        'ex_links;использование собственных ссылок (ЧПУ);'
        'ex_links2;опция для совмещения ЧПУ рубрикатора и товара;'
        'ex_links_multiurl;многоязычный ЧПУ<hr/>;'
        'post_proccessing;замена тегов для оптимизации (h1,h2,h3);'
        'redirect_to_www;редирект x.com на www.x.com;'
        'redirect_from_www;редирект www.x.com на x.com;'
        'redirect_to_slash;редирект /news на /news/;'
        'redirect_from_slash;редирект /news/ на /news<hr/>;'
        'use_csv_parser_uploader;Загрузчик файлов для парсеров <b>csv</b>;'
        'use_xml_parser_uploader;Загрузчик файлов для парсеров <b>xml</b><hr/>;'
        'generate_description;Генерация дескрипшенов (ТЕСТ, НЕ НАЖИМАТЬ);'
        'new_client_backend_style;Новая клиентская админка (ТЕСТ, НЕ НАЖИМАТЬ);'
        'goods_pic_loader;загрузчик картинок по артикулу товара;'
        'promo_loader;загрузчик промо<hr/>;'
        'redirect_loader;загрузка редиректов;'
        'export_form_data;Выгрузка ФОС (заказов) в xls;'
        'add_h1;H1;'
        'ecom;E-commerce(<a href="/ecom_instruct.txt" target="_blank">Инструкция</a>);'
        'url_generator; Генерация URL;'
        'site_redirect; Редиректы;'
        'use_external_promo_loader;Загрузчик promo;'
        'use_external_promo_exporter;Выгрузка promo;'
        'use_external_sitemap_file;Использовать <b>sitemap.xml</b> в каталоге проекта;'
        'yandex_yml;включить catalog.yml;',
    },
    {
      'description':'Домены',
      'name':'domains',
      'type':'1_to_m',
      'table':'domain',
      'table_id':'domain_id',
      'foreign_key':'project_id',
      'full_str':True,
      #'view_type':'list',
      'tab':'info',
      'fields':[
        {
          'description':'Домен',
          'name':'domain',
          'type':'text',
          'slide_code':domain_slide_code,
        },
        {
          'description':'Шаблон',
          'name':'template_id',
          'type':'select_from_table',
          'table':'template',
          'value_field':'template_id',
          'header_field':'header',
          'autocomplete':True,
          'slide_code':template_slide_code,
        },
        {
          'description':'Размещение на сервере',
          'name':'server_type',
          'type':'select_values',
          'change_in_slide':True,
          'values':[
            {'v':1,'d':'CGI'},
            {'v':3,'d':'PSGI + utf8'},
            {'v':4,'d':'Python + Fastapi'},
          ],
        },
        {
          'description':'Не кешировать',
          'name':'not_cache_nginx',
          'type':'checkbox',
        },
      ],
    },
    {
      'description':'Редиректы',
      'add_description':'Чтобы редиректы работали, поставьте галку «редиректы» в опциях проекта',
      'name':'redirects',
      'type':'1_to_m',
      'table':'site_redirect',
      'table_id':'site_redirect_id',
      'full_str':True,
      'limit':10,
      'foreign_key':'project_id',
      'tab':'add_info',
      'fields':[
        {
          'description':'Откуда',
          'name':'url_from',
          'type':'text',
        },
        {
          'description':'Куда',
          'name':'url_to',
          'type':'text',
        },
        {
          'description':'Вкл',
          'name':'enabled',
          'type':'checkbox',
          'change_in_slide':True,
          'value':1,
        },
      ],
    },
    {
      'type':'multiconnect',
      'description':'Стандартные сервисы',
      'name':'struct_public',
      'relation_save_table':'project_struct_public',
      'relation_table':'struct_public',
      'relation_table_header':'header',
      'relation_table_id':'struct_public_id',
      'relation_save_table_id_relation':'struct_public_id',
      'relation_save_table_id_worktable':'project_id',
      'tab':'struct',
    },
    {
      'description':'Собственные конфиги сущностей',
      'type':'code',
      'name':'exists_conf',
      'full_str':True,
      'tab':'struct',
    },
    {
      'description':'Создать стандартную структуру',
      'type':'project_struct',
      'name':'project_struct',
      'not_filter':1,
      'tab':'struct',
    },
    {
      'description':'Расширенные сервисы',
      'type':'1_to_m',
      'name':'project_menu',
      'table':'project_menu',
      'table_id':'id',
      'full_str':True,
      'foreign_key':'project_id',
      'sort':1,
      'tab':'project_menu',
      'fields':[
        {
          'description':'Наименование раздела',
          'type':'text',
          'name':'header',
        },
        {
          'description':'Ссылка на инструмент',
          'add_description':'для проектов на perl-е',
          'type':'text',
          'name':'url',
        },
        {
          'description':'json',
          'add_description':'JSON-описание пункта меню для Vue-CRM',
          'type':'textarea',
          'name':'json',
        },
      ],
    },
    {
      'description':'Sitemap',
      'type':'project_sitemap',
      'name':'project_sitemap',
      'not_filter':1,
      'tab':'project_menu',
    },
    {
      'description':'Экспорт проекта',
      'type':'project_export',
      'name':'project_export',
      'not_filter':1,
      'tab':'tools',
    },
    {
      'description':'Клонирование проекта',
      'type':'project_clone',
      'name':'project_clone',
      'not_filter':1,
      'tab':'tools',
    },
  ],
}
