#from .fields import get_fields
async def before_code_top(form,field):
    if form.action=='new':
        field['value']=1

form={
    'work_table':'struct_5830_owner',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Заказчики и клиенты',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Название',
            'type':'text',
            'name':'header',
        },


        {
            'description':'Лого',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5830/owner',
        },
        {
            'description':'Url',
            'type':'text',
            'name':'url',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            #'before_code':before_code_top
        },
    ]
}



