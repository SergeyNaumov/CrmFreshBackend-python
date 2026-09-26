#from .fields import get_fields
async def before_code_top(form,field):
    if form.action=='new':
        field['value']=1

form={
    'work_table':'struct_5830_news',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Новости',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Название новости',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Дата (для сортировки)',
            'type':'date',
            'name':'registered',
        },
        {
            'description':'Анонс',
            'type':'textarea',
            'name':'anons',
        },
        {
            'description':'Описание',
            'type':'wysiwyg',
            'name':'body',
        },
        {
            'description':'Название-2',
            'add_description':'выводится под анонсом новости белым шрифтом',
            'type':'text',
            'name':'header2',
        },
        {
            'description':'Фото',
            'name':'photo',
            'type':'file',
            'filedir':'./files/project_5830/news',
        },
        {
             'description':'Ссылка на новость',
             'add_description':'если не стандартная',
             'type':'text',
             'name':'url_old',
         },
        {
            'description':'TOP',
            'type':'checkbox',
            'name':'top',
        },
        {
            'description':'Вкл',
            'type':'checkbox',
            'name':'enabled',
            'before_code':before_code_top
        },
    ]
}



