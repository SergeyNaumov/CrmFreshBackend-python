from .contact_field import contact_field
from .paids_field import paids_field

fields=[
        { # фильтр / поле из user
            'description':'Наименование компании',
            'type':'filter_extend_text',
            'tablename':'u',
            'name':'firm',
            'tab':'main',
            'filter_on':True,

        },
        { # фильтр / поле из user
            'description':'ИНН',
            'type':'filter_extend_text',
            'tablename':'u',
            'tab':'main',
            'name':'inn',
        },
        {
            'description':'Дата создания',
            'type':'date',
            'name':'registered',
            'read_only':1,
            'filter_on':1,
            'tab':'main',
        },
        {
            'description':'Дата следующего контакта',
            'type':'date',
            'name':'contact_date',
            'tab':'ofp',
            'tab':'main',
        },
        {
          'description':'Статус клиента',
          'type':'select_values',
          'name':'status',
          'values':[
            {'v':1,'d':'В работе'},
            {'v':2,'d':'Заявка подана'},
            {'v':3,'d':'Одобрено, получена платёжка','c':'forestgreen'},
            {'v':4,'d':'Одобрено, отказ клиента','c':'red'},
            {'v':5,'d':'Отказ банка / МФО','c':'red'},
            
            #{'v':7,'d':'Отказ'},


          ],
          'tab':'main',
        },
        {
            'description':'Вид продукта',
            'name': 'product',
            #'regexp_rules': [
            #    '/^\d+$/','выберите корректное значение'
            #],
            #'regexp':'/^\d*[1-9]$/',
            'multiple':5,
            'values':[
              {'v':'1','d':'Кредит на исполнение контракта'},
              {'v':'2','d':'Банковская гарантия на исполнение контракта'},
              {'v':'3','d':'Лимиты'},
              {'v':'4','d':'Банковская гарантия на Гарантийные обязательства'},
              {'v':'5','d':'Банковская на участие в закупке'},
              {'v':'6','d':'Коммерческая банковская гарантия'},
              {'v':'7','d':'Тендерный займ'},
              {'v':'8','d':'Лизинг'},
              {'v':'9','d':'Страхование'},
              {'v':'10','d':'Кредит оборотный'},
            ],            'type':'select_values', 
            #'frontend':{'ajax':{'name':'product','timeout':600}},
            'tab':'main',
        },
        { # формируем ссылку на реестровый номер
          'description':'РНТ номер',
          'type':'text',
          'name':'rnt',
          'replace_rules':[
                '/^\s+/', '',
                '/\s+$/', '',
           ],
          'regexp_rules':[
            '/\S+/i','обязательно для заполнения',
          ],
          'frontend':{'ajax':{'name':'rnt','timeout':600}},
          'tab':'main',
        },
        # Контакты
        contact_field
        ,
        # Платежи
        #paids_field,





        {
          'description':'Файлы',
          'tab':'main',
          'type':'1_to_m',
          'table':'user_fin_files',
          'table_id':'id',
          'name':'files',
          'foreign_key':'user_fin_id',
          'view_type':'list',
          'fields':[
            {
              'description':'файл',
              'type':'file',
              'keep_orig_filename':1,
              'filedir':'./files/user_fin',
              'name':'attach'
            }
          ]
        },
        {
          'description':'Поставщик',
          'tab':'main',
          'type':'select_from_table',
          'name':'supplier_id',
          'table':'user',
          'where':'supplier=1',
          'header_field':'firm',
          'value_field':'id',
          'tablename':'s',
        },
        {
          'description':'Сумма сделки',
          'tab':'main',
          'type':'text',
          'name':'sum_operation',
          'filter_type':'range',
          'regexp_rules': [
              '/^\d*$/','выберите корректное значение'
          ],
          'replace_rules': [
              '/[^\d]+/g',''
          ]
        },
        # {
        #     'description':'Контактное лицо',
        #     'type':'text',
        #     'name':'contact',
        #     'tab':'main',
        # },
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
            'name':'manager_id',
            'header_field':'name',
            'order':'name',
            'value_field':'id',
            'tablename':'m',
            'tab':'work',
            'where':"gone=0",
            'read_only':True,
            'filter_on':True
        },
        {
            'description':'Группа менеджеров фин. услуг',
            'name': 'group_id',
            'type':'select_from_table',
            'table':'manager_group',
            'tablename':'mg',
            'header_field':'header',
            'value_field':'id',
            # 211 -- право "менеджер фин. услуг"
            'where':'id in (select group_id from manager_group_permissions where permissions_id=211)',
            'tab':'work',
            'read_only':True,
        },
        {
            'description':'Менеджер фин. услуг',
            'type':'select_from_table',
            'table':'manager',
            'name':'manager_fin',
            'header_field':'name',
            'order':'name',
            'tablename':'m_fin',
            'value_field':'id',
            'read_only':True,
            # 196 -- юрист (lawer)
            'where':"""gone=0 and group_id in (select group_id from manager_group_permissions where permissions_id=211)""",# Андеррайтер пока только Деженков
            'tab':'work',
        },
        {
            'description':'Андеррайтер',
            'type':'select_from_table',
            'table':'manager',
            'name':'underwriter',
            'header_field':'name',
            'order':'name',
            'tablename':'m_un',
            'value_field':'id',
            'where':"""gone=0 and group_id in (select group_id from manager_group_permissions where permissions_id=212)""",# Андеррайтер пока только Деженков
            'read_only':1,
            'tab':'work',         
        },
        {
          'description':'Комментарии',
          'name':'memo',
          'type':'memo',
          'memo_table':'user_fin_memo',
          'memo_table_id':'id',
          'memo_table_comment':'comment',
          'memo_table_auth_id':'manager_id',
          'memo_table_registered':'registered',
          'memo_table_foreign_key':'user_fin_id',
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