

#from lib.anna.get_apt_list import get_apt_list

def get_fields():
    return [ 
    {
      'name':'registered',
      'description':'Дата создания',
      'type':'date',
      'read_only':1,
      'filter_on':1
    },
    # {
    #   'name':'header',
    #   'description':'Наименование',
    #   'type':'text',
    #   'filter_on':1
    # }, 
    {
      'name':'inn',
      'description':'ИНН',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'ur_address',
      'description':'Юридический адрес',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },
    {
      'description':'Представитель аптеки',
      'name':'manager_id',
      'type':'select_from_table',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',
      'where':'type=3'
    },
    {
      'description':'Менеджер компании Анна',
      'name':'anna_manager_id',
      'type':'select_from_table',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',
      'where':'type=1'
    }

]

