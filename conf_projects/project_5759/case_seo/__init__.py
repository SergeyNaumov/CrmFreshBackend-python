"""
CREATE TABLE `struct_5759_case_seo` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `header` varchar(100) NOT NULL DEFAULT '',
  `company` varchar(100) NOT NULL DEFAULT '' COMMENT 'Название компании',
  `type` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT 'вид кейса',
  `photo_mini` varchar(20) NOT NULL DEFAULT '0' COMMENT 'фото кейса в миниатюре',
  `photo` varchar(20) NOT NULL DEFAULT '0' COMMENT 'фото кейса в',
  `logo` varchar(20) NOT NULL DEFAULT '' COMMENT 'логтип',
  `service_id` int(10) unsigned NOT NULL DEFAULT '0',
  `opportunity` varchar(200) NOT NULL DEFAULT '',
  `block_about_content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8 COMMENT='Кейсы SEO'

"""
form={
    'work_table':'struct_5759_case_seo',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Кейсы SEO',
    
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Название кейса',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Название компании',
            'type':'text',
            'name':'company',
        },
        {
            'description':'Логотип',
            'type':'file',
            'name':'logo',
            'filedir':'./files/project_5759/case',
            'resize':[
                       {
                       'description':'Горизонтальное фото',
                       'file':'<%filename_without_ext%>_mini1.<%ext%>',
                       'size':'340x264',
                       'quality':'90'
                       },
            ]
        },
        {
            'description':'Фото кейса в миниатюра',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Фото кейса в миниатюра',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
        {
            'description':'Услуга',
            'name':'service_id',
            'type':'select_from_table',
            'table':'struct_5759_service',
            'tree_use':1,
            'header_field':'header',
            'value_field':'value'
        },
        {
            'description':'Сфера деятельности',
            'type':'text',
            'name':'opportunity',
        },
        {
            'description':'Вид кейса',
            'name':'type',
            'type':'select_from_table',
            'table':'struct_5759_case_type',
            'header_field':'header',
            'value_field':'value'
        },
        {
            'description':'Фото кейса в миниатюра',
            'type':'file',
            'name':'photo1',
            'filedir':'./files/project_5759/case_mini',
            'resize':[ { 'file':'<%filename_without_ext%>_mini1.<%ext%>', 'size':'315x157', 'quality':'90'} ]
        },
    ]
}
      


