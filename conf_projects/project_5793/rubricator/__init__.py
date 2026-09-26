form={
    'work_table':'struct_[project_id]_rubricator', # заполняется в events,
    'work_table_id':'id',
    'title':'Каталог товаров',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'max_level':2,
    'wide_form':True,
    'fields': [ 
        {
            'description':'Наименование рубрики',
            'type':'text',
            'name':'header',
            'tab':'main',
            #'frontend':{
            #    'ajax':{
            #        'name':'in_ext_url'
            #    }
            #}
        },
        {
            'description':'Иконка',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_[project_id]/rubricator',
            'tab':'main'
        },

  ]  
    
}
      


