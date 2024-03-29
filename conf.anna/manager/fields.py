from lib.send_mes import send_mes


def get_fields():
    return [ 
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
      'read_only':1,
      'unique':1,
      'regexp_rules':[
        '/.{5}/','длина логина должна быть не менее 5 символов',
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
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'tab':'main',
      'read_only':1,
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
      'name':'name',
      'description':'ФИО',
      'type':'text',
      'read_only':1,
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
    # {
    #   'name':'name_f',
    #   'description':'Фамилия',
    #   'type':'text',
    #   'tab':'main',
    #   'filter_on':1,
    #   'frontend':{'ajax':{'name':'name','timeout':300}}
    # },
    # {
    #   'name':'name_i',
    #   'description':'Имя',
    #   'type':'text',
    #   'tab':'main',
    #   'filter_on':1,
    #   'frontend':{'ajax':{'name':'name'}}
    # },
    # {
    #   'name':'name_o',
    #   'description':'Отчество',
    #   'type':'text',
    #   'tab':'main',
    #   'filter_on':1,
    #   'frontend':{'ajax':{'name':'name'}}
    # },
    # {
    #   'description':'Зарегистрирован',
    #   'type':'datetime',
    #   'name':'registered',
    #   'read_only':1,
    #   'tab':'permissions'
    # },
    { 
      'description':'Доступ к просмотру прогнозного бонуса за прошлый квартал',
      'name':'show_old_plans',
      'type':'checkbox',
      'tab':'permissions',
      #'before_code':enabled_before_code
    },
    # { 
    #   'description':'Имеет доступ в систему',
    #   'name':'enabled',
    #   'type':'checkbox',
    #   'tab':'permissions',
    #   'before_code':enabled_before_code
    # },
    {
      'name':'type',
      'description':'Тип учётной записи',
      'read_only':1,
      'type':'select_values',

      'tab':'permissions',
      'before_code':type_before_code,
      'values':[
        {'v':1,'d':'Сотрудник компании Анна'},
        {'v':2,'d':'Представитель юридического лица'},
        {'v':3,'d':'Представитель аптеки'},
        {'v':4,'d':'Фармацевт'},
      ]
    },
    {
      'description':'Менеджер компании АннА',
      'add_description':'для ',
      'name':'anna_manager_id',
      'read_only':1,
      'type':'select_from_table',
      'header_field':'name',
      'where':'type=1',
      'table':'manager',
      'tablename':'ma',
      'value_field':'id',
      'tab':'permissions',
      'filter_code': anna_manager_id_filter_code
    },
    {
      'before_code': permissions_before_code,
      'description':'Права учётной записи',
      'add_description':'для юрлиц и аптек',
      'type':'multiconnect',
      'tree_use':1,
      'tree_table':'permissions',
      'name':'permissions',
      'tablename':'p',
      'relation_table':'permissions',
      'relation_save_table':'manager_permissions',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'manager_id',
      'relation_save_table_id_relation':'permissions_id',
      'tab':'permissions',
      #'not_order':1,
      'read_only':1
    },
    {
       'name':'email',
       'description':'Email',
       'read_only':1,
       'type':'text',
        'replace':[
            ['\s+','']
        ],
        #'regexp':'^([a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z0-9_\-]+)?$',

       'tab':'main'
    },
    {
      'description':'Юр.лицо',
      'type':'filter_extend_select_from_table',
      'name':'ur_lico_id',
      'db_name':'id',
      'table':'ur_lico',
      'header_field':'header',
      'value_field':'id',
      'tablename':'u',
      'filter_code':ur_lico_id_filter_code
    },
    # Юридические лица
    {
      'description':'Юридические лица',
      'name':'comp',
      'type':'1_to_m',
      'table':'comp',
      'table_id':'id',
      'foreign_key':'manager_id',
      'tab':'comp',
      'fields':[
        {
          'description':'Юридическое лицо',
          'type':'select_from_table',
          'table':'comp',
          'header_field':'header',
          'value_field':'id',
          'name':'comp_id'
        }
      ]
    },
    {
      'description':'Доступ к видео',
      'name':'access_to_video',
      'type':'checkbox',
      'tab':'permissions',
      'before_code':access_to_video_bc
    },
    {
      'description':'Доступ к конференциям',
      'name':'access_to_conf',
      'type':'checkbox',
      'tab':'permissions',
      'before_code':access_to_video_bc
    },

]
def ur_lico_id_filter_code(form,field,row):
  return row["ur_lico_list"]
  
def anna_manager_id_filter_code(form,field,row):
  if row['ma__id']:
    return row['ma__name_f']+' '+row['ma__name_i']+row['ma__name_o']
  else:
    return 'не указан'

def without_send():
    return 

def send_new_password(form,field,newpass):
  #print('ov:',form.ov)
  #print('send: ',field,newpass)
  if form.ov['email']:
    send_mes(
      subject='Вам сгенерирован пароль для входа в систему AннА',
      to=form.ov['email'],
      message=f"""
        Ссылка для входа в ЛК: <a href="https://anna.crm-dev.ru/">https://anna.crm-dev.ru/</a>
        Логин: {form.ov['login']}<br>
        Пароль: {newpass}<br>
        Если появятся вопросы свяжитесь удобным для Вас способом:<br>
        Телефон: +7-901-993-58-28<br>
        E-mail: AnnAvoronezh2017@yandex.ru<br>
      """
    )
  #send_mes()

def permissions_before_code(**arg):
  form=arg['form']
  field=arg['field']

  # Для администратора или для менеджера с галкой открываем возможность изменять права доступа
  if form.is_admin:
    field['read_only']=0
  
    

def type_before_code(**arg):
  form=arg['form']
  field=arg['field']
  
  if(form.action == 'new'):
    field['value']='1'
  s=form.s


def enabled_before_code(**arg):
  form=arg['form']
  field=arg['field']
  if(form.action == 'new'):
    field['value']='1'

def access_to_video_bc(form,field):
  if form.action=='new': field['value']=1