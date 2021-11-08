def get_fields():
    return [ 
    {
      'name':'info',
      'type':'code',
      'code':info_code
    },
    {
      'name':'registered',
      'description':'Дата и время заявки',
      'type':'date',
      'read_only':1,
      'filter_on':1
    },
    {
      'description':'Статус заявки',
      'name':'status',
      'type':'select_values',
      'values':[
        {'v':1,'d':'В работе'},
        {'v':2,'d':'Закрыта'},
      ]

    },

    # {
    #   'name':'firm',
    #   'description':'Логин',
    #   'type':'text',
    #   'filter_on':1
    # }, 
    {
      'name':'phone',
      'description':'Телефон',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Роль',
      'name':'type',
      'type':'filter_extend_select_values',
      'tablename':'m',
      'filter_on':1,
      'values':[
        {'v':1,'d':'менеджер АннА'},
        {'v':2,'d':'представитель юрлица'},
        {'v':3,'d':'представитель аптеки'},
      ],
      'filter_code':filter_code_type
    },
    {
      'name':'name_f',
      'description':'Фамилия',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'name_i',
      'description':'Имя',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'name_o',
      'description':'Отчество',
      'type':'text',
      'filter_on':1
    },

]

def info_code(form,field):
  out='';
  out+=f"<b>Юридическое лицо:</b>"
  field['after_html']=out

def filter_code_type(form,field,row):

  if row['m__type']==2:
    return f'''представитель юрлица: <u>{row['ul__header']}</u>'''
  
  if row['m__type']==3:
    return f'''представитель аптеки: <u>{row['apt__ur_address']}</u><br><small>({row['ul2__header']})</small>'''

  
  return 'менеджер АннА'