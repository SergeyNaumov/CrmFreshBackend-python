form={
  'work_table':'struct_public',
  'work_table_id':'struct_public_id',
  'title':'Стандартные инструменты',
  'make_delete':1,
  'read_only':0,
  'tree_use':0,
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'Название инструмента',
      'type':'text',
      'name':'header',
      'regexp_rules':['^.+$','Заполните название инструмента'],
      'filter_on':True,
    },
    {
      'description':'ссылка на инструмент',
      'type':'textarea',
      'name':'link',
    },
    {
      'description':'json для vue CRM',
      'type':'textarea',
      'name':'json',
    },
  ],
}
