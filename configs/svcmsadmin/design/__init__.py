form = {
  'work_table': 'design',
  'work_table_id': 'id',
  'title': 'Дизайны',
  'make_delete': 0,
  'default_find_filter': 'header',
  'read_only': 1,
  'tree_use': 0,
  'fields': [
    {
      'description': 'Наименование шаблона',
      'name': 'header',
      'type': 'text',
      'regexp_rules': ['^.+$'],
      'filter_on': True,
    },
    {
      'description': 'Ссылка на дизайн',
      'name': 'url_design',
      'type': 'text',
    },
    {
      'description': 'Ссылка на UI',
      'name': 'url_ui',
      'type': 'text',
    },
    {
      'description': 'Изображения',
      'name': 'design_img',
      'type': '1_to_m',
      'table': 'design_img',
      'table_id': 'id',
      'foreign_key': 'design_id',
      'sort': 1,
      'fields': [
        {
          'description': 'Название страницы',
          'name': 'header',
          'type': 'text',
        },
        {
          'description': 'изображение',
          'name': 'attach',
          'type': 'file',
          'filedir': './design',
        },
      ],
    },
  ],
}
