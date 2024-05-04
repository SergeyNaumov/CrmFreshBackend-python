from .fields import fields
from .query_search_tables import query_search_tables
form={
    'work_table':'arbotrage_ugrul',
    'work_table_id':'id',
    'not_create':True,
    'title':'Арбитражы - ЕГРЮЛ',
    'sort':False,
    'tree_use':False,
    'explain':False,
    'make_delete':0,
    'read_only':1,
    'QUERY_SEARCH_TABLES':query_search_tables,
    'fields': fields,
    'GROUP_BY':'wt.id',
}
