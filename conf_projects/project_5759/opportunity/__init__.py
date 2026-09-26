'''
create table struct_5759_opportunity(
    id int unsigned primary key auto_increment,
    sort int unsigned not null default '0',
    header varchar(100) not null default '',
) engine=innodb default charset=utf8 comment 'сферы деятельности';

'''
#from .fields import get_fields
form={
    'work_table':'struct_5759_opportunity',
    'work_table_id':'id',
    'title':'Сферы деятельности',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'changed_in_tree':True, 
    'fields': [ 
        {
            'description':'Сфера деятельности',
            'type':'text',
            'name':'header',
        },
        
  ]  
    
}
      


