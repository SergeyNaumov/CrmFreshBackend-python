from .fields import fields

form={
    'work_table':'bill',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'not_create':True,
    'title':'Счета',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'make_delete':0,
    'read_only':1,
    'QUERY_SEARCH_TABLES':
      [
          {'t':'bill','a':'wt',},
          {'t':'act','a':'act','l':'wt.id=act.bill_id','for_fields':['act_number'],'lj':1},
          {'t':'manager','a':'m','l':'m.id=wt.manager_id','lj':1},
          {'t':'manager_group','a':'mg','l':'m.group_id=mg.id','lj':1},
          {'t':'docpack','a':'dp','l':'wt.docpack_id=dp.id'},
          {'t':'tarif','a':'t','l':'dp.tarif_id=t.id'},
          {'t':'blank_document','a':'bd_fb','l':'bd_fb.id=t.blank_bill_id','for_fields':['blankument_doc_for_bill']}, # blank_document_for_bill
          {'t':'dogovor','a':'d','l':'dp.id=d.docpack_id','for_fields':['d_number']}, # for_fields=>['blankument_doc_for_bill']
          {'t':'ur_lico','a':'ul','l':'ul.id=dp.ur_lico_id','lj':1,'for_fields':['ur_lico_id']},
          {'t':'user','a':'u','l':'dp.user_id=u.id'},
          {'t':'buhgalter_card_requisits','a':'bcr','l':'bcr.id=wt.requisits_id','lj':1},
         # {'t':'bill_part', 'a':'bp', 'l':'bp.bill_id=wt.id', 'lj':1},
          #{'t':'bill_part_comment','a':'bpc', 'l':'bpc.id=bp.comment_id','lj':1},
    ],
    'fields': fields
    
}
      

