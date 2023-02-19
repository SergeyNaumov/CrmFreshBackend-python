"""
create table struct_5759_slider(
    id int unsigned primary key auto_increment,
    sort int unsigned not null default '0',
    header varchar(512) not null default '',
    photo varchar(20) not null default ''
) engine=innodb default charset=utf8;
alter table struct_5759_slider add photo_mob varchar(20) not null default ''
"""
form={
    'work_table':'struct_5759_slider',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Слайдер изображений',
    'sort':1,
    'tree_use':0,
    'header_field':'header',
    'default_find_filter':'',
    #'changed_in_tree':True, 
    'fields': [ 
        {
            'description':'Заголовок',
            'type':'textarea',
            'name':'header',
        },
        {
            'description':'Url',
            'name':'url',
            'type':'text'
        },
        {
            'description':'Фото, ПК',
            'add_description':'svg',
            'type':'file',
            'name':'photo',
            'filedir':'./files/project_5759/slider',
#            'crops':True,
            # 'resize':[
            #         {
            #            'description':'Фото ПК',
            #            'file':'<%filename_without_ext%>_mini1.<%ext%>',
            #            'size':'753x448',
            #            'quality':'90'
            #         },
            #         {
            #            'description':'Фото моб',
            #            'file':'<%filename_without_ext%>_mini2.<%ext%>',
            #            'size':'241x143',
            #            'quality':'90'
            #         },
            # ]
        },
        {
            'description':'Фото, мобильные',
            'add_description':'svg',
            'type':'file',
            'name':'photo_mob',
            'filedir':'./files/project_5759/slider',
#            'crops':True,
            # 'resize':[
            #         {
            #            'description':'Фото ПК',
            #            'file':'<%filename_without_ext%>_mini1.<%ext%>',
            #            'size':'753x448',
            #            'quality':'90'
            #         },
            #         {
            #            'description':'Фото моб',
            #            'file':'<%filename_without_ext%>_mini2.<%ext%>',
            #            'size':'241x143',
            #            'quality':'90'
            #         },
            # ]
        },
        {
            'description':'Кнопка',
            'type':'text',
            'name':'button',
        },


  ]  
    
}
      


