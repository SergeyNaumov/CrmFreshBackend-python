
def enabled_before_code(form,field):
    if form.action=='new':
        field['value']=1

form={
    'title':'Товары',
    'work_table':'struct_[project_id]_good',
    'work_table_id':'id',
    
    'sort':0,
    'tree_use':0,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':False,
    'fields': [ 
        {
            'description':'Наименование товара',
            'type':'text',
            'name':'header',
            'tab':'main',
        },
        {
            'description':'Краткое описание',
            'type':'textarea',
            'name':'anons',
            'tab':'main',
        },

        {
            'description':'Рубрика',
            'type':'select_from_table',
            'name':'rubricator_id',
            'table':'', # задаётся в events
            'header_field':'header',
            'value_field':'id',
            'order':'sort'
        },
        {
            'description':'Артикул',
            'type':'text',
            'name':'artikul',
            'tab':'main',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'before_code':enabled_before_code
        },
        {
            'description':'В наличии',
            'name':'in_stock',
            'type':'checkbox',
            'before_code':enabled_before_code
        },
        {
            'description':'Старая цена',
            'type':'text',
            'name':'old_price',
            'make_change_in_search':True,
            'regexp_rules':[
                '^[0-9]+(\.[0-9]{1,2})?$', 'укажите корректную цену'
            ],
            'replace_rules':[
                '/^\./','0.',
                '/,/','.',
                '/[^0-9\.]+/','',
            ]
        },
        {
            'description':'Новая цена',
            'type':'text',
            'name':'price',
            'make_change_in_search':True,
            'regexp_rules':[
                '/^[0-9]+(\.[0-9]{1,2})?$/', 'укажите корректную цену'
            ],
            'replace_rules':[
                '/^\./','0.',
                '/,/','.',
                '/[^0-9\.]+/','',
            ]
        },
        {
            'description':'Фото товара',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_[project_id]/good', # заполняем в events
            'preview':'156x117',
            'resize':[
                { # список товаров
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'156x117',
                    'quality':'100'
                },
                # в карте товара
                { 'file':'<%filename_without_ext%>_mini2.<%ext%>', 'size':'355x215', 'quality':'100'}
            ],
            'tab':'main'
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'body',
            'plugins':[
                {'type':'GPTAssist', 'set_value_button':'Отправить в описание'}
            ]
        }
  ]  
    
}
      


