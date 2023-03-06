#from .fields import get_fields
form={
    'work_table':'struct_5759_case',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы',
    
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
        # {
        #     'description':'Сфера деятельности',
        #     'type':'text',
        #     'name':'opportunity',
        # },
        # {
        #     'description':'Вид кейса',
        #     'name':'type',
        #     'type':'select_from_table',
        #     'table':'struct_5759_case_type',
        #     'header_field':'header',
        #     'value_field':'value'
        # },
        # # SEO
        # {
        #     'description':'Фото кейса ПК',
        #     'type':'file',
        #     'filedir':'./files/project_5759/case',
        #     'name':'photo_for_pk',
        # },
        # # Фото кейса мобильная (без ресайза)
        # {
        #     'description':'текстовый блок над контентом', # SEO, Айдентика, Создание сайта
        #     'type':'wysiwyg',
        #     'name':'block_about_content'
        # },
        # { # Создание сайта, РК, SMM
        #     'description':'Адрес сайта',
        #     'type':'text',
        #     'name':'url',
        # },
        # {
        #     'description':'Фото ПК',
        #     'type':'file',
        #     'name':'photo1',
        #     'filedir':'./files/project_5759/case/photo_pk',
        #     'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        # },

# """
#         # Создание сайта:
#   ]           
            
#             - фото ПК – ресайз 1129х0
#             - фото смартфон – ресайз332х0
#             - фотогалерея – ресайз для списка 295Х0, для лайтбокса 1000Х0 (фото внутренних страниц в карусели)
#             - текстовый блок  wysiwyg под контентом

        
#         # Айдентика
            
#             - заголовок – textarea 
#             - фото  - ресайз 388х183, 1000Х0 для лайтбокса


#         Если выбрано #рекламная кампания появляются поля верстка 7_keisy_in_3.html
#         - отрасль – text 
#         - логотип – file  ресайз 0х129px
#         - название компании
#         - адрес сайта 
#         - задачи - wysiwyg
#         - решение - wysiwyg
#         - результаты - wysiwyg
#         - резюме - wysiwyg
#         - контекст - wysiwyg

#         Если выбрано #smm появляются поля. верстка 7_keisy_in_3.html

#         - отрасль – text 
#         - логотип – file   ресайз 0х135px
#         - название компании
#         - адрес сайта 
#         - анонс -  wysiwyg
#         - задачи - wysiwyg
#         - платформы - wysiwyg
#         - задачи - wysiwyg
#         - результаты - wysiwyg
# """
    ]
}
      


