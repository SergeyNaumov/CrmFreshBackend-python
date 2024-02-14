from lib.core import cur_date
def today_filter(form,field):
  if form.script=='admin_table':
    field['value']=[cur_date(),'']

fields=[
    {
      'description':'Время парсинга',
      'type':'date',
      'name':'registered',
      'filter_on':1,
      'before_code': today_filter
    },
    {
      'description':'Дата регистрации',
      'name':'regdate',
      'type':'text',
      'filter_on':1,

    },
    {
      'description':'ИНН',
      'name':'inn',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'КПП',
      'name':'kpp',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Организация',
      'name':'shortname',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'ФИО директора',
      'name':'fio',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Адрес',
      'name':'address',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'ОКТМО',
      'name':'oktmo',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'ОКАТО',
      'name':'okato',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'ОКПО',
      'name':'okpo',
      'type':'text',
      'filter_on':1
    },
]