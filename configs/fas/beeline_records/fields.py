from lib.core import cur_date

def before_code_date(form,field):
  if form.script=='admin_table':
    field['value']=[cur_date(),cur_date()]


fields=[ 
    {
      'description':'Дата',
      'type':'date',
      'name':'date',
      'before_code':before_code_date,
      'filter_on':1
    },
    {
      'description':'Тип звонка',
      'type':'select_values',
      'values':[
        {'v':'INBOUND','d':'Входящий'},
        {'v':'OUTBOUND','d':'Исходящий'},
      ],
      'name':'direction',
      'filter_on':1
    },
    {
      'description':'Продолжительность, сек',
      'type':'text',
      'name':'duration',
      'filter_type':'range',
      'filter_on':1
    },
    {
      'description':'Менеджер',
      'type':'filter_extend_select_from_table',
      'name':'manager_name',
      'table':'manager',
      'tablename':'m',
      'header_field':'name',
      'value_field':'id',
      'db_name':'id',
      'where':'id in (select manager_id from beeline_abonent)',
      'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },


]