#from .fields import get_fields
form={
    'work_table':'struct_5830_action',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Акции',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Название акции / товара',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Цена',
            'type':'text',
            'name':'price',
            'regexp_rules':[
                '^[0-9]*$', 'укажите корректную цену'
            ],
        },
        {
            'description':'Фото для главной',
            'type':'file',
            'filedir':'./files/project_5830/action_main',
            'name':'photo',
        },
        {
            'description':'Фото для спецпредложений',
            'type':'file',
            'filedir':'./files/project_5830/action_spec',
            'name':'photo_action',
        },
        {
            'description':'Ссылка с кнопки',
            'type':'text',
            'name':'url',
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



