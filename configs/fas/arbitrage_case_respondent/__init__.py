from .fields import get_fields

form={
    'work_table':'arbitrage_case_respondent',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Ответчики',
    'sort':False,
    'tree_use':False,
    'explain':True,
    'make_delete':0,
    'not_edit':1,
    'read_only':1,
    #'QUERY_SEARCH_TABLES':query_search_tables,
    'fields': get_fields(),
    'GROUP_BY':'wt.id',
}
