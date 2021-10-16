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
        'description':'Код видео',
        'type':'textarea',
        'name':'code',
      },
      
]