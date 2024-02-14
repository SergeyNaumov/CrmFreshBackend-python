from .fields import fields
#from .ajax import ajax
form={
    'work_table':'beeline_abonent',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Абоненты Beeline',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'make_delete':False,
    'read_only':1,
    'not_edit':1,
    'search_on_load':1,
    #'ajax':ajax,
    # 'cols':[
    #           [
    #             {
    #               'description':'Общая информация','name':'main','hide':False,
    #             },
    #           ],
    #           [
    #             {
    #               'description':'Информация об оплате','name':'paid','hide':False,
    #             },
    #           ]
    # ],
    'QUERY_SEARCH_TABLES':
      [

          {'t':'beeline_abonent','a':'wt'},
          {'t':'manager','a':'m', 'l':'wt.manager_id=m.id'}

    ],
    'fields': fields
    
}
      

