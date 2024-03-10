"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
form={
    'work_table':'snt',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'СНТ',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'QUERY_SEARCH_TABLES':[
        {'t':'snt','a':'wt'},
        {'t':'manager','a':'m','l':'m.id=wt.owner_id','lj':1}
    ],
    'fields': [ 
        {
            'description':'Название СНТ',
            'type':'text',
            'name':'header',
            'filter_on':True
        },
        {
            'description':'Председатель СНТ',
            'type':'select_from_table',
            'name':'owner_id',
            'table':'manager',
            'tablename':'m',
            'header_field':'name',
            'value_field':'id'
        }
  ]  
    
}
      


