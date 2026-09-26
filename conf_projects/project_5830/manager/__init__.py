#from .fields import get_fields
async def before_code_top(form,field):
    if form.action=='new':
        field['value']=1

form={
    'work_table':'struct_5830_manager',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Менеджеры',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Имя',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Должность',
            'type':'text',
            'name':'position',
        },
        {
            'description':'Телефон',
            'type':'text',
            'name':'phone',
        },
        {
            'description':'Email',
            'type':'text',
            'name':'email',
        },
        {
            'description':'Фото',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5830/manager',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            #'before_code':before_code_top
        },
    ]
}



