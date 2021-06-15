def get_fields():
    return [ 
    {
      'name':'registered',
      'description':'Дата и время заявки',
      'type':'datetime',
      'read_only':1,
      'filter_on':1
    },

    # {
    #   'name':'firm',
    #   'description':'Логин',
    #   'type':'text',
    #   'filter_on':1
    # }, 
    {
      'name':'phone',
      'description':'Телефон',
      'type':'text',
      'filter_on':1
    }, 
    {
      'name':'name_f',
      'description':'Фамилия',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'name_i',
      'description':'Имя',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'name_o',
      'description':'Отчество',
      'type':'text',
      'filter_on':1
    },

]
