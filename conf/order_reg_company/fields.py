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
      'name':'firm',
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
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },
    {
      'description':'Имя',
      'type':'text',
      'name':'name',
      'filter_on':1
    }

]
