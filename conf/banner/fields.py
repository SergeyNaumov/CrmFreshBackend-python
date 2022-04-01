from lib.send_mes import send_mes


def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Название баннера',      
      'type':'text',
      'filter_on':1,
      'regexp_rules':[
        '/.{1}/','название обязательно',
      ],
    },
    {
      'description':'Вкл',
      'name':'enabled',
      'filter_on':1,
      'type':'switch',
      'before_code':enabled_before_code
    },
    {
      'description':'Url',
      'type':'text',
      'filter_on':1,
      'name':'url',
    },
    {
      'name':'attach',
      'description':'Файл баннера',
      'add_description':'подготовленное изображение 300Х200',
      'type':'file',
      'filter_on':1,
      'filedir':'./files/bfiles'
    },
    {
      'name':'type',
      'description':'Местоположение (desktop)',
      'add_description':'если не указано -- не выводить',
      'regexp_rules':[
        #'/^\d+$/','укажите местоположение баннера',
      ],
      'type':'select_values',
      'filter_on':1,
      'values':[
        {'v':1,'d':'справа верх'},
        {'v':2,'d':'справа низ'},
        {'v':3,'d':'слева верх'},
        {'v':4,'d':'слева низ'},
      ],
      'tab':'main',
    },
    {
      'name':'type_mobile',
      'description':'Местоположение (мобильные устройства)',
      'add_description':'если не указано -- не выводить',
      'regexp_rules':[
        #'/^\d+$/','укажите местоположение баннера',
      ],
      'type':'select_values',
      'filter_on':1,
      'values':[
        {'v':1,'d':'сверху'},
        {'v':2,'d':'снизу'},
      ],
      'tab':'main',
    },
    # {
    #   'description':'Кол-во секунд',
    #   'type':'text',
    #   'name':'count_sec',
    #   'regexp_rules':[
    #     '/^\d+$/','только число',
    #   ],
    #   'filter_on':1,
    #   'before_code':count_sec_before_code
    # }
]

def enabled_before_code(form,field):
  if form.action == 'new':
    field['value']=1

def count_sec_before_code(form,field):
  if form.action == 'new':
    field['value']='0'