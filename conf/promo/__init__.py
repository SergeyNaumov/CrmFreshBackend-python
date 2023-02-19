#from .fields import get_fields
form={
    'work_table':'promo',
    'work_table_id':'promo_id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Promo (для оптимизаторов)',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'',
    'fields': [ 
        {
            'description':'url',
            'type':'text',
            'name':'url',
            'filter_on':True
        },
        {
          'description':'Title',
          'name':'promo_title',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
        {
          'description':'Descrption',
          'name':'promo_description',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
        {
          'description':'Keywords',
          'name':'promo_keywords',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
        {
          'description':'Promo body',
          'name':'promo_body',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
        {
          'description':'h1',
          'name':'h1',
          'type':'text',
          'make_change_in_search':True,
          'filter_on':True
        },
  ]  
    
}
      


