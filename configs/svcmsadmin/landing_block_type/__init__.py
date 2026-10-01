form={
  'work_table':'landing_block_type',
  'work_table_id':'id',
  'title':'Блоки для LP',
  'make_delete':1,
  'read_only':0,
  'sort':True,
  'sort_field':'sort',
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'Название блока',
      'type':'text',
      'name':'header',
      'regexp_rules':['^.+$','Заполните название блока'],
      'filter_on':True,
    },
    {
      'description':'Уникальное обозначение блока',
      'type':'text',
      'name':'name',
      'regexp_rules':['^.+$','Заполните уникальное обозначение'],
      'filter_on':True,
    },
  ],
}
