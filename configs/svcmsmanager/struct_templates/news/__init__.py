# Эталон уникальной структуры "Новости".
# При создании структуры подставляются: [%project_id%], [%table_name%], [%table_id%], [%header%].
form={
  'work_table':'[%table_name%]',
  'work_table_id':'[%table_id%]',
  'title':'[%header%]',
  'header_field':'header',
  'default_find_filter':'header',
  'make_delete':1,
  'read_only':0,
  'tree_use':0,
  'fields':[
    {'description':'Заголовок','type':'text','name':'header','filter_on':True},
    {'description':'Анонс','type':'textarea','name':'anons'},
    {'description':'Текст','type':'wysiwyg','name':'body'},
    {'description':'Фото','type':'file','name':'photo'},
    {'description':'Вкл','type':'checkbox','name':'enabled','value':1,'filter_on':True},
    {'description':'Дата','type':'date','name':'registered','filter_on':True},
  ],
}
