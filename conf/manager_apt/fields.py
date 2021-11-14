


def get_fields():
    return [ 
    {
      'name':'login',
      'description':'Логин',
      
      'type':'text',
      'filter_on':1,
      'unique':1,

      'regexp_rules':[
        '/^[a-zA-Z0-9\_\-]+$/','допускаются только латинские буквы, цифры, подчёркивание и тире',
        '/.{12}/','длина логина должна быть не менее 12 символов',
        '/^.{12,20}$/','длина логина должна быть не более 20 символов',
      ],
      'before_code':login_before_code,
      'frontend':{'ajax':{'name':'login','timeout':600}},
      'tab':'main'
    },
    {
      'description':'Пароль',
      'name':'password',
      'type':'password',
      'min_length':8,
      #'before_code':password_before_code,
      'symbols':'123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
      'methods_send':[
        {
          'description':'сохранить',
          'method_send':password_method_send
        }
      ],
      'tab':'main'
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'tab':'main',
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
      'name':'name',
      'description':'ФИО',
      'type':'text',
      'tab':'main',
      'regexp_rules':[
          '/^.+$/','Полное имя обязательно для заполнения',
      ],
      'filter_on':1
    },

    {
       'name':'email',
       'description':'Email',
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
      'before_code':ur_lico_id_before_code,
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
    # {
    #   'name':'type',
    #   'description':'Тип учётной записи',
    #   'type':'select_values',
    #   'tab':'permissions',
    #   'before_code':type_before_code,
    #   'values':[
    #     {'v':1,'d':'Сотрудник компании Анна'},
    #     {'v':2,'d':'Представитель юридического лица'},
    #     {'v':3,'d':'Представитель аптеки'},
    #     {'v':4,'d':'Фармацевт'},
    #   ]
    # },
    {
      'description':'Аптека',
      'name':'apteka_id',
      'tablename':'a',
      'tab':'permissions',
      'table':'apteka',
      'not_process':1,
      'type':'select_from_table',
      'header_field':'ur_address',
      'value_field':'id',
      'before_code':apteka_id_before_code
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
def ur_lico_id_before_code(form,field):
 # form.pre(field)
  if form.manager['type']==2:
    field['where']=f"id in ({','.join(form.manager['ur_lico_list_ids'])})"

  #form.pre(form.manager['ur_lico_list_ids'])

def ur_lico_id_filter_code(form,field,row):
  
  return row["ur_lico_list"]
  
def anna_manager_id_filter_code(form,field,row):
  if row['ma__id']:
    return row['ma__name_f']+' '+row['ma__name_i']+row['ma__name_o']
  else:
    return 'не указан'

def send_mes():
    pass

def password_method_send(new_password):
  send_mes()

def permissions_before_code(**arg):
  form=arg['form']
  field=arg['field']

 
    
def login_before_code(form,field):


  if form.action=='new':
    login_list=form.db.query(
      query="select login from manager where login like %s",
      values=[f"provizor-{form.manager['id']}-%"],
      massive=1
    )

    max_sublogin=0
    for f in login_list:
      sublogin=f.replace(f"provizor-{form.manager['id']}-",'')
      if sublogin.isdigit() and int(sublogin)>max_sublogin:
        max_sublogin=int(sublogin)
        

    
    field['value']='provizor-'+form.manager['id']+'-'+str(max_sublogin+1)
    
  if not(form.action in ('new','insert')):
    field['read_only']=1
  else:
    field['regexp_rules'].append(f"/^provizor-{form.manager['id']}-/")
    field['regexp_rules'].append(f"Логин фармацевта должен начинаться на: provizor-{form.manager['id']}-")


def apteka_id_before_code(form,field):
  #form.pre(f"BEFORE_CODE {form.ov['apteka_id']}")
  if form.action=='edit':
    field['value']=form.ov['apteka_id']


  if form.manager['type'] in (2,3): # Аптеке или юрлицу показываем только их аптеки
    apt_list_ids=form.manager['apt_list_ids']


  

    if len(apt_list_ids)>0:
      field['where']=f"id in ({ ','.join(apt_list_ids) })"
      if form.action=='new':
        field['value']=apt_list_ids[0]
    else:
      field['where']=" 0 "
  #print('v:',form.ov['apteka_id'], ' field:',field)

  if form.manager['type']==1:
    field['autocomplete']=1



def type_before_code(form,field):
  #form=arg['form']
  #field=arg['field']
  
  if(form.action == 'new'):
    field['value']=4
  
  if form.action!='insert':
    field['value']=4
    field['read_only']=1

def access_to_video_bc(form,field):
  if form.action=='new': field['value']=1


def enabled_before_code(**arg):
  form=arg['form']
  field=arg['field']
  if form.action in ('new','insert'): field.read_only=0

  if(form.action == 'new'):
    field['value']='1'