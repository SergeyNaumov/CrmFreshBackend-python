"""
alter table article add promo_title varchar(255) not null default '';
alter table article add promo_description varchar(255) not null default '';
alter table article add promo_keywords varchar(255) not null default '';
"""
form={
    'work_table':'',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Статьи',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'fields': [ 
        {
            'description':'',
            'type':'',
            'name':'url',
            'filter_on':True
        },

  ]  
    
}
      


