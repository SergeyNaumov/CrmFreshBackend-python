#from .fields import get_fields
form={
    'work_table':'struct_5794_ed',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Единицы изменения',
    #'sort':1,
    #'tree_use':False,
    'header_field':'header',

    'default_find_filter':'header',
    'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Название',
            'type':'textarea',
            'name':'header',
        },
    ]
}
      


