from .fields import fields
#from .ajax import ajax
form={
    'work_table':'arbitrage_court',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Cуды',
    'sort':False,
    'tree_use':False,
    'explain':False,
    'make_delete':0,
    'read_only':1,
    'search_on_load':1,

    'QUERY_SEARCH_TABLES':
      [
          {'t':'arbitrage_court','a':'wt'},
      ],
    'fields': fields
    
}
      

