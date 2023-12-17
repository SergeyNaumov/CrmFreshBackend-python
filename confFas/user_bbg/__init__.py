from .contact_field import contact_field
from .query_search_tables import QUERY_SEARCH_TABLES

form={
    'work_table':'user_bbg',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Пользователи BBG',
    'sort':False,
    'tree_use':False,
    'explain':False,
    'not_create':True,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':QUERY_SEARCH_TABLES,
    'GROUP_BY':'wt.id',
    'make_delete':False,
    'read_only':True,
    'fields': [ 
        {
          'description':'Время создания',
          'type':'datetime',
          'name':'registered',
          'read_only':1,
          'filter_on':1
        },
        {
          'description':'Дата следующего контакта',
          'type':'date',
          'name':'next_contact',
          'filter_on':1
        },

        {
          'description':'Наименование компании',
          'type':'code',
          'name':'firm'
        },
        {
          'description':'ИНН',
          'type':'code',
          'name':'inn'
        },
        {
          'type':'code',
          'name':'links'
        },
        {
          'description':'Вид продукта',
          'type':'select_values',
          'values':[
            {'v':'1','d':'Кредит на исполнение контракта'},
            {'v':'2','d':'Банковская гарантия на исполнение контракта'},
            {'v':'3','d':'Лимиты'},
            {'v':'4','d':'Банковская гарантия на Гарантийные обязательства'},
            {'v':'5','d':'Банковская на участие в закупке'},
            {'v':'6','d':'Коммерческая банковская гарантия'},
            {'v':'7','d':'Тендерный займ'},
          ],
          'name':'product',
        },
        {
          'description':'Реестровый номер аукциона',
          'type':'text',
          'name':'reg_number',
        },
        {
          'description':'Дата подписания контракта',
          'type':'date',
          'name':'contract_date',
        },
        contact_field,
        {
          'description':'Менеджер',
          'type':'select_from_table',
          'name':'manager_id',
          'table':'manager',
          'tablename':'m',
          'header_field':'name',
          'value_field':'id',
          'read_only':1,
          'filter_on':1
        },
        {
          'description':'Менеджер ББГ',
          'type':'select_from_table',
          'table':'manager',
          'tablename':'mb',
          'header_field':'name',
          'value_field':'id',
          'name':'manager_bbg',
          # право "card_bbg_manager" (менеджер ББГ)
          'where':'(id IN (select manager_id from manager_permissions where permissions_id=201))',
          'read_only':1,
          'filter_on':1

        },
        { # Memo
            # Комментарий
            'description':'Комментарий',
            'name':'memo',
            'type':'memo',
            'memo_table':'user_bbg_memo',
            'memo_table_id':'id',
            'memo_table_comment':'body',
            'memo_table_auth_id':'manager_id',
            'memo_table_registered':'registered',
            'memo_table_foreign_key':'user_bbg_id',
            'auth_table':'manager',
            'auth_login_field':'login',
            'auth_id_field':'id',
            'auth_name_field':'name',
            'reverse':1,
            'memo_table_alias':'memo',
            'auth_table_alias':'m_memo',
            'make_delete':False,
            'make_edit':False,
            'tab':'sale',
            'show_type':'html',
            'filter_on':1
        },

  ]  
    
}
      


