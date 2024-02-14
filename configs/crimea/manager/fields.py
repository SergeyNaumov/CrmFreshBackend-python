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
        # {
        #   'description':'сохранить и отправить по электронной почте',
        #   'method_send':send_new_password
        # },
        {
          'description':'сохранить и никуда не отправлять',
          'method_send': without_send
        }
      ],
      #'before_code':password_before_code,
      'tab':'main'
    },
    {
      'name':'name',
      'description':'Имя',
      'type':'text',
      'tab':'main',
    },

    {
      'description':'Email',
      'name':'email',
      'type':'filter_extend_text',
      'tablename':'me',
      'db_name':'group_concat(me.email) SEPARATOR ", "'
    },

    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'tab':'main',
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
      'name':'comment',
      'description':'Комментарий',
      'type':'textarea',
      'tab':'main',
    },

    {
      'description':'Зарегистрирован',
      'type':'datetime',
      'name':'registered',
      'read_only':1,
      'tab':'permissions'
    },
    {
      'description':'Доступ к СНТ',
      'add_description':'к новостям, рекламным блокам, заявкам и т.д.',
      'name':'manager_snt',
      'type':'1_to_m',
      'table':'manager_snt',
      'table_id':'id',
      'foreign_key':'manager_id',
      'fields':[
        {
          'description':'СНТ',
          'name':'snt_id',
          'table':'snt',
          'type':'select_from_table',
          'header_field':'header',
          'value_field':'id'
        }
      ]

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
      #'read_only':1
    },
    # {
    #   'description':'Должность',
    #   'type':'text',
    #   'name':'position',
    #   'tab':'hr'
    # },

]


def without_send(form,field,newpass):
    return 

# def send_new_password(form,field,newpass):
#   #print('ov:',form.ov)
#   #print('send: ',field,newpass)
#   if form.ov['email']:
#     send_mes(
#       subject='Вам сгенерирован пароль для входа в систему AннА',
#       to=form.ov['email'],
#       message=f"""
#         Ссылка для входа в ЛК: <a href="https://anna.crm-dev.ru/">https://anna.crm-dev.ru/</a>
#         Логин: {form.ov['login']}<br>
#         Пароль: {newpass}<br>
#         Если появятся вопросы свяжитесь удобным для Вас способом:<br>
#         Телефон: +7-901-993-58-28<br>
#         E-mail: AnnAvoronezh2017@yandex.ru<br>
#       """

#     )
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
def access_role_before_code(form,field):
  if form.manager['permissions'].get('manager_make_change_role'):
    field['read_only']=0
#
def current_role_before_code(form,field):
  field['read_only']=1
  
  if form.manager['permissions'].get('manager_make_change_role'):
    field['read_only']=0
  ids=form.db.query(
    query=f"select role from manager_role where manager_id={form.manager['id']}",
    massive=1,
    str=1
  )
  if len(ids):
    field['where']=f"id in ({','.join(ids)})"
  else:
    field['read_only']=1
  