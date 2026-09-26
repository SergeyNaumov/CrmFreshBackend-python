#from .fields import get_fields
form={
    'work_table':'struct_5759_interest',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Блок "вас может заинтересовать"',
    'sort':1,
    'explain':0,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Иконка svg (не обязательно)',
            'name':'icon',
            'type':'file',
            'filedir':'./files/project_5759/interest',

        },
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Название таба',
            'type':'text',
            'name':'tabname',
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'body',
            'edit_mode':True
        },
  ]  
    
}
      


