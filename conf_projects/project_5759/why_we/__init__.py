"""
create table struct_5759_why_we(
    id int unsigned primary key auto_increment,
    header varchar(255),
    body varchar(255),
    photo varchar(20)
) engine=innodb default charset=utf8;
"""
form={
    'work_table':'struct_5759_why_we',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Почему к нам?',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'fields': [ 
        {
            'description':'Заголовок',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Описание',
            'type':'textarea',
            'name':'body',
        },
        {
            'description':'Фото',
            'add_description':'338x237',
            'type':'file',
            'name':'photo',
            'filedir':'./files/project_5759/why_we',
            #'crops':True,
            # 'resize':[
            #            {
            #            'description':'Квадратное фото',
            #            'file':'<%filename_without_ext%>_mini1.<%ext%>',
            #            'size':'280x280',
            #            'quality':'90'
            #            }
            # ]
        },

  ]  
    
}
      


