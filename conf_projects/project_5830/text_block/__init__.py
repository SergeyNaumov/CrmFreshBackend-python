#from .fields import get_fields
form={
    'work_table':'struct_5830_text_block',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Текстовые блоки',
    'sort':False,
    'tree_use':False,
    'header_field':'header',
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[

        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
            'filter_on':1
        },
        {
            'description':'Имя блока в шаблоне',
            'type':'text',
            'name':'name',
            'filter_on':1
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'name':'body',
            'filter_on':1
        },


    ]
}
      


