from lib.core import cur_date
def today_filter(form,field):
  if form.script=='admin_table':
    field['value']=[cur_date(),'']

def get_fields():
  return [

      {
        'description':'Время парсинга',
        'type':'date',
        'name':'registered',
        'filter_on':1,
        'before_code': today_filter
      },
      {
        'description':'№дела',
        'tablename':'c',
        'table':'c',
        'name':'case_number',
        'type':'filter_extend_text',
        'filter_on':1
      },
      {
        'description':'Предмет спора',
        'tablename':'c',
        'table':'c',
        'name':'dispute_subject',
        'type':'filter_extend_text',
        'filter_on':1
      },
      {
        'description':'Суд',
        'type':'filter_extend_select_from_table',
        'table':'arbitrage_court',
        'name':'court_name',
        'tablename':'court',
        'header_field':'name',
        'value_field':'id',
        'db_name':'id',
        'filter_on':1
      },
      {
        'description':'Ответчик',
        'type':'text',
        'name':'name',
        'filter_on':1
      },
      {
        'description':'ИНН',
        'type':'filter_extent_text',
        'tablename':'e',
        'name':'inn',
        'filter_on':1
      },
      {
        'description':'КПП',
        'type':'filter_extent_text',
        'tablename':'e',
        'type':'text',
        'name':'kpp',
        'filter_on':1
      },
      {
        'description':'ОГРН',
        'type':'filter_extent_text',
        'tablename':'e',
        'type':'text',
        'name':'ogrn',
        'filter_on':1
      },
      {
        'description':'ОКАТО',
        'type':'filter_extent_text',
        'tablename':'e',
        'type':'text',
        'name':'okato',
        'filter_on':1
      },
      {
        'description':'Телефон',
        'type':'filter_extent_text',
        'tablename':'phone',
        'name':'phone',
        'filter_on':1
      },
      {
        'description':'Email',
        'type':'filter_extent_text',
        'tablename':'email',
        'name':'email',
        'filter_on':1
      },
      {
          'description':'Дата регистрации карты ОП',
          'type':'filter_extend_date',
          'name':'u_registered',
          'tablename':'u',
          'db_name':'registered',
          'filter_on':True,
          #'value':['2023-08-01','2023-08-02']

      },
      {
        'description':'Распределено на',
        'type':'filter_extend_select_from_table',
        'name':'manager_id',
        'table':'manager',
        'tablename':'m',
        'db_name':'id',
        'header_field':'name',
        'value_field':'id',
        'filter_on':1
      },
      {
        'description':'ID карты ОП',
        'type':'filter_extend_text',
        'tablename':'tr',
        'filter_type':'range',
        'name':'user_id',
        #'read_only':1,
        'filter_on':1,
      },
      # {
      #   'description':'Тип дела',
      #   'name':'type_id',
      #   'type':'select_from_table',
      #   'table':'arbitrage_case_type',
      #   'tablename':'t',
      #   'header_field':'header',
      #   'value_field':'id',
      #   'filter_on':1
      # },
      # {
      #   'description':'Суд',
      #   'name':'court_id',
      #   'type':'select_from_table',
      #   'table':'arbitrage_court',
      #   'tablename':'c',
      #   'header_field':'name',
      #   'value_field':'id',
      #   'filter_on':1
      # },
      # {
      #   'description':'Предмет спора',
      #   'name':'dispute_subject',
      #   'type':'text',
      #   'filter_on':1
      # },
      # {
      #   'description':'Дата',
      #   'name':'date',
      #   'type':'date',
      #   'filter_on':1
      # },
      # {
      #   'description':'Сумма',
      #   'name':'summa',
      #   'filter_type':'range',
      #   'type':'text',
      #   'filter_on':1
      # },
      # {
      #   'description':'Истец',
      #   'name':'pl',
      #   'type':'text',
      #   'not_process':1,
      #   'filter_on':1
      # },
      # {
      #   'description':'Ответчик',
      #   'name':'resp',
      #   'type':'text',
      #   'not_process':1,
      #   'filter_on':1
      # },
  ]