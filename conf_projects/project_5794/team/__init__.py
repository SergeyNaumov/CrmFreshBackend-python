#from .fields import get_fields
form={
    'work_table':'struct_5794_team',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Наша команда',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Фамилия',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Имя и Отчество',
            'type':'text',
            'name':'name',
        },
        {
            'description':'Должность',
            'type':'text',
            'name':'position',
        },
        {
            'description':'Отдел',
            'name':'department',
            'type':'text'
        },
        {
            'description':'Фото',
            'type':'file',
            'filedir':'./files/project_[project_id]/team',
            'name':'photo',
            'preview':'138x138',
            'resize':[
                {   # Главная
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'138x138',
                    'quality':'100'
                },
                {   # страница "Наша команда"
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'296x316',
                    'quality':'100'
                },
                {   # Наша команда
                    'file':'<%filename_without_ext%>_mini3.<%ext%>',
                    'size':'353x571',
                    'quality':'100'
                },
            ],
        },
        {
            'description':'Телефоны',
            'name':'phones',
            'type':'textarea'
        },
        {
            'description':'Email`ы',
            'name':'emails',
            'type':'textarea'
        },
        {
            'description':'Вкл',
            'name':'enabled',
            'type':'checkbox'
        },
        {
            'description':'Образование',
            'name':'education',
            'type':'wysiwyg',
            'edit_mode':1,
        },
        {
            'description':'О себе',
            'name':'body',
            'type':'wysiwyg',
            'edit_mode':1,
        },
    ]
}
      


