form={
    'work_table':'struct_[project_id]_paid', # заполняется в events
    'work_table_id':'id',
    'title':'Способы оплаты',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'',
    'wide_form':True,
    'changed_in_tree':True,
    'fields': [ 
        {
            'description':'Наименование способа доставки',
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
            'description':'Цена',
            'name':'price',
            'type':'text',
            'regexp_rules':[
                '/^\d+$/','укажите корректную цену'
            ],
            'replace_rules':[
                '/^[^\d]+$/',''
            ]

        },

  ]  
    
}
      


