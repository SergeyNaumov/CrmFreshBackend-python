#from .fields import get_fields
form={
    'work_table':'struct_5759_faq',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Вопрос / ответ',
    'sort':1,
    'explain':0,
    'header_field':'header',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'Вопрос',
            'type':'text',
            'name':'header',
        },

        {
            'description':'Ответ',
            'type':'wysiwyg',
            'name':'body',
            'edit_mode':True
        },
        {
        #   # before_code=>sub{
        #   #         my $e=shift;                    
                
        #   # },
           'description':'Услуги',
           'type':'multiconnect',
           'tree_table':'struct_5759_service',
           'relation_tree_order':'sort',
           'name':'services',
           'relation_table':'struct_5759_service',
           'relation_save_table':'struct_5759_faq_service',
           'relation_table_header':'header',
           'relation_table_id':'id',
           'relation_save_table_id_worktable':'faq_id',
           'relation_save_table_id_relation':'service_id',
           'tree_use':1
        #   'make_add':1,
        #   'view_only_selected':1,
        
        },
        {
            'description':'Выводить на главной',
            'type':'checkbox',
            'name':'main',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
        },

  ]  
    
}
      


