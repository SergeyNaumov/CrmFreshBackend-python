def before_code_photo(form,field):
  field['filedir']=f'./files/project_{form.s.shop_id}/catalog'
  #form.pre(field)


form={
    'work_table':'catalog',
    'work_table_id':'id',
    #'work_table_foreign_key':'s_id',
    #'work_table_foreign_key_value':4664,
    'title':'Каталог товаров',
    'sort':1,
    'tree_use':1,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    #'changed_in_tree':True, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
 
        {
            'description':'Наименование раздела',
            'type':'text',
            'name':'header',
        },
        { # Внимание, важен порядок поля, в events к нему обращение
            'description':'Фото',
            'type':'file',
            'name':'photo',
            'file_type':'image',
            'filedir':'./files/project_<%shop_id%>/catalog',
            'before_code':before_code_photo,
            'resize':[
              {
                'file':'<%filename_without_ext%>_mini1.<%ext%>',
                'size':'230x230',
                'quality':'100'
              },
              {
                'file':'<%filename_without_ext%>_mini2.<%ext%>',
                'size':'72x32',
                'quality':'100'
              }
            ]

        },
        # {
        #   'description':'Анонс',
        #   'name':'anons',
        #   'type':'textarea'
        # },
        {
          'description':'Подробное описание',
          'name':'body',
          'type':'wysiwyg'
        },
    ]
}
      


