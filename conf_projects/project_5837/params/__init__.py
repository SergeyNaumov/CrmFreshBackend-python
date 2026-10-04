# Раздел «Характеристики товаров → Справочник параметров».
# Таблица ds_params: название параметра и тип (1 — число, 2 — текст).
# Числовые параметры (type=1) доступны для фильтров в каталоге.
form={
    'work_table':'ds_params',
    'work_table_id':'id',
    'work_table_foreign_key':'project_id',
    'title':'Параметры товаров',
    'sort':True,
    'tree_use':False,
    'explain':True,
    'header_field':'header',
    'default_find_filter':'header',
    'search_on_load':True,
    'fields':[
        {
            'description':'Название параметра',
            'name':'header',
            'type':'text',
            'filter_on':1,
        },
        {
            'description':'Тип',
            'name':'type',
            'type':'select_values',
            'values':[
                {'v':1,'d':'число (доступен в фильтрах)'},
                {'v':2,'d':'текст'},
            ],
            'filter_on':1,
            'default':2,
        },
    ]
}
