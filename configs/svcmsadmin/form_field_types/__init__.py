form={
  'work_table':'form_field_types',
  'work_table_id':'id',
  'title':'Типы полей',
  'make_delete':1,
  'read_only':0,
  'tree_use':0,
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'Название',
      'type':'text',
      'name':'header',
      'filter_on':True,
    },
    {
      'description':'Правило для проверки',
      'type':'text',
      'name':'regexp_code',
      'add_description':'Если поле обязательное',
      'filter_on':False,
    },
    {
      'description':'HTML код',
      'type':'textarea',
      'name':'html',
      'add_description':'Используется для генерации поля',
      'filter_on':False,
    },
  ],
}
