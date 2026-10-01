form={
  'work_table':'fast_rule',
  'work_table_id':'fast_rule_id',
  'title':'Быстрые правила',
  'make_delete':1,
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'Тип быстрого правила',
      'type':'select_values',
      'name':'rtype',
      'values':[
        {'v':'url','d':'Для url'},
        {'v':'code','d':'Блоки в шаблоне'},
      ],
      'filter_on':True,
    },
    {
      'description':'Заголовок',
      'type':'text',
      'name':'header',
      'filter_on':True,
    },
    {
      'description':'url_regexp',
      'type':'text',
      'name':'url_regexp',
      'filter_on':True,
    },
    {
      'description':'Код',
      'type':'codelist',
      'name':'run_code',
    },
    {
      'description':'Админ',
      'type':'text',
      'name':'admin_id',
      'hide':True,
    },
  ],
}
