form={
  'work_table':'top_menu',
  'work_table_id':'top_menu_id',
  'title':'Верхнее меню',
  'make_delete':0,
  'read_only':1,
  'tree_use':True,
  'sort':True,
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'наименование',
      'type':'text',
      'name':'header',
      'regexp_rules':[
        '/^.+$/','Поле обязательно для заполнения',
      ],
      'filter_on':True,
    },
    {
      'description':'/url',
      'type':'text',
      'name':'url',
      'regexp_rules':[
        '/^.+$/','Поле обязательно для заполнения',
      ],
    },
    {
      'description':'Проект',
      'type':'select_from_table',
      'name':'project_id',
      'table':'project',
      'header_field':'header',
      'value_field':'project_id',
      'order':'header',
      'regexp_rules':[
        '/^[0-9]+$/','Проект должен быть выбран',
      ],
      'filter_on':True,
    },
    {
      'description':'Вкл',
      'type':'checkbox',
      'name':'enabled',
    },
  ],
}
