#from .fields import get_fields
form={
    'work_table':'struct_5794_slider',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Слайдер',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Описание',
            'type':'text',
            'name':'body',
        },
        {
            'description':'Надпись на кнопке',
            'type':'text',
            'name':'button'
        },
        {
            'description':'url',
            'type':'text',
            'name':'url'
        },
        { # pic5
            'description':'Фото ПК (1980x505)',
            'type':'file',
            'filedir':'./files/project_5794/slider',
            'name':'photo'
        },
        # { # pic5_1
        #     'description':'Фото ПК подложка (987x505)',
        #     'type':'file',
        #     'filedir':'./files/project_[project_id]/slider',
        #     'name':'photo_bg'
        # },
        { #
            'description':'Фото, мобильные (359x259)',
            'type':'file',
            'filedir':'./files/project_[project_id]/slider',
            'name':'photo_mob'
        },

    ]
}
      


