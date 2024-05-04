
def manager_otk_is_double_fc(form,field,row):
    firm=row.get('u_otk__firm') or '---'
    return f"{row['wt__manager_otk_is_double']}<br><a href='/edit_form/users/{row['u_otk__id']}' target='_blank'>{firm}</a>"

def is_double_filter_code(form,field,row):
    if row['wt__is_double']:
        firm = row.get('u__firm') or '---'
        return f"да<br><a href='/edit_form/user/{row['u__id']}' target='_blank'>{firm}</a>"
    else:
        return 'нет'

def start_price_filter_code(form,field,row):
    return row['wt__start_price']

def manager_dt2_is_double_fc(form,field,row):
    firm=row['u_dt2__firm'] or '---'
    return f"{row['wt__manager_dt2_is_double']}<br><a href='/edit_form/users_card/{row['u_dt2__id']}' target='_blank'>{firm}</a>"

form={
    'work_table':'brand',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Реестр РНП',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'QUERY_SEARCH_TABLES':[
        {'t':'rnp_reestr_from_FTP','a':'wt'},
        {'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1},
        {'t':'user','a':'u','l':'wt.user_id=u.id','lj':1},
        {'t':'manager','a':'m_otk','l':'wt.manager_otk=m_otk.id','lj':1,'for_fields':['manager_otk']},
        {'t':'manager','a':'m_dt2','l':'wt.manager_dt2=m_dt2.id','lj':1,'for_fields':['manager_dt2']},
        {'t':'user','a':'u_otk','l':'wt.manager_otk_users_id=u_otk.id','lj':1,'for_fields':['manager_otk_is_double']},
        {'t':'user','a':'u_dt2','l':'wt.manager_dt2_users_id=u_dt2.id','lj':1,'for_fields':['manager_dt2_is_double']},


    ],
    'fields': [ 
    {
      'description':'Время добавления в базу',
      'type':'datetime',
      'name':'registered',

    },
    {
      'description':'Время распределения',
      'type':'datetime',
      'name':'time_manager_set',


    },
    {
      'description':'Менеджер',
      'type':'filter_extend_select_from_table',
      'table':'manager',
      'tablename':'m',
      'name':'manager_id',
      'header_field':'name',
      'value_field':'id'
    },
    {
      'description':'Дубль',
      'name':'is_double',
      'type':'checkbox',
      'filter_code':is_double_filter_code
    },
    {'description':'Реестровый номер','type':'text','name':'reestr_number'},
    {'description':'Дата подтверждения','type':'date','name':'approve_date'},
    {
      'description':'Статус примечания','type':'select_values','name':'note_status',
      'values':[
        {'v':1,'d':'Отказ во включение в РНП'},
        {'v':2,'d':'Опубликована'},
        {'v':3,'d':'Заявка на исключение сведений'},
        {'v':4,'d':'Информация исключена из РНП на время судебного разбирательства'},
        {'v':5,'d':'Информация исключена из РНП. Архив'},
      ]
    },
    {
      'description':'ФЗ','name':'law_type','type':'select_values',
      'values':[
        {'v':1,'d':'44 ФЗ'},
        {'v':2,'d':'223 ФЗ'},
        {'v':3,'d':'615 ФЗ'},
      ]
    },
    {'description':'Номер закупки','type':'text','name':'purchase_number'},
    {'description':'Объект закупки','type':'','name':'purchase_object'},
    {
      'description':'Начальная цена контракта','type':'text','filter_type':'range','name':'start_price',
      'filter_code':start_price_filter_code
    },
    {'description':'ИНН организации','type':'text','name':'client_inn'},
    {'description':'Название организации','type':'text','name':'client_name'},
    {'description':'Город организации','type':'text','name':'client_address'},
    {'description':'ИНН заказчика','type':'text','name':'customer_inn'},
    {'description':'КПП заказчика','type':'text','name':'customer_kpp'},
    {'description':'Название заказчика','type':'text','name':'customer_name'},
    {'description':'Адрес заказчика','type':'text','name':'customer_address'},
    {'description':'fas код','type':'text','name':'fas_code'},
    {'description':'fas имя','type':'text','name':'fas_name'},
    {'description':'Город УФАС','type':'text','name':'fas_region'},
    {
      'description':'Причина','type':'select_values','name':'include_reason',
      'values':[
        {'v':1,'d':'Уклонение победителя от заключения контракта'},
        {'v':2,'d':'Уклонение единственного участника от заключения контракта'},
        {'v':3,'d':'Уклонение победителя от заключения контракта'},
        {'v':4,'d':'Расторжение контракта'},
        {'v':5,'d':'Отмена контракта'},
        {'v':6,'d':'Решение суда по отмене договора'},
      ]
    },
    {
      'description':'Причина1',
      'name':'reason_1',
      'type':'text'
    },
    {
      'description':'Причина2',
      'name':'reason_2',
      'type':'text'
    },
    {
      'description':'Менеджер ОТК',
      'name':'manager_otk',
      'type':'select_from_table',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',

      'tablename':'m_otk'
    },

    {
      'description':'Дубль (при распределении на ОТК)',
      'name':'manager_otk_is_double',
      'filter_on':0,
      'type':'checkbox',
      'filter_code': manager_otk_is_double_fc

    },
    {
      'description':'Момент распределения ОТК',
      'name':'manager_otk_moment',
      'type':'datetime',
      'filter_on':0,


    },
    {
      'description':'Менеджер ДТ2',
      'name':'manager_dt2',
      'type':'select_from_table',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',
      'filter_on':0,
      'tablename':'m_dt2'
    },
    {
      'description':'Дубль (при распределении на ДТ2)',
      'name':'manager_dt2_is_double',
      'filter_on':0,
      'type':'checkbox',
      'filter_code': manager_dt2_is_double_fc


    },
    {
      'description':'Момент распределения ДТ2',
      'name':'manager_dt2_moment',
      'type':'datetime',
      'filter_on':0,
    },

  ]  
    
}
      

