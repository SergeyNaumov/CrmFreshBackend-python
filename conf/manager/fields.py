
def send_mes():
    print()

def password_method_send(new_password):
            send_mes()

def get_fields():
    return [ 

 {
      'description':'ID',
      'name':'id',
      'type':'text',
      'read_only':1,
      'filter_on':1

    },
    {
      'name':'name',
      'description':'Имя',
      'type':'text',
      'tab':'main',
      'filter_on':1
    },
    {
      'name':'login',
      'description':'Логин',
      
      'type':'text',
      'filter_on':1,
      #regexp':'^[a-zA-Z\-_0-9\.\@]+$',
      # filter_code=>sub{
      #   my $e=shift;
      #   my $login=$e->{str}->{wt__login};
      #   $login=~s{([^a-zA-Z\-_0-9\.\@]+)}{<span style="color: red;">$1</span>}gs;
      #   return $login;
      # },
      'unique':1,
      'regexp_rules':[
        '/.{5}/','длина логина должна быть не менее 5 символов',
        '/^[a-zA-Z0-9\.\-_@\/]+$/','только символы: a..z,A..Z, 0-9, _, -, @, .'
      ],
      'tab':'main'
    },

    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
       'tab':'main',
       'regexp_rules':[
        '^(\+7\d{10})?$/','Если указывается телефон, он должен быть в формате +7XXXXXXXXXX',
      ],
      'replace_rules':[
        ['/^[87]/','+7'],
        ['/[^\d\+]+/',''],
        ['/^([^87\+])/','+7$1']
      ]
      #regexp':'^(\+\d{6}\d*)?$',
      # replace=>[
      #   ['(^\(|,\s*\()','+7'],
      #   ['[^\+\s\d,]',''],
      #   ['(^\s+|[^,\d]\s+$)',''],
      #   ['(^|,\s*)(9|4)','$1+7$2'],
      #   ['(^|,\s*)[8]','+7'],
      #   ['^(\d)',' +$1'],
      #   ['(,\s*)(\d)',', +$2'],
      #   ['(\d)\s(\d)','$1$2'],
      #   ['(,\s*),','$1'],
      #   ['(\d)\+7','$1, +7']
      # ],
    },

    {
      'description':'Пароль',
      'name':'password',
      'type':'password',
      'encrypt_method':'sha256',
      'methods_send':[
        {
          'description':'сохранить',
          'method_send':password_method_send
        }
      ],
       'tab':'main'
    },
    {
      'description':'Зарегистрирован',
      'type':'datetime',
      'name':'registered',
      'read_only':1,
      'tab':'permissions'
    },
    { 
      'description':'Имеет доступ в систему',
      'name':'enabled',
      'type':'checkbox',
      'tab':'permissions'
    },
    {
      'name':'type',
      'description':'Тип учётной записи',
      'type':'select_values',
      'tab':'permissions',
      'values':[
        {'v':'1','d':'Сотрудник компании Анна'},
        {'v':'2','d':'Представитель юридического лица'},
        {'v':'3','d':'Представитель аптеки'},
      ]
    },
    {
       'name':'email',
       'description':'Email',
       'type':'text',
        'replace':[
            ['\s+','']
        ],
        'regexp':'^([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-]+)?$',

       'tab':'main'
    },



]
