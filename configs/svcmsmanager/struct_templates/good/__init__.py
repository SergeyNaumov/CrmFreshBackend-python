# Эталон уникальной структуры "Товары".
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
    {'description':'Наименование','type':'text','name':'header','filter_on':True},
    {'description':'Артикул','type':'text','name':'artikul','filter_on':True},
    {'description':'Цена','type':'text','name':'price'},
    {'description':'Цена 2','type':'text','name':'price2'},
    {'description':'Анонс','type':'textarea','name':'anons'},
    {'description':'Описание','type':'wysiwyg','name':'body'},
    {'description':'Фото','type':'file','name':'photo'},
    {'description':'Рубрика (id)','type':'text','name':'rubricator_id'},
    {'description':'Вкл','type':'checkbox','name':'enabled','value':1,'filter_on':True},
    {'description':'Спецпредложение','type':'checkbox','name':'specpredl'},
  ],
}
