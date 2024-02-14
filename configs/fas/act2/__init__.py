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
        #   {'t':'bill','a':'b','l':'wt.bill_id=b.id','lj':1},
        #   {'t':'manager','a':'m','l':'m.id=wt.manager_id','lj':1},
        #   {'t':'manager_group','a':'mg','l':'m.group_id=mg.id','lj':1},
        #   {'t':'docpack','a':'dp','l':'b.docpack_id=dp.id'},
        #   {'t':'ur_lico','a':'ul','l':'ul.id=dp.ur_lico_id','lj':1,'for_fields':['ur_lico']},
        #   {'t':'user','a':'u','l':'u.id=dp.user_id','lj':1,'for_fields':['firm','inn']},
        #   {'t':'tarif','a':'t','l':'dp.tarif_id=t.id', 'for_fields':['tarif']},
          #{'t':'blank_document','a':'bd_fb','l':'bd_fb.id=t.blank_bill_id','for_fields':['blankument_doc_for_bill']}, # blank_document_for_bill
          #{'t':'dogovor','a':'d','l':'dp.id=d.docpack_id','for_fields':['d_number']}, # for_fields=>['blankument_doc_for_bill']
          #{'t':'ur_lico','a':'ul','l':'ul.id=dp.ur_lico_id','lj':1,'for_fields':['ur_lico_id']},
          #{'t':'user','a':'u','l':'dp.user_id=u.id'},
          #{'t':'buhgalter_card_requisits','a':'bcr','l':'bcr.id=wt.requisits_id','lj':1},
    ],
    'fields': fields
    
}
      

