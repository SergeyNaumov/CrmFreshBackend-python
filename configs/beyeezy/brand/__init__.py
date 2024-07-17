def before_code_type(form,field):
  #print('form:',form)
  #print('field:',field)
  if not 'value' in field or not field['value']:
    field['value']='vue'

form={
    'work_table':'brand',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Бренды',
    'sort':True,
    'tree_use':False,
    'max_level':2,
    'explain':False,
    'fields': [ 
        {
            'description':'Наименование',
            'type':'text',
            'name':'header',
            
        },
        {
            'description':'Фото',
            'type':'file',
            'name':'photo',
            'filedir':'./files/brand',
            'preview':'214x293',
            'resize':[
                { # вертикальное фото
                    'file':'<%filename_without_ext%>_mini1.<%ext%>',
                    'size':'214x293',
                    'quality':'100'
                },
                { # горизонтальное фото
                    'file':'<%filename_without_ext%>_mini2.<%ext%>',
                    'size':'295x202',
                    'quality':'100'
                },
                { # лайтбокс
                    'file':'<%filename_without_ext%>_mini3.<%ext%>',
                    'size':'0x700',
                    'quality':'100'
                },
                { # вкладка "документы"
                    'file':'<%filename_without_ext%>_mini4.<%ext%>',
                    'size':'0x700',
                    'quality':'100'
                },
            ],
        },


  ]  
    
}
      

