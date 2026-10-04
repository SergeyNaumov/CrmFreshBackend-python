# Раздел «Характеристики товаров → Параметры рубрик».
# ds_params_catalog: какие параметры показывать у рубрики каталога.
# Наследование: рубрика показывает свои параметры + параметры родителей
# (см. lib/dsengine/params.py — цепочка rubricator_id).
form={
    'work_table':'ds_params_catalog',
    'work_table_id':'param_id,catalog_id',
    'title':'Параметры рубрик',
    'sort':False,
    'tree_use':False,
    'explain':True,
    'header_field':'',
    'search_on_load':True,
    'fields':[
        {
            'description':'Параметр',
            'name':'param_id',
            'type':'select_from_table',
            'table':'ds_params',
            'header_field':'header',
            'value_field':'id',
            'filter_on':1,
        },
        {
            'description':'Рубрика каталога',
            'name':'catalog_id',
            'type':'select_from_table',
            'table':'ds_catalog',
            'header_field':'header',
            'value_field':'id',
            'tree_use':1,
            'filter_on':1,
        },
        {
            'description':'Порядок',
            'name':'sort',
            'type':'text',
            'default':0,
        },
    ]
}
