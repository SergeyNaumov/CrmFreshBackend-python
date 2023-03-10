#from .fields import get_fields
form={
    'work_table':'wysiwyg_template',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Шаблоны для визивиг-редактора',
    'sort':1,
    'tree_use':False,
    'header_field':'title',
    'max_level':2,
    'default_find_filter':'title',
    'fields':[
 
        {
            'description':'Наименование шаблона',
            'type':'text',
            'name':'title',
        },
        {
          'description':'Краткое описание',
          'name':'description',
          'type':'text'
        },
        {
          'description':'Содержимое шаблона',
          'name':'body',
          'type':'textarea'
        },
    ]
}
      


