def get_fields():
    return [ 
    {
      'name':'registered',
      'description':'Дата регистрации',
      'type':'date',
      'read_only':1,
      'filter_on':1
    },
    {
      'description':'Подтверждена',
      'name':'accepted',
      'type':'checkbox',
    },
    {
      'name':'header',
      'description':'Наименование организации',
      'type':'text',
      'filter_on':1
    }, 
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
      'name':'email_for_notify',
      'description':'Email для оповещений',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },

]
