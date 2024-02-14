from .fields import get_fields

form={
    'work_table':'arbotrage_case',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Арбитражи',
    'sort':False,
    'tree_use':False,
    'explain':False,
    'make_delete':0,
    'read_only':1,
    #'QUERY_SEARCH_TABLES':query_search_tables,
    'fields': get_fields(),
    'GROUP_BY':'wt.id'
}
