form = {
  'work_table': 'bot_rules',
  'work_table_id': 'id',
  'title': 'Правила бота',
  'make_delete': 1,
  'default_find_filter': 'header',
  'read_only': 0,
  'tree_use': 0,
  'fields': [
    {
      'description': 'Команда',
      'type': 'text',
      'name': 'command',
      'filter_on': True,
    },
    {
      'description': 'Сообщение',
      'type': 'textarea',
      'name': 'message',
    },
    {
      'description': 'Кнопки для веб-приложения',
      'name': 'buttons',
      'type': '1_to_m',
      'table': 'bot_rules_webapp',
      'table_id': 'id',
      'foreign_key': 'rule_id',
      'sort': 1,
      'fields': [
        {
          'description': 'Название кнопки',
          'type': 'text',
          'name': 'header',
        },
        {
          'description': 'url',
          'type': 'text',
          'name': 'url',
        },
      ],
    },
  ],
}
