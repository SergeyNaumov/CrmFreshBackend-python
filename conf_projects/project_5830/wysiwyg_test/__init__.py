form={
    'work_table':'struct_5830_wysiwyg_test',
    'work_table_id':'id',
    'title':'Тест двух визивигов',
    'tree_use':False,
    'header_field':'header',
    'default_find_filter':'header',
    'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Название',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Визивиг 1',
            'type':'wysiwyg',
            'name':'body',
        },
        {
            'description':'Визивиг 2',
            'type':'wysiwyg',
            'name':'body2',
        },
    ]
}
