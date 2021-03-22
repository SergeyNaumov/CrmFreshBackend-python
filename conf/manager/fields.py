
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
        '/^[a-zA-Z0-9\-_@\/]+$/','только символы: a..z,A..Z, 0-9, _, -, @, .'
      ],
      'tab':'main'
    },
    {
      'description':'Аватар',
      'type':'file',
      'name':'photo',
       'filedir':'./files/manager',
      # . 'accept':'doc,.docx,.xml,application/msword,application/vnd.openxm
      # 'accept':'image/png, image/jpeg',
       'accept':'image/*',
       #'crops':1,
       'resize':[
        {
          'description':'Горизонтальное фото',
          'file':'<%filename_without_ext%>_mini1.<%ext%>',
          'size':'256x256',
          'quality':'100'
        },
      ],
       'tab':'main'
    },
    # {
    #   'name':'login_tel',
    #   'description':'Логин для IP-телефонии',
    #    'type':'text',
    #    'tab':'main'
    # },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
       'tab':'main',
       'regexp_rules':[
        '^(\+7\d{10})?$/','Если указывается телефон, он должен быть в формате +7XXXXXXXXXX',
      ],
      'replace_rules':[
        #'/^[87]/':'+7',
        #'/[^\d\+]+/':'',
        #'/^([^87\+])/':'+7$1',
      ],
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
      'description':'Добавочный',
      'type':'text',
      'name':'phone_dob',
      'tab':'main',
      'regexp':'^\d*$'
    },
    {
      'description':'Мобильный телефон',
      'type':'text',
      'name':'mobile_phone',
       'tab':'main',
       'regexp_rules':[
            '/^(\+7\d{10})?$/',
            'Если указывается телефон, он должен быть в формате +7XXXXXXXXXX',
        ],
      'replace_rules':[
        #'/^[87]/':'+7',
        #'/[^\d\+]+/':'',
        #'/^([^87\+])/':'+7$1',
      ],
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
      'description':'Вкл',
      'name':'enabled',
      'type':'checkbox',
       'tab':'main'
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
    {
      'description':'Уволен',
      'type':'checkbox',
      'name':'gone',
       'tab':'permissions'
    },
    {
      'description':'Текущая роль',
      'type':'select_from_table',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',
      'not_filter':'1',
      'name':'current_role',
      # before_code=>sub{
      #   my $e=shift;
      #   if(!$form->{is_admin}){
      #     $e->{where}=qq{id in (select role from manager_role where manager_id=$form->{manager}->{id}) }
      #   }
      #   else{
      #     #$e->{autocomplete}=1
      #   }
      # },
       'tab':'permissions',

    },
    {
      'description':'Доступные роли',
      'name':'manager_role',
      'type':'1_to_m',
      'table':'manager_role',
      'table_id':'id',
      'foreign_key':'manager_id',
      'fields':[
            {
              'description':'Роль',
              'name':'role',
              'type':'select_from_table',
              'table':'manager',
              'header_field':'name',
              'value_field':'id'
            }
       ],
       'tab':'permissions'
    },

    # {
    #    'name':'group_id',
    #    'description':'Группа менеджера',
    #    'type':'select_from_table',
    #   'table':'manager_group',
    #   'tree_use':1,
    #   'tablename':'mg',
    #   'header_field':'header',
    #   'value_field':'id',
    #    'tab':'permissions',
    #   # filter_code=>sub{
    #   #   my $s=$_[0]->{str};
    #   #   return qq{<a href="./edit_form.pl?config=manager_group&action=edit&id=$s->{mg__id}" target="_blank">$s->{mg__header}</a>}
    #   # }
    # },

    {
      # before_code=>sub{
      #         my $e=shift;                    
      #         #$e->{read_only}=1 unless($form->{manager}->{permissions}->{make_change_permissions});
      # },
      'description':'Права менеджеров',
      'type':'multiconnect',
      'tree_use':1,
      'tree_table':'permissions',
      'name':'permissions',
      'relation_table':'permissions',
      'relation_save_table':'manager_permissions',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'manager_id',
      'relation_save_table_id_relation':'permissions_id',
      'tab':'permissions'
    },

]
