#from .fields import get_fields
form={
    'work_table':'struct_5830_text_page',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Статичные текстовые страницы',
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
        },
        {
            'description':'url',
            'type':'text',
            'name':'url',
        },
        {
            'description':'Без промо',
            'name':'without_promo',
            'type':'checkbox'
        },
        {

            'description':'Промо изображение',
            'type':'file',
            'filedir':'./files/project_5830/text_page_banner',
            'name':'photo_promo',
        },
        {
            'description':'Текст promo',
            'type':'wysiwyg',
            'name':'promo_body',
            'style':['https://armit-new.design-b2b.com/templates/2026/arm-it/assets/fonts/font-awesome/font-awesome.min.css']
        },
        {
            'description':'Содержимое',
            'type':'wysiwyg',
            'style':['https://armit-new.design-b2b.com/templates/2026/arm-it/assets/fonts/font-awesome/font-awesome.min.css'],
            'name':'body',
        },




    ]
}
      


