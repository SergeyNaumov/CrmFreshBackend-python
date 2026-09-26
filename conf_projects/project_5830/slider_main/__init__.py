#from .fields import get_fields
form={
    'work_table':'struct_5830_slider_main',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Слайдер для главной',
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
            'filedir':'./files/project_5830/slider_main',
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
            'description':'Ссылка с кнопки',
            'type':'text',
            'name':'button_url',
        },
        {
            'description':'Текст кнопки',
            'type':'text',
            'name':'button_text',
        },



    ]
}



