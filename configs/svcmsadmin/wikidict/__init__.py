form={
  'work_table':'wikidict',
  'work_table_id':'id',
  'title':'Wiki словарь',
  'make_delete':1,
  'read_only':0,
  'tree_use':0,
  'default_find_filter':'header',
  'header_field':'header',
  'add_where':'parent_id is null',
  'fields':[
    {
      'description':'Основное слово',
      'type':'text',
      'name':'header',
      'regexp_rules':['^.+$','Заполните основное слово'],
      'filter_on':True,
    },
    {
      'description':'Правила бота',
      'type':'1_to_m',
      'name':'keywords',
      'table':'wikidict',
      'table_id':'id',
      'foreign_key':'parent_id',
      'fields':[
        {
          'description':'Словоформа',
          'type':'text',
          'name':'header',
        },
        {
          'description':'неправильное слово',
          'type':'checkbox',
          'name':'wrong',
        },
      ],
    },
  ],
}
