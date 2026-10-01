# Легаси domain.pl: блок «Ссылки» (project / template / карточка ОП).
def links_code(form, field):
  v = form.values or {}
  out = ''
  if v.get('project_id'):
    out += (
      f'<a href="/edit_form/project/{v["project_id"]}" target="_blank">проект</a><br>'
    )
  if v.get('template_id'):
    out += (
      f'<a href="/edit_form/template/{v["template_id"]}" target="_blank">шаблон</a><br>'
    )
  if v.get('user_id'):
    out += (
      f'<br><a style="font-weight: bold;" '
      f'href="http://crm.digitalstrateg.ru/edit_form.pl?action=edit&id={v["user_id"]}&config=user" '
      'target="_blank">ссылка на карточку ОП</a><br>'
    )
  field['html'] = out


form={
  'work_table':'domain',
  'work_table_id':'domain_id',
  'title':'Домен',
  'make_delete':0,
  'read_only':0,
  'tree_use':0,
  'default_find_filter':'domain',
  'header_field':'domain',
  'QUERY_SEARCH_TABLES':[
    {'t':'domain','a':'wt'},
    {'t':'project','a':'p','l':'p.project_id=wt.project_id','lj':1},
    {'t':'template','a':'t','l':'t.template_id=wt.template_id','lj':1},
  ],
  'cols':[
    [
      {'description':'Ссылки','name':'links'},
      {'description':'Настройки домена','name':'main'},
      {'description':'Кеширование и работа','name':'cache'},
    ],
    [
      {'description':'SSL','name':'ssl'},
      {'description':'DNS','name':'dns'},
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
      'description':'Домен',
      'add_description':'Без www',
      'type':'text',
      'name':'domain',
      'regexp_rules':[
        '/^[a-zA-Z0-9\\-\\.]+$/','Недопустимые символы в названии домена',
      ],
      'autocomplete':True,
      'filter_on':True,
      'tab':'main',
    },
    {
      'description':'id CRM strateg',
      'type':'text',
      'name':'user_id',
      'regexp_rules':[
        '/^[0-9]+$/','ID CRM должен быть числом',
      ],
      'tab':'main',
    },
    {
      'description':'Шаблон',
      'type':'select_from_table',
      'name':'template_id',
      'autocomplete':True,
      'table':'template',
      'header_field':'header',
      'value_field':'template_id',
      'order':'header',
      'tab':'main',
    },
    {
      'description':'Проект',
      'type':'select_from_table',
      'name':'project_id',
      'autocomplete':True,
      'table':'project',
      'header_field':'header',
      'value_field':'project_id',
      'order':'header',
      'filter_on':True,
      'tab':'main',
    },
    {
      'description':'SSL',
      'type':'select_values',
      'name':'is_ssl',
      'values':[
        {'v':0,'d':'отсутствует'},
        {'v':1,'d':'платный ssl'},
        {'v':2,'d':'lets encrypt'},
      ],
      'tab':'ssl',
    },
    {
      'description':'Домены для сертификатов',
      'add_description':'каждый домен на новой строке',
      'type':'textarea',
      'name':'ssl_domains',
      'tab':'ssl',
    },
    {
      'description':'Состояние сертификата (Lets Encrypt)',
      'type':'code',
      'name':'ssl_steps',
      'full_str':True,
      'not_filter':1,
      'tab':'ssl',
    },
    {
      'description':'включен в DNS',
      'add_description':'зоны обновляются раз в 4 часа',
      'type':'checkbox',
      'name':'dns_enabled',
      'value':1,
      'tab':'dns',
    },
    {
      'description':'Serial',
      'type':'text',
      'name':'dns_serial',
      'regexp_rules':[
        '/^\\d\\d+$/','Serial должен быть числом',
      ],
      'tab':'dns',
    },
    {
      'description':'A записи',
      'type':'1_to_m',
      'name':'a_records',
      'table':'domain_dns_records_a',
      'table_id':'id',
      'foreign_key':'domain_id',
      'sort':True,
      'full_str':True,
      'tab':'dns',
      'fields':[
        {
          'description':'Домен (без точки в конце)',
          'type':'text',
          'name':'name',
        },
        {
          'description':'Адрес',
          'type':'text',
          'name':'value',
          # быстрые кнопки IP (legacy field_a_records.pl: our_ip)
          'values':[
            {'v':'178.57.220.192','d':'w01'},
            {'v':'185.76.252.13','d':'w02_n'},
          ],
        },
      ],
    },
    {
      'description':'TXT записи',
      'type':'1_to_m',
      'name':'txt_records',
      'table':'domain_dns_records_txt',
      'table_id':'id',
      'foreign_key':'domain_id',
      'sort':True,
      'full_str':True,
      'tab':'dns',
      'fields':[
        {
          'description':'Домен',
          'type':'text',
          'name':'domain',
        },
        {
          'description':'Значение',
          'type':'textarea',
          'name':'value',
          # presets: клик заполняет несколько полей записи (legacy set_txt_record)
          'presets':[
            {
              'label':'spf для stg_w01',
              'values':{
                'domain':'<%domain%>',
                'value':'v=spf1 ip4:178.57.220.192 ~all',
              },
            },
            {
              'label':'spf для stg_w02',
              'values':{
                'domain':'<%domain%>',
                'value':'v=spf1 ip4:185.87.194.51 ~all',
              },
            },
            {
              'label':'spf для stg_w01 и stg_w02',
              'values':{
                'domain':'<%domain%>',
                'value':'v=spf1 ip4:178.57.220.204 ip4:185.87.194.51 ~all',
              },
            },
          ],
        },
      ],
    },
    {
      'description':'MX записи',
      'type':'1_to_m',
      'name':'mx_records',
      'table':'domain_dns_records_mx',
      'table_id':'id',
      'foreign_key':'domain_id',
      'sort':True,
      'full_str':True,
      'tab':'dns',
      'fields':[
        {
          'description':'Домен (без точки в конце)',
          'type':'text',
          'name':'domain',
          'regexp_rules':[
            '/^(@|[a-zA-Z0-9\\*\\@][a-zA-Z0-9\\.\\-]+[a-zA-Z0-9])$/','Недопустимый домен',
          ],
        },
        {
          'description':'Приоритет',
          'type':'text',
          'name':'priority',
          'regexp_rules':[
            '/^\\d+$/','Приоритет должен быть числом',
          ],
        },
        {
          'description':'Mail сервер',
          'type':'text',
          'name':'mail_serv',
          'regexp_rules':[
            '/^[a-zA-Z0-9][a-zA-Z0-9\\.\\-\\_]+[a-zA-Z0-9]$/','Недопустимый mail сервер',
          ],
        },
      ],
    },
    {
      'description':'NS записи',
      'type':'1_to_m',
      'name':'ns_records',
      'table':'domain_dns_records_ns',
      'table_id':'id',
      'foreign_key':'domain_id',
      'sort':True,
      'full_str':True,
      'tab':'dns',
      'fields':[
        {
          'description':'Домен (без точки в конце)',
          'type':'text',
          'name':'domain',
        },
        {
          'description':'NS сервер',
          'type':'text',
          'name':'ns_serv',
        },
      ],
    },
    {
      'description':'CNAME записи',
      'type':'1_to_m',
      'name':'cname_records',
      'table':'domain_dns_records_cname',
      'table_id':'id',
      'foreign_key':'domain_id',
      'sort':True,
      'full_str':True,
      'tab':'dns',
      'fields':[
        {
          'description':'Домен (без точки в конце)',
          'type':'text',
          'name':'domain',
        },
        {
          'description':'canonical_name (без точки в конце)',
          'type':'text',
          'name':'canonical_name',
          'regexp_rules':[
            '/[^\\.]*$/','Недопустимый canonical_name',
          ],
        },
      ],
    },
    {
      'description':'Оплачено до (обновляется скриптом раз в сутки)',
      'type':'date',
      'read_only':True,
      'name':'paid_till',
      'tab':'main',
    },
    {
      'description':'дата последнего обновления paid_till',
      'type':'date',
      'read_only':True,
      'name':'last_paid_till_update',
      'tab':'main',
    },
    {
      'description':'Не создавать в конфигах nginx-a для svcms',
      'type':'checkbox',
      'name':'not_crm_server',
      'tab':'cache',
    },
    {
      'description':'Не кешировать nginx-ом',
      'type':'checkbox',
      'name':'not_cache_nginx',
      'tab':'cache',
    },
    {
      'description':'Размещение на сервере',
      'type':'select_values',
      'name':'server_type',
      'value':3,
      'values':[
        {'v':1,'d':'CGI'},
        {'v':3,'d':'PSGI + utf8'},
        {'v':4,'d':'Python + Fastapi'},
      ],
      'tab':'cache',
    },
    {
      'description':'Порт',
      'type':'text',
      'name':'port',
      'tab':'cache',
    },
    {
      'description':'',
      'type':'code',
      'name':'whois',
      'not_filter':1,
      'tab':'main',
    },
  ],
}
