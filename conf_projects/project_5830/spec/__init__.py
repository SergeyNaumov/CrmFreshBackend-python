#from .fields import get_fields
form={
    'work_table':'struct_5830_spec',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Спецпредложения',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Фото',
            'type':'file',
            'filedir':'./files/project_5830/spec',
            'name':'photo',
        },
        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Подзаголовок',
            'type':'text',
            'name':'subheader',
        },
        {
            'description':'TOP',
            'type':'checkbox',
            'name':'top',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
        },
    ]
}



