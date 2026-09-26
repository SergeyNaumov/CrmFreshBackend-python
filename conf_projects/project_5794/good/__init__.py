#from .fields import get_fields
form={
    'work_table':'struct_5794_good',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Товары',
    #'sort':1,
    'tree_use':False,
    'header_field':'header',
    #'max_level':2,
    'default_find_filter':'header',
    #'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'cols':[
        [
            {'description': 'SEO','name':'promo','hide':True},
            {'description': 'Данные о товаре','name':'main','hide':False},

        ],
    ],
    'QUERY_SEARCH_TABLES':[
        {'t':'struct_5794_good','a':'wt'},
        {'t':'struct_5794_rubricator','a':'r','l':'wt.rubricator_id=r.id','left_join':1},
    ],
    'javascript':{
      #'edit_form':'',
      'edit_form_static':[
        '/CrmFresh/trade/users_card/edit_form.js?nocache=20240313.1'
      ]
    },
    'fields':[
        # seo
        {'description':'title','type':'text','name':'promo_title','tab':'promo'},
        {'description':'description','type':'textarea','name':'promo_description','tab':'promo'},
        {'description':'keywords','type':'textarea','name':'promo_keywords','tab':'promo'},
        {'description':'promo текст','type':'textarea','name':'promo_body','tab':'promo'},
        # данные о товаре
        {
            'description':'Название',
            'type':'text',
            'name':'header',
        },
        {
            'description':'url',
            'type':'text',
            'name':'url',
            'regexp_rules':[
                r'/^\/good\/.+$/', 'url должен быть в формате: /good/[ключевое-слово]'
            ]
        },
        {
            'description':'Рубрика каталога',
            'type':'select_from_table',
            'table':'struct_5794_rubricator',
            'name':'rubricator_id',
            'header_field':'header',
            'value_field':'id',
            'order':'sort',
            'tablename':'r',
            'tree_use':1
        },
        {
            'description':'Артикул',
            'name':'artikul',
            'type':'text'
        },
        {
            'description':'Цена',
            'name':'price',
            'type':'text',
            'replace_rules':[
                r'/[^\d]/g',''
            ],
            'make_change_in_search':True
        },
        {
            'description':'Наличие',
            'name':'nal',
            'type':'checkbox'
        },
        {
            'description':'Фото',
            'type':'file',
            'filedir':'./files/project_5794/good',
            'name':'photo',
            'preview':'260x185',
            'resize':[
                { # для блока "популярные товары"

                    'description':'для блока "популярные товары"',
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'260x185',
                    'quality':'100'
                },
                { # для списка товаров
                    'description':'для списка товаров',
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'283x187',
                    'quality':'100'
                },
                { # для карточки товара
                    'description':'для карточки товара',
                    'file':'<%filename_without_ext%>_mini3.<%ext%>',
                    'size':'470x367',
                    'quality':'100'
                },
                { # лайтбокс
                    'description':'лайтбокс',
                    'file':'<%filename_without_ext%>_mini4.<%ext%>',
                    'size':'800x0',
                    'quality':'100'
                },
            ],
        },
        {
            'description':'Сортировка',
            'name':'sort',
            'type':'text',
            'make_change_in_search':True,
            'replace_rules':[
                r'/[^\d]/g',''
            ]
        },
        {
            'description':'Популярный товар',
            'name':'popular',
            'type':'checkbox'
        },
        {
            'description':'Вкл',
            'name':'enabled',
            'type':'checkbox'
        },
        {
            'description':'Характеристики (название вкладки)',
            'type':'text',
            'name':'tech_header'
        },
        {
            'description':'Характеристики (содержимое)',
            'type':'wysiwyg',
            'name':'tech',
            'edit_mode':1,
        },

        {
            'description':'описание',
            'type':'wysiwyg',
            'name':'body',
            'edit_mode':1
        },
    ]
}
      


for f in form['fields']:
    if not f.get('tab'):
        f['tab']='main'