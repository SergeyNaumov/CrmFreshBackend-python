#from .fields import get_fields
form={
    'work_table':'struct_5794_document',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Документы',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5794_document','a':'wt'},
        {'t':'struct_5794_service','a':'s','l':'wt.service_id=s.id','lj':1},
    ],
    'fields':[
        {
            'description':'Название документа',
            'type':'text',
            'name':'header',
            'filter_on':1,
            'make_change_in_search':True,
        },
        {
            'description':'Услуга',
            'type':'select_from_table',
            'name':'service_id',
            'table':'struct_5794_service',
            'tablename':'s',
            'header_field':'header',
            'value_field':'id',
            'filter_on':1,
            'make_change_in_search':True,
        },
        {
            'description':'Дата',
            'type':'date',
            'name':'registered',
            'make_change_in_search':True,
            'filter_on':1
        },
        {
            'description':'Фото',
            'type':'file',
            'name':'photo',
            'filedir':'./files/project_5794/document',
            'preview':'214x293',
            'resize':[
                { # вертикальное фото
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'214x293',
                    'quality':'100'
                },
                { # горизонтальное фото
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'295x202',
                    'quality':'100'
                },
                { # лайтбокс
                    'file':'<%filename_without_ext%>_mini3.<%ext%>',
                    'size':'0x700',
                    'quality':'100'
                },
                { # вкладка "документы"
                    'file':'<%filename_without_ext%>_mini4.<%ext%>',
                    'size':'0x700',
                    'quality':'100'
                },
            ],
        },
        {
            'description':'Тип вывода фото в списке',
            'name':'type',
            'type':'select_values',
            'values':[
                {'v':1,'d':'вертикальное'},
                {'v':2,'d':'горизонтальное'},
            ]
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'filter_on':1,
            'make_change_in_search':True
        },


    ]
}
      


