ur_lico_filedir='files/slider'

form={
    'work_table':'slider',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Слайдер',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    'fields': [ 
        {
          'description':'Вкл',
          'type':'checkbox',
          'name':'enabled',
          'value':1
        },
        {
          'description':'Название слайда',
          'type':'text',
          'name':'header',
        },
        {
          'description':'url',
          'type':'text',
          'name':'url',
        },
        {
          'description':'Фото слайда, desktop',
          'add_description':'1680x840',
          'name':'photo',
          'type':'file',
          'filedir':'./files/slider'
        },
        {
          'description':'Фото слайда, моб. устройства',
          'add_description':'640x900',
          'name':'photo_mob',
          'type':'file',
          'filedir':'./files/slider'
        },
  ]  
    
}
      


