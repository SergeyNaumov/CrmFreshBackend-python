#from .fields import get_fields
form={
    'work_table':'struct_5794_video',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Видео',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    #'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Название',
            'type':'textarea',
            'name':'header',
        },

        {
            'description':'Фотозаглушка (368x253)',
            'type':'file',
            'filedir':'./files/project_[project_id]/video',
            'preview':'368x253',
            'resize':[
                { # 1-3 фото в списке услуг на главной странице и странице списка услуг
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'368x253',
                    'quality':'100'
                },
            ],
            'name':'photo',
        },
        {
            'description':'url видео на youtube',
            'type':'text',
            'name':'url',
        },
        {
            'description':'описание',
            'type':'text',
            'name':'body'
        },
    ]
}
      


