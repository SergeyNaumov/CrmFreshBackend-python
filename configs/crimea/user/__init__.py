"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
from .query_search_tables import *
def without_send(form,field,newpass):
    return

form={
    'work_table':'user',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Члены СНТ',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':query_search_tables,
# """
# | id       | int(10) unsigned | NO   | PRI | NULL    | auto_increment |
# | snt_id   | int(10) unsigned | YES  | MUL | NULL    |                |
# | name     | varchar(100)     | NO   |     |         |                |
# | num      | varchar(5)       | NO   |     |         |                |
# | email    | varchar(100)     | NO   |     |         |                |
# | phone    | varchar(20)      | NO   |     |         |                |
# | login    | varchar(20)      | NO   |     |         |                |
# | password | varchar(20)      | NO   |     |         |                |

# """
    'fields': [ 
        {
            'description':'СНТ',
            'type':'select_from_table',
            'name':'snt_id',
            'table':'snt',
            'header_field':'header',
            'value_field':'id',
            'tablename':'snt',
            'regexp_rules':[
                '/^[1-9][0-9]*$/','Поле, обязательное для заполнения'
            ],
            'filter_on':True
        },
        {
            'description':'Логин',
            'type':'text',
            'name':'login',
            'regexp_rules':[
                '/^.+$/','заполните поле'
            ],
            'filter_on':True
        },
        {
            'description':'Пароль',
            'type':'text',
            'name':'password',
            'min_length':6,
            'symbols':'123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
            'methods_send':[
                # {
                #   'description':'сохранить и отправить по электронной почте',
                #   'method_send':send_new_password
                # },
                {
                  'description':'сохранить и никуда не отправлять',
                  'method_send': without_send
                }
            ],
            'filter_on':True
        },
        {
            'description':'ФИО',
            'type':'text',
            'name':'name',
            'filter_on':True
        },
        {
            'description':'Номер участка',
            'type':'text',
            'name':'num',
            'filter_on':True
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
            'filter_on':True
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
            'filter_on':True
        },
  ]  
    
}
      


