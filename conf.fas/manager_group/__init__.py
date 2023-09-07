def permissions_before_code(form,field):
  pass

form={
    'work_table':'manager_group',
    'work_table_id':'id',
    'title':'Группы менеджеров',
    'sort':1,
    'tree_use':1,
    #'max_level':2,
    'read_only':1,
    'make_delete':0,
    'not_create':1,
    'explain':False,
    'fields': [ 
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Руководитель',
            'type':'select_from_table',
            'table':'manager',
            'header_field':'name',
            'name':'owner_id',
            'value_field':'id'
        },
        {
          'before_code': permissions_before_code,
          'description':'Права учётной записи',
          'add_description':'для юрлиц и аптек',
          'type':'multiconnect',
          'tree_use':1,
          'tree_table':'permissions',
          'name':'permissions',
          'tablename':'p',
          'relation_table':'permissions',
          'relation_save_table':'manager_group_permissions',
          'relation_table_header':'header',
          'relation_save_table_header':'header',
          'relation_table_id':'id',
          'relation_save_table_id_worktable':'group_id',
          'relation_save_table_id_relation':'permissions_id',
          'tab':'permissions',
          #'not_order':1,
          #'read_only':1
        },
   ]  
    
}
      

