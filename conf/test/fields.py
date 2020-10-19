def kladr_after_search(data):
    i=0
    list=[]
    if not data:
        return list
    
    for d in data:
        res=[]
        for d2 in d['parents']:

            if d2['name']=='Москва' and d2['contentType']!='city':
                continue
            res.append,f'{d2["typeShort"]} {d2["name"]}'


        res.append(f'{d["typeShort"]} {d["name"]}')
        h=', '.join(res)
        list.append({'header':h})
    return list


fields=[ 

   {
        'description':'Wysiwyg',
        'type':'wysiwyg',
        'name':'wysiwyg',
        'not_filter':1,
        'tab':'wysiwyg'
    },
    # {
    #     'description':'Текстовое поле',
    #     'type':'text',
    #     'name':'header',
    #     change_in_search=>1,
    #     'tab';'plain'
    # },
    {
        'description':'Адрес',
        'type':'text',
        'name':'address',
        'subtype': 'kladr',
        'kladr':{
            #'after_search':kladr_after_search
        },
        'prefix_list_header':'Укажите регион',
        'prefix_list':['Москва','Московская Область','Калужская Область'],
        'change_in_search':1,
        'tab':'plain'
    },
    # {
    #     'description':'Наименование поля',
    #     add_'description':'дополнительное описание',
    #     'type':'textarea',
    #     'name':'textarea',
    #     full_str=>1,
    #     'tab';'plain'
    # },
    {
        'description':'checkbox',
        'type':'checkbox',
        'name':'checkbox',
        'tab':'plain'
    },
    {
        'description':'switch',
        'type':'switch',
        'name':'switch',
        'tab':'plain'
    },
    {
        'description':'Дата',
        'type':'date',
        'name':'f_date',
        'empty_value':'null',
        'tab':'timing',
        'change_in_search':1
    },
    # {
    #     'description':'Время',
    #     'type':'time',
    #     'name':'f_time',
    #     'tab';'timing'
    # },
    {
        'description':'Дата и время',
        'type':'datetime',
        'name':'f_datetime',
        'empty_value':'null',
        'tab':'timing'
    },
    # {
    #     'description':'Год и месяц (yearmon)',
    #     'type':'yearmon',
    #     'name':'f_yearmon',
    #     empty_value=>'null',
    #     'tab';'timing'
    # },
    # {
    #     'description':'День и месяц (daymon)',
    #     'type':'daymon',
    #     'name':'f_daymon',
    #     empty_value=>'null',
    #     'tab';'timing'
    # },
    {
        'name':'status',
        'description':'Выбор из списка (select_values)',
        'add_description':'с цветами',
        'type':'select_values',
        'change_in_search':1,
        # regexp_rules=>[
        #     q{/^[0-9]+$/},'Поле должно быть заполнено'
        # ],
        'values':[
            {'v':'0','d':'Другое','c':'#FFFFFF'},
            {'v':'1','d':'Ждем материалы от клиента','c':'#CC99FF'},
            {'v':'2','d':'Сделать медиаплан','c':'#FFFF00'},
            {'v':'3','d':'Сделать креатив','c':'#FF0000'},
            {'v':'4','d':'Работа с сайтом','c':'#99CCFF'},
            {'v':'5','d':'Мониторить рекламу','c':'#CCFFCC'},
            {'v':'6','d':'Сделать отчет','c':'#FF6600'},
            {'v':'7','d':'Работа закончена','c':'#DDDDDD'},
            {'v':'8','d':'Отправлять напоминание','c':'#24FF00'},
            {'v':'9','d':'Выставлен счёт','c':'#99CCFF'},
            {'v':'10','d':'Переговоры по продлению','c':'#800080'},
            {'v':'11','d':'Сделать конкурентный анализ','c':'#84193C'},
            {'v':'12','d':'Согласование УТП','c':'#164775'},
            {'v':'13','d':'Совместная работа','c':'#c1f498'},
        ],
        'tab':'plain'
    },
    # {
    #   # before_code=>sub{
    #   #         my $e=shift;                    
              
    #   # },
    #   'description':'Тэги',
    #   'type':'multiconnect',
    #   'tree_table':'tag',
    #   'name':'tags',
    #   'relation_table':'tag',
    #   'relation_save_table':'test_tag',
    #   'relation_table_header':'header',
    #   'relation_table_id':'id',
    #   'relation_save_table_id_worktable':'test_id',
    #   'relation_save_table_id_relation':'tag_id',
    #   'make_add':1,
    #   'view_only_selected':1,
    #   'tab':'tags'
    # },
    # { # Memo
    #     # Комментарий 
    #     'description':'Комментарий',
    #     'name':'memo',
    #     'type':'memo',
    #     'memo_table':'test_memo',
    #     'memo_table_id':'id',
    #     'memo_table_comment':'body',
    #     'memo_table_auth_id':'manager_id',
    #     'memo_table_registered':'registered',
    #     'memo_table_foreign_key':'test_id',
    #     'auth_table':'manager',
    #     'auth_login_field':'login',
    #     'auth_id_field':'id',
    #     'auth_name_field':'name',
    #     'reverse':1,
    #     'memo_table_alias':'memo',
    #     'auth_table_alias':'m_memo',
    #     'make_delete':'1',
    #     'make_edit':'1',
    #     'tab':'memo'
    # },
   {
     'description':'Файл',
     'type':'file',
     'name':'file',
     'filedir':'./files/test/files'
   },
    # {
    #     'description':'1_to_m',
    #     'type':'1_to_m',
    #     'name':'onetom_test',
    #     'table':'test_onetomany',
    #     'table_id':'id',
    #     'foreign_key':'test_id',
    #     'tab':'one_to_m',
    #     'sort':1,
    #     'view_type':'list',  
    #     'fields':[
    #         {
    #             'description':'select',
    #             'name':'sel',
    #             'type':'select_values',
    #             'values':[
    #                 {'v':1,'d':'красный'},
    #                 {'v':2,'d':'оранжевый'},
    #                 {'v':3,'d':'жёлтый'},
    #                 {'v':4,'d':'зелёный'},
    #                 {'v':5,'d':'Голубой'},
    #                 {'v':6,'d':'Синий'},
    #                 {'v':7,'d':'Фиолетовый'},
    #             ]
    #         },
    #         {
    #             'description':'chk',
    #             'name':'chk',
    #             'type':'checkbox'
    #         },
    #         {
    #             'description':'Телефон',
    #             'type':'text',
    #             'name':'phone',
    #             'change_in_slide':1,
    #             'replace_rules':[
    #                 '/^8/','+7',
    #             ],
    #             'regexp_rules':[
    #                 #q{/^\+[0-9]+$/},'Номер телефона в формате: +7XXXXXXXXXX, например: +74951234567',
    #                 #q{/^[0-9]+$/}=>'Допускаются только цифры',
    #             ]
    #         },

    #         {
    #             'description':'Файл',
    #             'type':'file',
    #             'name':'attach',
    #             'keep_orig_file_name':1,
    #             'filedir':'./files/test',
    #             'read_only':1,
    #             'preview':'200x0'
    #         }
    #     ]
    # },
    # {
    #     'description':'Соцсети',
    #     'name':'soc',
        
    #     'type':'1_to_m',
    #     table=>'test_social',
    #     table_id=>'id',
    #     foreign_key=>'test_id',
    #     'tab';'one_to_m',
    #     fields=>[
    #       {
    #         'description':'Соцсеть',
    #         'type':'select_values',
    #         'name':'social_id',
    #         values=>[
    #           {'v':1,'d':'vk'},
    #           {'v':2,'d':'ok'},
    #           {'v':3,'d':'facebook'},
    #         ]
    #       },
    #       {
    #         'description':'ссылка на профиль',
    #         'name':'profile',
    #         'type':'textarea',
    #       }
    #     ]
    # },
]