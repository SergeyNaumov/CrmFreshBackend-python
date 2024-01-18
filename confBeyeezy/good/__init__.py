from .search_multi_action import search_multi_action_list
from .events import events
from .ajax import ajax
form={
    'work_table':'good',
    'work_table_id':'id',
    'title':'Товары',
    'sort':False,
    'tree_use':False,
    #'explain':1,
    'make_delete':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'good','a':'wt'},
        {'t':'category','a':'c','l':'c.id=wt.category_id','lj':1,},
        {'t':'color','a':'color','l':'color.id=wt.color_id','lj':1,'for_fields':['color_id']},
        {'t':'model','a':'model','l':'model.id=wt.model_id','lj':1,'for_fields':['model_id']},
        {'t':'season','a':'season','l':'season.id=wt.season_id','lj':1,'for_fields':['season_id']},
    ],
    'search_multi_action':search_multi_action_list, # множественное действие в поиске
    'GROUP_BY':'wt.id',
    'ajax':ajax,
    'fields': [ 
        {
            'description':'Название',
            'type':'text',
            'name':'header',
            'filter_on':True,
            'frontend':{'ajax':{'name':'gen_url','timeout':100}},

        },
        {
            'description':'url',
            'name':'keyword',
            'type':'text',
            'frontend':{'ajax':{'name':'url','timeout':100}},
        },
        {
            'description':'Категория',
            'type':'select_from_table',
            'table':'category',
            'name':'category_id',
            'tablename':'c',
            'header_field':'header',
            'value_field':'id',
            'frontend':{'ajax':{'name':'gen_url','timeout':100}},
            'filter_on':True
        },
        {
            'description':'Артикул',
            'type':'text',
            'name':'artikul',
            'filter_on':True
        },
        {
            'description':'Цена',
            'type':'text',
            'name':'price',
            'filter_on':True,
            'make_change_in_search':True
        },
        {
            'description':'Видео на youtube',
            'type':'text',
            'name':'youtube_link',
            'filter_on':True,
            'make_change_in_search':True
        },
        {
            'description':'Фотогалерея',
            'type':'1_to_m',
            'name':'photos',
            'table':'good_galery',
            'table_id':'id',
            'foreign_key':'good_id',
            'view_type':'list',
            'sort':1,
            'fields':[
                {
                    'description':'Фото',
                    'preview':1,
                    'type':'file',
                    'name':'photo',
                    'filedir':'./files/good_galery',
                    'preview':'300x300',
                    'resize':[
                        {
                            'description':'Для спика товаров',
                            'file':'<%filename_without_ext%>_mini1.<%ext%>',
                            'size':'300x300',
                            'quality':'100'
                        },
                        {
                            'description':'Для карточек товара',
                            'file':'<%filename_without_ext%>_mini2.<%ext%>',
                            'size':'585x585',
                            'quality':'100'
                        },
                    ]
                },
                {
                    'description':'Значение тэга alt',
                    'name':'alt',
                    'type':'text'
                }
            ],
            'filter_on':False
        },
        {
            'description':'Новинка',
            'name':'new',
            'type':'checkbox'
        },
        {
            'description':'ТОП',
            'name':'top',
            'type':'checkbox'
        },
        {
            'description':'Распродажа',
            'name':'sale',
            'type':'checkbox'
        },
        {
            'description':'Цвет',
            'name':'color_id',
            'table':'color',
            'tablename':'color',
            'type':'select_from_table',
            'header_field':'header',
            'value_field':'id',
            #'filter_code':lambda form,field,row: row['color__header']
        },
        {
            'description':'Модель',
            'name':'model_id',
            'table':'model',
            'tablename':'model',
            'type':'select_from_table',
            'header_field':'header',
            'value_field':'id',
        },
        {
            'description':'Сезон',
            'name':'season_id',
            'table':'season',
            'tablename':'season',
            'type':'select_from_table',
            'header_field':'header',
            'value_field':'id',
        },
        # {
        #     'description':'Год',
        #     'name':'year',
        #     'type':'text',
        #     'regexp_rules':[
        #         '^\d{4}$','укажите год, например 2024'
        #     ],
        #     'make_change_in_search':1,
        #     'filter_on':1,

        # },
        {
            'description':'Дата релиза',
            'name':'release_date',
            'type':'date',

        },
        {
            'description':'Параметры',
            'type':'1_to_m',
            'name':'params',
            'table':'good_param',
            'table_id':'id',
            'foreign_key':'good_id',
            'sort':1,
            'fields':[
                {
                    'description':'параметр',
                    'type':'text',
                    'name':'header',
                },
                {
                    'description':'Значение',
                    'type':'text',
                    'name':'value',
                },
            ],
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'description',
            'filter_on':False
        },

  ]  
    
}
      


