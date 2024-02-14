QUERY_SEARCH_TABLES=[
	{'t':'user_bbg','a':'wt'},
	{'t':'manager','a':'m','l':'wt.manager_id=m.id','lj':1,'for_fields':['manager_id']},
	{'t':'manager','a':'mb','l':'wt.manager_bbg=mb.id','lj':1,'for_fields':['manager_bbg']},
	{'t':'user_bbg_memo','a':'memo','l':'wt.id=memo.user_bbg_id','lj':1,'for_fields':['memo']},
]