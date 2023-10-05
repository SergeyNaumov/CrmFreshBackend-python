

form={
    'work_table':'blank_document',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Бланки документов',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'fields': [ 
        {
          'description':'Название бланка',
          'name':'header',
          'type':'text'
        },
        {
          'description':'Файл бланка',
          'add_description':'в формате odt',
          'type':'file',
          'name':'attach',
          'filedir':'./files/blank_document'
        },
        {
          'description':'Последнее обновление',
          'type':'datetime',
          'name':'registered',
          'read_only':1,

        },
        {
          'description':'Изображения в документе, которые являются печатью',
          'name':'ur_lico_attach_pechat',
          'type':'text'
        },
        {
          'description':'Изображения в документе, которые являются подписью ген. директора',
          'name':'ur_lico_gendir_podp',
          'type':'text'
        },
        {
          'description':'Изображения в документе, которые являются подписью глав. буха',
          'name':'ur_lico_buh_podp',
          'type':'text'
        }
#        {
#          'description':'Доступен для выбора в "доп. файлах"',
#          'name':'to_other_files',
#          'type':'checkbox',
#        },
  ]  
    
}
      


