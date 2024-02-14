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
        'name':'case_number',
        'type':'text',
        'filter_on':1
      },
      {
        'description':'Тип',
        'name':'type_id',
        'type':'select_from_table',
        'table':'arbitrage_case_type',
        'tablename':'t',
        'header_field':'header',
        'value_field':'id',
        'filter_on':1
      },
      {
        'description':'Суд',
        'name':'court_id',
        'type':'select_from_table',
        'table':'arbitrage_court',
        'tablename':'c',
        'header_field':'name',
        'value_field':'id',
        'filter_on':1
      },
      {
        'description':'Предмет спора',
        'name':'dispute_subject',
        'type':'text',
        'filter_on':1
      },
      {
        'description':'Дата',
        'name':'date',
        'type':'date',
        'filter_on':1
      },
      {
        'description':'Сумма',
        'name':'summa',
        'filter_type':'range',
        'type':'text',
        'filter_on':1
      },
      {
        'description':'Истец',
        'name':'pl',
        'type':'text',
        'not_process':1,
        'filter_on':1
      },
      {
        'description':'Ответчик',
        'name':'resp',
        'type':'text',
        'not_process':1,
        'filter_on':1
      },
  ]