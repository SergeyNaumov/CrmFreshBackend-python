from .fields import get_fields
form={
    'work_table':'manager_menu',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Меню системы',
    'sort':True,
    'tree_use':True,
    'max_level':2,
    'explain':False,
    'read_only':1,
    'fields': get_fields()
    
}
      

