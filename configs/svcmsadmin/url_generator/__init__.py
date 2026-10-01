form={
  'work_table':'url_generator',
  'work_table_id':'id',
  'title':'Генерация URL',
  'make_delete':1,
  'default_find_filter':'project_id',
  'read_only':0,
  'tree_use':0,
  'fields':[
    {
      'description':'Проект',
      'type':'select_from_table',
      'name':'project_id',
      'table':'project',
      'header_field':'header',
      'value_field':'project_id',
      'filter_on':True,
    },
    {
      'description':'Сервис',
      'type':'select_from_table',
      'name':'struct_id',
      'table':'struct',
      'header_field':'header',
      'value_field':'struct_id',
    },
    {
      'description':'Входной URL',
      'type':'text',
      'name':'in_url',
    },
    {
      'description':'База для выходного URL',
      'type':'text',
      'name':'base',
    },
    {
      'description':'Поле "Заголовок"',
      'type':'text',
      'name':'header_field',
    },
    {
      'description':'Поле "Значение"',
      'type':'text',
      'name':'id_field',
    },
    {
      'description':'Опции(неиспользуется пока что)',
      'type':'textarea',
      'name':'options',
    },
    {
      'description':'Вкл',
      'type':'checkbox',
      'name':'enabled',
      'value':1,
    },
  ],
}
