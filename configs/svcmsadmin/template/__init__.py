from config import config as cfg 

async def run_code_before_code(form,field):
  run_code_field=field['fields'][2]
  run_code_field['fast_rules']=await form.db.query(
    query=f"SELECT header,concat('{cfg['BaсkendBase']}/edit-form/template?action=fast_rule&id=',fast_rule_id) as url FROM fast_rule where rtype='url' and url_regexp='' order by header",
    values=[],
    errors=form.errors,

  )
  #form.pre(run_code_field['fast_rules'])
  

form={
  'wide_form':1,
  'work_table':'template',
  'work_table_id':'template_id',
  'title':'Шаблоны',
  'make_delete':0,
  'read_only':1,
  'tree_use':0,
  'default_find_filter':'header',
  'header_field':'header',
  'QUERY_SEARCH_TABLES':[
    {'t':'template','a':'wt'},
    {'t':'domain','a':'d','l':'d.template_id=wt.template_id','lj':1},
    {'t':'project','a':'p','l':'d.project_id=p.project_id','lj':1},
  ],
  'fields':[
    {
      'description':'Домен',
      'type':'filter_extend_text',
      'name':'domain',
      'filter_table':'domain',
      'tablename':'d',
      'header_field':'domain',
      'value_field':'domain_id',
      'db_name':'domain',
      'autocomplete':True,
      'filter_on':True,
    },
    {
      'description':'Размещение на сервере',
      'type':'filter_extend_select_values',
      'name':'server_type',
      'tablename':'d',
      'values':[
        {'v':1,'d':'CGI'},
        {'v':3,'d':'PSGI + utf8'},
        {'v':4,'d':'Fastapi'},
      ],
      'filter_on':True,
    },
    {
      'description':'Наименование шаблона',
      'type':'text',
      'name':'header',
      'regexp_rules':[
        '/^.+$/','Поле обязательно для заполнения',
      ],
      'filter_on':True,
    },

    {
      'description':'Папка с шаблонами',
      'type':'text',
      'name':'folder',
    },
    {
      'description':'Тип шаблона',
      'type':'select_values',
      'name':'type',
      'value':0,
      'regexp_rules':[
        '/^[0-9]+$/','Тип шаблона указан неверно',
      ],
      'values':[
        {'v':0,'d':'общий'},
        {'v':1,'d':'индивидуальный'},
        {'v':2,'d':'Эталон'},
        {'v':3,'d':'Создан на основе эталона'},
        {'v':4,'d':'эталон Landing'},
        {'v':5,'d':'создан на основе эталона Landing'},
        {'v':6,'d':'DS Конструктор'},
      ],
      'filter_on':True,
    },
    {
      'description':'Опции шаблона',
      'type':'multiconnect',
      'name':'options',
      # источник опций: run_code_on_fs (запускать кодовые сценарии из файловой системы)
      'relation_table':'template_options',
      'relation_table_header':'header',
      'relation_table_id':'option_id',
      'relation_save_table':'template_options_link',
      'relation_save_table_id_relation':'option_id',
      'relation_save_table_id_worktable':'template_id',
    },
    {
      'description':"Коды для URL'ов",
      'type':'1_to_m',
      'name':'url_run_code',
      'table':'url_run_code',
      'table_id':'url_run_code_id',
      'foreign_key':'template_id',
      'sort':True,
      'explain':True,
      'before_code':run_code_before_code,
      'fields':[
        {
          'description':'множество страниц',
          'name':'header',
          'type':'text',
        },
        {
          'description':'url_regexp',
          'name':'url_regexp',
          'type':'text',
        },
        {
          'description':'Код',
          'name':'run_code',
          'type':'codelist',
          
        },
      ],
    },
    {
      'description':'Константы шаблона',
      'type':'1_to_m',
      'name':'template_const',
      'table':'template_const',
      'table_id':'id',
      'foreign_key':'template_id',
      'sort':True,
      'fields':[
        {
          'description':'Название',
          'name':'description',
          'type':'text',
        },
        {
          'description':'Имя константы',
          'name':'header',
          'type':'text',
        },
        {
          'description':'Тип',
          'name':'type',
          'type':'text',
        },
      ],
    },
    {
      'description':"Шаблоны для URL'ов",
      'type':'1_to_m',
      'name':'url_rules',
      'table':'url_rules',
      'table_id':'url_rules_id',
      'foreign_key':'template_id',
      'sort':True,
      'explain':True,
      'fields':[
        {
          'description':'множество страниц',
          'name':'header',
          'type':'text',
        },
        {
          'description':'url_regexp',
          'name':'url_regexp',
          'type':'text',
        },
        {
          'description':'Наименование файла-шаблона',
          'name':'template_name',
          'type':'text',
        },
      ],
    },
    {
      'description':'Блоки Landing-a',
      'type':'1_to_m',
      'name':'landing_block',
      'table':'landing_block',
      'table_id':'id',
      'foreign_key':'template_id',
      'sort':True,
      'fields':[
        {
          'description':'Название блока в админке сайта',
          'name':'header',
          'type':'text',
          'regexp_rules':[
            '/^.+$/','Поле обязательно для заполнения',
          ],
        },
        {
          'description':'Тип блока',
          'name':'type',
          'type':'select_from_table',
          'table':'landing_block_type',
          'header_field':'header',
          'value_field':'id',
          'regexp_rules':[
            '/^\\d+$/','Тип блока должен быть выбран',
          ],
        },
      ],
    },
    {
      'description':'Группа шаблонов',
      'type':'1_to_m',
      'name':'template_group_site',
      'table':'template_group_site',
      'table_id':'id',
      'foreign_key':'template_id',
      'sort':0,
      'not_create':0,
      'make_delete':1,
      'fields':[
        {
          'description':'название переменной',
          'name':'header',
          'type':'text',
        },
        {
          'description':'Значение',
          'name':'value',
          'type':'text',
        },
      ],
    },
  ],
}
