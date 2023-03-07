#from .fields import get_fields
form={
    'work_table':'project',
    'work_table_id':'project_id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Проекты',
    'sort':1,
    'tree_use':0,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'wide_form':True,
    'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'cols':[
        [
            {'description':'Ссылки','name':'links'},
            {'description':'Общая информация','name':'info'},
        ],
        [
            {'description':'Работа с сущностями','name':'struct'},
        ]
    ],
    'QUERY_SEARCH_TABLES':[
        {'t':'project','a':'wt'},
        {'t':'project_struct_public','a':'psp','l':'psp.project_id=wt.project_id','lj':1,'for_fields':['struct_public']},
        {'t':'struct_public','a':'sp','l':'sp.struct_public_id=psp.struct_public_id','lj':1,'for_fields':['struct_public']},

        {'t':'domain','a':'d','l':'d.project_id = wt.project_id','lj':1},
    ],
    'GROUP_BY':'wt.project_id',
    #'explain':1,
    'fields':[
 
        {
            'description':'Название проекта',
            'type':'text',
            'name':'header',
            'tab':'info'
        },
        {
            'description':'Дата создания',
            'type':'datetime',
            'name':'registered',
            'tab':'info'
        },
        {
            'description':'Номер проекта',
            'name':'project_id',
            'type':'filter_extend_text',
            'filter_type':'range'
        },
        {
            'description':'Домен',
            'name':'domain_id',
            'tablename':'d',
            'type':'filter_extend_select_from_table',
            'table':'domain',
            'header_field':'domain',
            'value_field':'domain_id',
            'autocomplete':1
            
        },
        {
            'description':'Домены',
            'type':'1_to_m',
            'name':'domains',
            'table':'domain',
            'table_id':'domain_id',
            'foreign_key':'project_id',
            #'view_type':'list',
            'fields':[
                {
                    'description':'Домен',
                    'name':'domain',
                    'type':'text'
                },
                {
                    'description':'Шаблон',
                    'name':'template_id',
                    'type':'select_from_table',
                    'table':'template',
                    'autocomplete':1,
                    'header_field':'header',
                    'value_field':'template_id'
                },
                {
                    'description':'Размещение на сервере',
                    'name':'server_type',
                    'type':'select_values',
                    'values':[
                        {'v':1,'d':'CGI (1251)'},
                        {'v':3,'d':'PSGI (utf8)'},
                        {'v':4,'d':'Fastapi (utf8)'},
                    ]
                },
            ],
            'tab':'info'
        },
        {
            'type':'multiconnect',
            'description':'Стандартные сервисы',
            'name':'struct_public',
            'tablename':'psp',
            'fast_search':1,
            'cols':2,
            'relation_save_table':'project_struct_public',
            'relation_table':'struct_public',
            'relation_table_header':'header',
            'relation_table_id':'struct_public_id',
            'relation_save_table_id_relation':'struct_public_id',
            'relation_save_table_id_worktable':'project_id',
            'tab':'struct',

        },

   
    ]
}
      


