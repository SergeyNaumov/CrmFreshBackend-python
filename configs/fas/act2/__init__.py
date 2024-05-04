from .fields import fields
#from .ajax import ajax
form={
    'work_table':'act2',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Акты',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'make_delete':0,
    'read_only':1,
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

          {'t':'act2','a':'wt'},
          {'t':'docpack','a':'dp','l':'dp.id=wt.docpack_id', 'lj':1},
          {'t':'user','a':'u','l':'dp.user_id=u.id','lj':1},
          {'t':'ur_lico','a':'ul','l':'ul.id=dp.ur_lico_id','lj':1,'for_fields':['ur_lico_id']},
    ],
    'fields': fields
    
}
      

