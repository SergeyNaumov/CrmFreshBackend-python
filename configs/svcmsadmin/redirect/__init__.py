form={
  'work_table':'redirect',
  'work_table_id':'id',
  'title':'Домен',
  'make_delete':1,
  'default_find_filter':'domain_f,domain_t',
  'fields':[
    {
      'description':'Откуда',
      'type':'text',
      'name':'domain_f',
      'regexp_rules':[
        '/^[a-z0-9\\-\\.\\_\\?\\=\\/\\:]+$/','Недопустимые символы в поле «Откуда»',
      ],
      'filter_on':True,
    },
    {
      'description':'Протокол откуда',
      'type':'select_values',
      'name':'protocol_f',
      'regexp_rules':[
        '/^[12]$/','Протокол должен быть выбран',
      ],
      'values':[
        {'v':1,'d':'http'},
        {'v':2,'d':'https'},
      ],
    },
    {
      'description':'Куда',
      'type':'text',
      'name':'domain_t',
      'regexp_rules':[
        '/^[a-z0-9\\-\\.\\_\\?\\=\\/\\:]+$/','Недопустимые символы в поле «Куда»',
      ],
      'filter_on':True,
    },
    {
      'description':'Протокол куда',
      'type':'select_values',
      'name':'protocol_t',
      'regexp_rules':[
        '/^[12]$/','Протокол должен быть выбран',
      ],
      'values':[
        {'v':1,'d':'http'},
        {'v':2,'d':'https'},
      ],
    },
  ],
}
