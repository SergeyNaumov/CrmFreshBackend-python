
form={
    'work_table':'category',
    'work_table_id':'id',
    'title':'Категории',
    'sort':True,
    'tree_use':True,
    'max_level':2,
    'explain':False,
    #'changed_in_tree':True,
    'fields': [ 
        {
            'description':'Наименование категории',
            'type':'text',
            'name':'header',
            
        },
        {
            'description':'Ключевое слово',
            'type':'text',
            'name':'keyword',
            
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'body'
        },
        {
            'description':'Таблица размеров',
            'type':'1_to_1_wysiwyg',
            'save_table':'category_sizes',
            'foreign_key':'id',
            'name':'size_table',
            'db_name':'body'
        }
  ]  
    
}

