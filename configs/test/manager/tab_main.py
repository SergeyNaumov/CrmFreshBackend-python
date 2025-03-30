from lib.send_mes import send_mes


async def send_new_password(form,field,newpass):
  # print('ov:',form.id)
  #print('send: ',field,newpass)
  if email:=form.ov['email']:
    send_mes(
      subject='Вам сгенерирован пароль для входа в систему Fas',
      to=email,
      message=f"""
        Ссылка для входа в ЛК: <a href="https://fas.crm-dev.ru/">https://fas.crm-dev.ru/</a>
        Логин: {form.ov['login']}<br>
        Пароль: {newpass}<br>
      """
    )

async def without_send(form,field,newpass):
    return

fields=[
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
      #'read_only':1,
      'unique':1,
      'regexp_rules':[
        '/.{3}/','длина логина должна быть не менее 3 символов',
        #'/^[a-zA-Z0-9\.\-_@\/]+$/','только символы: a..z,A..Z, 0-9, _, -, @, .'
      ],
      'frontend':{'ajax':{'name':'login','timeout':600}},
      'tab':'main'
    },
    {
      'description':'Пароль',
      'name':'password',
      'type':'password',
      'min_length':8,
      'symbols':'123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
      'methods_send':[
        {
          'description':'сохранить и отправить по электронной почте',
          'method_send':send_new_password
        },
        {
          'description':'сохранить и никуда не отправлять',
          'method_send': without_send
        }
      ],
      #'before_code':password_before_code,
      'tab':'main'
    },
    {
        'description': 'Группа',
        'name': 'group_id',
        'type': 'select_from_table',
        'table': 'manager_group',
        'tablename': 'mg',
        'header_field': 'header',
        'value_field': 'id',
        'filter_on':1,
        'regexp_rules':[
              '/^.+$/','Укажите группу',
        ],
        'tab': 'main',
    },
    {
      'description':'Email',
      'name':'email',
      'type':'text',
      'tab':'main'

    },
    {
      'description':'Email',
      'name':'email',
      'type':'filter_extend_text',
      'tablename':'me',
      'db_name':'group_concat( distinct me.email) SEPARATOR ", "'
    },

    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'tab':'main',
      'frontend':{'ajax':{'name':'phone','timeout':600}},
      #'read_only':1,
      # 'regexp_rules':[
      #     '/^(\+7 \(\d{3}\) \d{3}-\d{2}-\d{2})?$/','Если указывается телефон, он должен быть в формате +7 (XXX) XXX-XX-XX',
      # ],
      'replace_rules':[
          '/[^\d]/g','',
          '/^(\d{11}).*$/','$1',
          '/^[87]/','+7',
          '/^\+7(\d{3})(\d)/','+7 ($1) $2',
          '/^(\+7 \(\d{3}\))(\d{3})/','$1 $2',
          '/(\d{3})(\d{2})/',"$1-$2",
          '/-(\d{2})(\d{2}\d*)$/',"-$1-$2"

      ]
    },
    {
      'description':'Сохранять запись',
      'type':'checkbox',
      'name':'cloud_ats',
      'tab':'main'
    },
    {
        'description':'фото',
        'type':'file',

        'name':'photo',
        #'keep_orig_filename':1,
        'filedir':'./files/manager',
        'preview':'200x200',
        'crops':1,
        'tab':'main',
        'resize':[
            {
              'description':'Квадратное фото',
              #'file':'<%filename_without_ext%>_mini1.<%ext%>',
              'file':'<%filename_without_ext%>.<%ext%>',
              'size':'200x200',
              'quality':'95'
            },

        ]
    },
    {
      'description':'Уволен',
      'type':'checkbox',
      'name':'gone',
      'tab':'main',
    },
    {
      'name':'name',
      'description':'ФИО',
      'type':'text',
      #'read_only':1,
      'tab':'main',
      'regexp_rules':[
          '/^.+$/','Полное имя обязательно для заполнения',
      ],
      'filter_on':1
    },
    {
      'name':'comment',
      'description':'Комментарий',
      'type':'textarea',
      'tab':'main',
    },
]
