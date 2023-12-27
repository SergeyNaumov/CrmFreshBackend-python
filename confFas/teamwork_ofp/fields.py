from .contact_field import contact_field
fields=[

        # {
        #     'description':'№',
        #     'type':'text',
        #     'name':'teamwork_ofp_id',
        #     'tab':'ofp',
        #     'read_only':True,

        # },
        {
            'description':'Дата создания',
            'type':'date',
            'name':'born',
            'read_only':1,
            'filter_on':1,
            'tab':'main',
        },
        {
            'description':'Дата следующего контакта',
            'type':'datetime',
            'name':'contact_date',
            'tab':'ofp',
            'tab':'main',
        },
        {
            'description':'Наименование компании',
            'type':'filter_extend_text',
            'tablename':'u',
            'name':'firm',
            'filter_on':True,
            'tab':'main',
        },
        {
            'description':'ИНН',
            'type':'filter_extend_text',
            'tablename':'u',
            'name':'inn',
            #'regexp_rules':[
            #    '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            #],
            #'replace_rules':[
            #    '/[^0-9]/', ''
            #],
            'tab':'main',
        },

        { # формируем ссылку на реестровый номер (доделать!!!)
          'description':'Реестровый номер',
          'type':'text',
          'name':'regnumber',
          'replace_rules':[
                '/^\s+/', '',
                '/\s+$/', '',
           ],
          'regexp_rules':[
            '/\S+/i','обязательно для заполнения',
          ],
          'frontend':{'ajax':{'name':'regnumber','timeout':600}},
          'tab':'main',
        },
        {
          'description':'Статус победы',
          'type':'select_values',
          'name':'win_status',
          'values':[
            {'v':1,'d':'Победа','c':'forestgreen'},
            {'v':2,'d':'В работе','c':'yellow'},
            {'v':3,'d':'Поражение','c':'red'},
            {'v':4,'d':'Работа не велась, оплаты не было','c':'blue'},
          ],
          'tab':'main',
        },
        {
          'description':'Дата изменения статуса победы',
          'type':'date',
          'name':'win_status_change_date',
          'read_only':1,
          'tab':'main',
        },
        {
          'description':'Председатель комиссии',
          'type':'text',
          'name':'pred_comm',
          'placeholder':'обязательно укажите председателя комиссии',
          'tab':'main',
        },
        # Контакты
        contact_field
        ,
        # {
        #   'description':'Статус клиента',
        #   'name':'client_status',
        #   'type':'select_values',
        #   'values':[
        #     {'v':3,'d':'В работе'},
        #     {'v':6,'d':'Заявка подана'},
        #     {'v':2,'d':'Одобрено, получена платежка'},
        #     {'v':4,'d':'Одобрено, отказ клиента'},
        #     {'v':1,'d':'Отказ Банка/МФО'},
        #     {'v':9,'d':'Передан в гр. Тихонова по регламенту'},
        #   ],
        #   'tab':'work',
        #   #'read_only':1,
        #   #'before_code':client_status_before_code
        # },

        {
            'description':'Вид продукта',
            'name': 'product',
            'regexp_rules': [
                '/^\d+$/','выберите корректное значение'
            ],
            'multiple':5,
            'values':[
              {'v':3,'d':'Банковская Гарантия (Аукцион выигран с нашей помощью)'},
              {'v':4,'d':'Банковская Гарантия (есть победитель)'},
              {'v':5,'d':'Банковская гарантия, консультация для продажи тарифа (50/50 от оплаченного тарифа)'},
              {'v':10,'d':'Банковская гарантия (консультация на будущее)'},
              {'v':7,'d':'Тендерный займ (нужен под конкретный аукцион)'},
              {'v':8,'d':'Подготовка документации'},
              {'v':9,'d':'Юридические услуги (разное)'},
              {'v':14,'d':'Юридические услуги (ФАС)'},
              {'v':15,'d':'Юридические услуги (Арбитраж)'},
              {'v':11,'d':'Оформление сро, Лицензий, Допусков'},
              {'v':12,'d':'Лизинг'},
              {'v':13,'d':'Факторинг'},


            ],
            'type':'select_values', 
            'frontend':{'ajax':{'name':'product','timeout':600}},
            'tab':'main',
        },
        {
          'description':'Дата и время заседания',
          'type':'datetime',
          'name':'dat_session',
          'read_only':True,
          'tab':'main',
          
        },
        {
          'description':'Представитель',
          'type':'select_from_table',
          'name':'exhibitor_id',
          'table':'manager',
          'tablename':'me',
          'where':'group_id in (select id from manager_group where parent_id=347 or path regexp "/347/")', # группа 
          'header_field':'name',
          'value_field':'id',
          'tab':'main',
        },
        # !!!!не отображается список, наладить
        {
          'description':'Город заседания',
          'type':'select_from_table',
          'autocomplete':True,
          'name':'city_id',
          'table':'city',
          'tablename':'city',
          'header_field':'name',
          'search_query':"""
              SELECT
                c.city_id v, concat(r.header,' -> ', c.name ) d
              FROM
                city c
                join region r ON (r.region_id=c.region_id)
                where c.name like <%v%>
          """,
          'value_field':'city_id',     
          'tab':'main',
        },
       {
          'description':'Время вылета на заседание',
          'name':'date_fly_to',
          'type':'datetime',
          'tab':'main',
        },
        {
          'description':'Время возвращения с заседания',
          'name':'date_fly_from',
          'type':'datetime',
          'tab':'main',
          
        },
        {
          'description':'Файл',
          'name':'attach',
          'type':'file',
          'tab':'main',
          'filedir':'./files/teamwork_ofp',
        },
        {
          'description':'Файлы',
          'tab':'main',
          'type':'1_to_m',
          'table':'teamwork_ofp_files',
          'table_id':'id',
          'name':'files',
          'foreign_key':'teamwork_ofp_id',
          'view_type':'list',
          'fields':[
            {
              'description':'файл',
              'type':'file',
              'keep_orig_filename':1,
              'filedir':'./files/teamwork_ofp',
              'name':'attach'
            }
          ]
        },
        {
            'description':'Контактное лицо',
            'type':'text',
            'name':'contact',
            'tab':'main',
        },
        {
            'description':'Группа менеджеров',
            'type':'filter_extend_select_from_table', # фильтр для сложного запроса
            'table':'manager_group',
            'name':'managers_groups_name',
            'tablename':'mfg',
            'db_name':'id',
            # название таблицы, из которой будет происходить выборка по этому фильтру
            'filter_table': 'manager_group',
            'header_field': 'header',
            'value_field': 'id',
            'tree_use':True,
            'tab':'work',
        },
        {
            'description':'Менеджер ОП',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_from',
            'header_field':'name',
            'order':'name',
            'value_field':'id',
            'tablename':'mf',
            'tab':'work',
            'read_only':True,
            'filter_on':True
        },
        {
            'description':'Юрист',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_to',
            'header_field':'name',
            'order':'name',
            'tablename':'mt',
            'value_field':'id',
            # 196 -- юрист (lawer)
            'where':'(group_id IN (select group_id from manager_group_permissions where permissions_id=196))',# OR id (select manager_id from manager_permissions where permissions_id=196))',
            'tab':'work',
        },
        {
            'description':'Юрист2',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_to2',
            'header_field':'name',
            'order':'name',
            'tablename':'mt2',
            'value_field':'id',
            'where':'(group_id IN (select group_id from manager_group_permissions where permissions_id=196))',# OR id (select manager_id from manager_permissions where permissions_id=196))',
            'read_only':1,
            'tab':'work',         
        },
        {
          'description':'Комментарии',
          'name':'comment1',
          'type':'memo',
          'memo_table':'teamwork_ofp_memo',
          'memo_table_id':'id',
          'memo_table_comment':'comment',
          'memo_table_auth_id':'manager_id',
          'memo_table_registered':'registered',
          'memo_table_foreign_key':'teamwork_ofp_id',
          'auth_table':'manager',
          'auth_login_field':'login',
          'auth_id_field':'id',
          'auth_name_field':'name',
          'reverse':1,
          'memo_table_alias':'memo',
          'auth_table_alias':'m_memo',
          'make_delete':False,
          'make_edit':False,
          'tab':'work',
        }
    ]