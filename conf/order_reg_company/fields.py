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
      'regexp_rules':[
          '/^(\+7 \(\d{3}\) \d{3}-\d{2}-\d{2})?$/','Если указывается телефон, он должен быть в формате +7 (XXX) XXX-XX-XX',
      ],
      'replace_rules':[
          '/[^\d]/g','',
          '/^(\d{11}).*$/','$1',
          '/^[87]/','+7',
          '/^\+7(\d{3})(\d)/','+7 ($1) $2',
          '/^(\+7 \(\d{3}\))(\d{3})/','$1 $2',
          '/(\d{3})(\d{2})/',"$1-$2",
          '/-(\d{2})(\d{2}\d*)$/',"-$1-$2"

      ],
      'filter_on':1
    },
    {
      'description':'Имя',
      'type':'text',
      'name':'name',
      'filter_on':1
    }

]
