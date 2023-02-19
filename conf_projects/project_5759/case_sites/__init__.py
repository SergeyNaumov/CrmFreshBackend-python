#from .fields import get_fields
form={
    'work_table':'struct_5759_case_sites',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы "Создание сайтов"',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Название кейса',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Название компании',
            'type':'text',
            'name':'company',
        },
        {
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       'size':'340x264',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото кейса в миниатюра',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Фото кейса в миниатюра',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Услуга',
            'name':'service_id',
            'type':'select_from_table',
            'table':'struct_5759_service',
            'tree_use':1,
            'header_field':'header',
            'value_field':'value'
        },
        {
            'description':'Сфера деятельности',
            'type':'text',
            'name':'opportunity',
        },
        {
            'description':'Вид кейса',
            'name':'type',
            'type':'select_from_table',
            'table':'struct_5759_case_type',
            'header_field':'header',
            'value_field':'value'
        },
       
    ]
}
      


