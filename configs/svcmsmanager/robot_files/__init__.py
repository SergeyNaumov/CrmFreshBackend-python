def filter_code_body(form,field,row):
  return f"<pre><small>{row['wt__body']}</small></pre>"

#from .fields import get_fields
form={
    'work_table':'files',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Файлы для поисковиков',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'',
    #'explain':1,
    'fields': [ 
        {
            'description':'url',
            'type':'text',
            'name':'url',
            'filter_on':True
        },
        {
          'description':'Содержимое файла',
          'name':'body',
          'type':'textarea',
          'filter_code': filter_code_body,
          'filter_on':True
        },
        {
          'description':'MIME-Type',
          'name':'type',
          'type':'text',
          'filter_on':True
        },

  ]  
    
}
      


