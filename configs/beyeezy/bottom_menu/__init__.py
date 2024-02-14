def before_code_type(form,field):
  #print('form:',form)
  #print('field:',field)
  if not 'value' in field or not field['value']:
    field['value']='vue'

form={
    'work_table':'bottom_menu',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Нижнее меню',
    'sort':True,
    'tree_use':True,
    'max_level':2,
    'explain':False,
    'fields': [ 
        {
            'description':'Наименование пункта',
            'type':'text',
            'name':'header',
            
        },
        {
            'description':'url',
            'type':'text',
            'name':'url',
            
        },


  ]  
    
}
      

