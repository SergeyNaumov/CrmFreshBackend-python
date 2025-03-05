def before_code_type(form,field):
  #print('form:',form)
  #print('field:',field)
  if not 'value' in field or not field['value']:
    field['value']='vue'


fields=[ 
    {
        'description':'Название видео',
        'type':'text',
        'name':'header',
    },
    {
        'description':'Конференция',
        'name':'conference_id',
        'type':'select_from_table',
        'table':'conference',
        'header_field':'header',
        'value_field':'id'
    },
    {
        'description':'Код видео',
        'type':'textarea',
        'name':'code',
    },
      
]