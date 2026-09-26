#from .fields import get_fields
form={
    'work_table':'struct_5794_scheme_work',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Схема работы',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Название этапа',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Иконка',
            'type':'file',
            'filedir':'./files/project_[project_id]/scheme_work',
            'name':'icon',
        },


    ]
}
      


