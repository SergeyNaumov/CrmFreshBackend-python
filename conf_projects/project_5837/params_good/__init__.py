# Раздел «Характеристики товаров → Значения по товарам».
# ds_params_good: значение параметра для конкретного товара.
# Порядок вывода в карточке задаётся в «Параметры рубрик».
form={
    'work_table':'ds_params_good',
    'work_table_id':'param_id,good_id',
    'title':'Значения характеристик',
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
            'description':'Товар',
            'name':'good_id',
            'type':'select_from_table',
            'table':'ds_good',
            'header_field':'header',
            'value_field':'id',
            'filter_on':1,
        },
        {
            'description':'Значение',
            'name':'value',
            'type':'text',
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
