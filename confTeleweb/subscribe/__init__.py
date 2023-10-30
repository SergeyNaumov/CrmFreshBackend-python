

form={
    'work_table':'subscribe',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Рассылка',
    'sort':True,
    'tree_use':False,
    'explain':False,
    'header_field':'header',
    'default_find_filter':'header',
    'fields': [ 
        {
            'description':'Название рассылки',
            'add_description':'название рассылке видно только Вам',
            'type':'text',
            'name':'header',    
            'filter_on':True
        },
        {
            'description':'Метка для отправки',
            'add_description':'это метка, с которой был зарегистрирован пользоователь. если не заполнено, то уйдёт всем',
            'name':'mark',
            'type':'text',
            'filter_on':True
        },
        {
            'description':'Дата создания',
            'type':'datetime',
            'name':'registered',
            'read_only':1,
            'filter_on':True
        },
        {
            'description':'Рассылка отправлена',
            'type':'checkbox',
            'name':'send',
            #'read_only':1,
            'filter_on':True
        },        
        {
            'description':'Время отправки',
            'type':'datetime',
            'name':'send_time',
            'read_only':1,
            'filter_on':True
        },
        {
            'description':'Текст рассылки',
            'name':'body',
            'type':'textarea',
            'regexp_rules':[
                '/.+/','Заполните поле текстом рассылки',
            ],
            'after_html':'''В тексте сообщении иожете использовать специальные строки:<br>
                <b>&lt;first_name&gt;</b> - имя<br>
                <b>&lt;last_name&gt;</b> - фамилия<br>

            '''
        },
        {
            'description':'Отправить после',
            'type':'datetime',
            'name':'send_after',
            'read_only':0,
            'filter_on':True
        },


        

  ]  
    
}
      


