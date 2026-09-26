#from .fields import get_fields
form={
    'work_table':'struct_5794_partner',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Наши партнёры',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Название партнёра',
            'type':'text',
            'name':'header',
        },

        {
            'description':'Лого',

            'type':'file',
            'filedir':'./files/project_[project_id]/partner',
            'name':'photo',

        },


    ]
}
      


