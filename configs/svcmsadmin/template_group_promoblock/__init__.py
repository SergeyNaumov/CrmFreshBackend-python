form={
  'work_table':'template_group_promoblock',
  'work_table_id':'id',
  'title':'Промоблоки для типовых сайтов',
  'make_delete':0,
  'read_only':1,
  'default_find_filter':'header',
  'header_field':'header',
  'fields':[
    {
      'description':'Название',
      'type':'text',
      'name':'header',
      'regexp_rules':[
        '/^.+$/','Поле обязательно для заполнения',
      ],
      'filter_on':True,
    },
    {
      'description':'Отрасль',
      'type':'select_from_table',
      'name':'otr_id',
      'table':'otr',
      'header_field':'header',
      'value_field':'id',
      'regexp_rules':[
        '/^\\d+$/','Отрасль должна быть выбрана',
      ],
    },
    {
      'description':'Ширина, px',
      'type':'text',
      'name':'width',
      'read_only':True,
    },
    {
      'description':'Высота, px',
      'type':'text',
      'name':'height',
      'read_only':True,
    },
    {
      'description':'Файл с промоблоком',
      'type':'file',
      'name':'file',
      'filedir':'../files/typesites/promoblock',
    },
  ],
}
