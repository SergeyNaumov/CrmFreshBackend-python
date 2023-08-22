from lib.core import exists_arg
from lib.CRM.form import Form
#from .fields import get_fields

#from .ajax import ajax
def firm_filter_code(form,field,row):
    return f"<a href='/edit_form/user/{row['wt__id']}' target='_blank'>{row['wt__firm']}</a>"

def otk_before_code(form,field):
    if exists_arg('admin_otk', form.manager['permissions']):
        field['read_only']=False
    

def dt2_before_code(form,field):
    if exists_arg('admin_dt2', form.manager['permissions']):
        field['read_only']=False
def kladr_after_search(data):
    i=0
    list=[]
    if not data:
        return list
    
    for d in data:
        res=[]
        for d2 in d['parents']:

            if d2['name']=='Москва' and d2['contentType']!='city':
                continue
            res.append,f'{d2["typeShort"]} {d2["name"]}'


        res.append(f'{d["typeShort"]} {d["name"]}')
        h=', '.join(res)
        list.append({'header':h})
    return list

form={
    'wide_form':True,
    'title':'Карты ОП',
    'work_table':'user',
    #'ajax':ajax,
    'is_admin':False,
    'QUERY_SEARCH_TABLES':[
            {'table':'user','alias':'wt'},
            {'t':'manager','a':'m','l':'m.id=wt.manager_id','lj':1,'for_fields':['manager_id','f_manager_group']},
            {'t':'manager_group', 'a':'mg', 'l':'m.group_id','for_fields':['f_manager_group']},
            {'t':'user_contact','a':'uc','l':'uc.user_id=wt.id','lj':1, 'for_fields':['f_fio','f_email','f_phone']},
    ],
    'cols':[
            [ # Колонка1
              {'description':'Общая информация','name':'main','hide':0},
            ],
            [
              {'description':'Продажи','name':'sale','hide':0},
            ]
    ],
    'filters_groups':[],
    # 'on_filters':[
    #     {
    #      'name':'address'
    #     },
    #     {
    #      'name':'f_date',
    #      #'value':["2020-01-01","2020-01-02"]
    #     },
    # ],
    #'search_on_load':1,

    #'not_create':1,
    #'read_only':1,
    'GROUP_BY':'wt.id',
    'fields':[

        {
            'description':'Название компании',
            'name':'firm',
            'type':'text',
            'tab':'main',
            'filter_on':True,
            'filter_code':firm_filter_code

        },
        {
            'description':'Город',
            'name':'city',
            'type':'text',
            'tab':'main'
        },
        {
            'description':'Адрес',
            'name':'address',
            'subtype':'kladr',
            'kladr':{
                #'after_search':kladr_after_search
            },
            'type':'text',
            'tab':'main'
        },
        {
            'description':'Инн',
            'add_description':'для ИП 12 цифр, для остальных организаций 10',
            'name':'inn',
            'type':'text',
            'tab':'main',
            'regexp_rules':[
                '/^(\d{10}|\d{12})?$/i','Инн может быть 10 или 12 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ]
        },
        {
            'description':'КПП',
            'name':'kpp',
            'type':'text',
            'tab':'main',
            'regexp_rules':[
                '/^(\d{9})?$/i','КПП должен содержать 9 цифр',
            ],
            'replace_rules':[
                '/[^0-9]/', ''
            ],
            #'subtype':'qr_call',
        },
        {
            'description':'Зарегистрирована',
            'name':'registered',
            'type':'date',
            'read_only':True,
            'tab':'main',
        },
        {
            'description':'Контакты',
            'name':'contacts',
            'type':'1_to_m',
            'table':'user_contact',
            'foreign_key':'user_id',
            'table_id':'id',
            'view_type':'list',
            'fields':[
                {
                    'description':'ФИО',
                    'name':'fio',
                    'type':'text',
                },
                {
                    'description':'Email',
                    'name':'email',
                    'type':'text',
                },
                {
                    'description':'Телефон',
                    #'add_description':'В формате +7XXXXXXXXXX, например: +74951234567',
                    'name':'phone',
                    'type':'text',
                    'subtype':'qr_call',
                    'replace_rules':[
                        '/^8/','+7',
                        '/^92/', '+792',
                        '/;/g',',',
                        
                        '/,$/',', ',
                        '/\s+,/', ', ',
                        '/\s+,/g', ',',
                        '/[^\s,\d\+]/g','',
                        '/, 8/',', +7',
                        #'\s\s+',' ',
                        #'/^\s+/','',
                        #'/\s+,/',', ',
                        
                        

                    ],
                    'regexp_rules':[
                        '/^(\+\d{6,12})(,\s\+\d{6,12})*$/','Номер должен быть в формате: +[код]XXXXXXXXXX, например: +74951234567',
                       
                    ],
                },
                {
                    'description':'Должность',
                    'name':'position',
                    'type':'text',
                },
                {
                    'description':'Ответственный',
                    'name':'otv',
                    'type':'checkbox',
                },
                {
                    'description':'Комментарий',
                    'name':'comment',
                    'type':'text',
                },
            ],
            'tab':'main',
        },        
        {
            'description':'Менеджер',
            'name':'manager_id',
            'type':'select_from_table',
            'table':'manager',
            'tablename':'m',
            'header_field':'name',
            'value_field':'id',
            'tab':'sale',
            'filter_on':True
        },
        {
            'description':'Группы менеджеров',
            'type':'filter_extend_select_from_table',
            'name':'f_manager_group',
            'table':'manager_group',
            #'tree_use':True,
            'tablename':'mg',
            'header_field':'header',
            'value_field':'id'
        },
        {
            'description':'Дата контакта',
            'name':'contact_date',
            'type':'date',
            'tab':'sale',
        },
        { # Memo
            # Комментарий 
            'description':'Состояние',
            'name':'memo',
            'type':'memo',
            'memo_table':'user_memo',
            'memo_table_id':'id',
            'memo_table_comment':'body',
            'memo_table_auth_id':'manager_id',
            'memo_table_registered':'registered',
            'memo_table_foreign_key':'user_id',
            'auth_table':'manager',
            'auth_login_field':'login',
            'auth_id_field':'id',
            'auth_name_field':'name',
            'reverse':1,
            'memo_table_alias':'memo',
            'auth_table_alias':'m_memo',
            'make_delete':False,
            'make_edit':False,
            'tab':'sale'
        },
        {
            'description':'Состояние2',
            'name':'state2',
            'type':'textarea',
            'tab':'sale'
        },
        {
            'description':'ОТК',
            'name':'otk',
            'type':'checkbox',
            'read_only':True,
            'before_code':otk_before_code,
            'tab':'sale',
        },
        {
            'description':'ДТ2',
            'name':'dt2',
            'type':'checkbox',
            'read_only':True,
            'before_code':dt2_before_code,
            'tab':'sale',
        },
        {
            'description':'Презентация заявки',
            'name':'prez_order',
            'type':'checkbox',
            'tab':'sale',
        },
        {
            'description':'Презентация заявки, отмена',
            'name':'prez_order_cancel',
            'type':'checkbox',
            'tab':'sale',
        },
        # {
        #     'description':'',
        #     'name':'',
        #     'type':'',
        #     'tab':'sale',
        # },
        # {
        #     'description':'',
        #     'name':'',
        #     'type':'',
        #     'tab':'sale',
        # },
    ]
}

#form['fields']=get_fields()


