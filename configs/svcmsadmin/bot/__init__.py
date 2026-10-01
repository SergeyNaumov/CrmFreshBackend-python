form = {
  'work_table': 'bot',
  'work_table_id': 'id',
  'title': 'Боты Telegram',
  'make_delete': 1,
  'default_find_filter': 'header',
  'read_only': 0,
  'tree_use': 0,
  'fields': [
    {
      'description': 'Проект',
      'name': 'project_id',
      'type': 'select_from_table',
      'table': 'project',
      'header_field': 'header',
      'value_field': 'project_id',
      'autocomplete': 1,
      'filter_on': True,
    },
    {
      'description': 'Название бота',
      'name': 'header',
      'type': 'text',
      'regexp_rules': ['^.+$'],
      'filter_on': True,
    },
    {
      'description': 'token',
      'name': 'token',
      'type': 'text',
    },
    {
      'description': 'Правила бота',
      'name': 'rules',
      'type': '1_to_m',
      'table': 'bot_rules',
      'table_id': 'id',
      'foreign_key': 'bot_id',
      'fields': [
        {
          'description': 'Команда',
          'type': 'text',
          'name': 'command',
        },
        {
          'description': 'Сообщение',
          'type': 'textarea',
          'name': 'message',
        },
      ],
    },
  ],
}
