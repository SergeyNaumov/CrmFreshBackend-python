fields=[ 
    {
      'description':'Номер счёта',
      'type':'text',
      'filter_on':1,
      'name':'number',
      'read_only':1
    },
    {
      'description':'Номер договора',
      'type':'filter_extend_text',
      
      'name':'d_number',
      'db_name':'number',
      'tablename':'d',
      'read_only':1
    },
    {
      'description':'Номер договора',
      'name':'d1_number',
      'type':'code',
      'read_only':1
      # code=>sub{
      #   my $e=shift;
      #   return qq{$form->{old_values}->{d_number}}
      # }
    },
    # {
    #     'description':'Остаток в детализации',
    #     'name':'sum',
    #     'type':'filter_extend_select_from_table',
    #     'table':'bill_part',
    #     'tablename':'bp',
    #     'header_field':'sum',
    #     'filter_type':'range',
    #     'not_process':1,
    # },
    # {
    #   'description':'Номер акта',
    #   'type':'filter_extend_text',
    #   'name':'act_number',
    #   'db_name':'number',
    #   'tablename':'act',
    #   'filter_on':1,
    #   'read_only':1
    # },
    {
          'description':'Реквизиты(ИНН или название)',
          'name':'requis',
          'db_name':'inn',
          'type':'filter_extend_text',
          'tablename':'bcr',
          # filter_code=>sub{
          #   my $s=$_[0]->{str};
          #   #pre($s);
          #   my $out='Не выбрано';
          #   if($s->{bcr__inn} || $s->{bcr__firm}){
          #     $out=qq{$s->{bcr__inn} : $s->{bcr__firm}};
          #   }
          #   return $out;
          # }
    },
    # {
    #     'description':'Реквизиты',
    #     'add_description':'ИНН, Наименование',
    #     'type':'select_from_table',
    #     'table':'buhgalter_card_requisits',
    #     'name':'requisits_id',
    #     'header_field':'firm', #
    #     'value_field':'id',
    #     'not_filter':1,
    #     #regexp=>'^\d+$',
    #     #regexp=>'^\d+$',
    #     'autocomplete':True,
    #     # before_code=>sub{
    #     #     my $e=shift;
    #     #     if($form->{script}=~m{auto_complete}){
    #     #         $e->{out_header}=q{concat(inn,': ',firm, if(edo=1,' ЭДО настроен',''))},
    #     #     }
    #     #     if($form->{old_values}->{user_id}){
    #     #         $e->{autocomplete}=0;
    #     #         $e->{'sql':}.=' WHERE user_id='.$form->{old_values}->{user_id};
    #     #     }
    #     #     #pre($form);
    #     # },
    #     # code=>sub{
    #     #     my $e=shift;
    #     #     $e->{field}.=qq{<br><a href="?config=$form->{config}&id=$form->{id}&action=create_requsits">создать на основании реквизитов в основной карте</a><hr>}
    #     # },
    #     'sql':"SELECT id,if(inn<>'',concat(inn,': ',firm, if(edo=1,' ЭДО настроен','')),firm) header from buhgalter_card_requisits"
    # },
    
    {
      'description':'Юр.Лицо',
      'name':'c_ur_lico_id',
      'type':'code',
      # code=>sub{
      #   my $sth=$form->{dbh}->prepare('SELECT comment from ur_lico where id=?');
      #   $sth->execute($form->{old_values}->{ur_lico_id});
      #   my $comment=$sth->fetchrow;
      #   return qq{<a href="./edit_form.pl?config=ur_lico&action=edit&id=$form->{old_values}->{ur_lico_id}">$form->{old_values}->{ur_lico}}.($comment?' - '.$comment:'').'</a>';
      # }
    },
    {
      'description':'Название компании',
      'name':'firm',
      'type':'filter_extend_text',
      'tablename':'u',
      'filter_on':1,
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   my $out=qq{<a href="./edit_form.pl?config=user&action=edit&id=$s->{u__id}" target="_blank">$s->{u__firm}</a>};
      #   #if(){
      #   $out.=qq{
      #       <div style="margin-top: 10px; margin-bottom: 10px;"><a href="/tools/paid_division_parts.pl?bill_id=$s->{wt__id}" target="_blank">разделения</a></div>
      #     };
      #   #}
      #   return $out;
        
      # }
    },
    # { # поиск по ID компании (из карты клиента)
    #   'description':'Наименование в карте',
    #   'name':'f_user_id',
    #   'type':'filter_extend_select_from_table',
    #   'table':'user',
    #   'header_field':=>'firm',
    #   'tablename':'u',
    #   'value_field':=>'id',
    #   'db_name':'id',
    #   autocomplete=>1,
    #   before_code=>sub{
    #     my $e=shift;
    #     if($form->{script} eq 'admin_table.pl'){
    #       #$e->{not_filter}=1;
    #     }
    #   }
    # },

    {
      'description':'Оплата на юрлицо',
      'type':'filter_extend_select_from_table',
      'sql':"select id,concat(firm,' ',comment) from ur_lico order by header",
      'name':'ur_lico_id',
      'table':'ur_lico',
      'header_field':'firm',
      'value_field':'id',
      'tablename':'ul',
      'db_name':'id',
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   #pre($e);
      #   return $s->{ul__firm}.($s->{ul__comment}?" ($s->{ul__comment})":'')
      # }
    },
    # {
    #   'description':'Детализация',
    #   'name':'more',
    #   'type':'code',
      # code=>sub{

      #   return '' unless($form->{id});
      #   return qq{<a href="https://$form->{CRM_CONST}->{main_domain}/tools/paid_division_parts.pl?bill_id=$form->{id}" target="_blank">посмотреть</a>}
      # }
    #},
    {
      'description':'Компания',
      'name':'firm_c',
      'type':'code',

    },
    {
      'description':'Тариф',
      'type':'code',
      'name':'tarif',

    },



    # {
    #   'name':'edo',
      
    #   'description':'ЭДО',
    #   'type':'code',
    #   # code=>sub{
    #   #   my $e=shift;
    #   #   my $sth=$form->{dbh}->prepare('SELECT group_concat(bcr.firm," настроено с ", ul.firm SEPARATOR "<br>") as str from buhgalter_card_requisits_edo wt left join ur_lico ul on wt.ur_lico_id=ul.id left join buhgalter_card_requisits bcr on wt.buhgalter_card_requisits_id=bcr.id left join user on user.id=bcr.user_id where user.id=?');
    #   #   $sth->execute($form->{old_values}->{user_id});
    #   #   my $edos=$sth->fetchrow();
    #   #   if($edos){
    #   #     $e->{value}='<span style="color:green">'.$edos.'</span>';
    #   #   }else{
    #   #     $e->{value}='<span style="color:brown">ЭДО не настроено</span>';
    #   #   }
        

        
    #   # }
    # },
    # {
    #     'description':'Номер платёжного поручения',
    #     'type':'text',
    #     'name':'payment_order',
    #     'read_only':1
    #     # before_code=>sub{
    #     #     my $e=shift;
    #     #     if($form->{manager}{is_admin}){
    #     #         $e->{read_only}=0;
    #     #     }
    #     # }
    # },
    {
      'description':'Наименование услуги',
      'type':'text',
      'name':'service_name'
    },
    {
      'description':'Сумма',
      'type':'text',
      'filter_type':'range',
      'filter_on':1,
      'name':'summ'
    },
    {
      'description':'Комментарий',
      'type':'textarea',
      'filter_on':1,
      'name':'comment'
    },
    {
        'description':'Дата выставления',
        'type':'date',
        'name':'registered',
        #'filter_on':1,
        
        'read_only':1
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # }
    },
    {
        'description':'Оплата производилась',
        'type':'checkbox',
        'name':'paid',
        'read_only':1,
        'filter_on':1,
    },
    {
        'description':'Дата оплаты',
        'type':'date',
        'name':'paid_date',
        #'filter_on':1,
        
        'read_only':1
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # },
    },

    # {
    #   'description':'Оплачен до',
    #   'type':'date',
    #   'name':'paid_to',
    #   'read_only':1
    # },
    # {
    #   'description':'Группа счёта',
    #   'name':'group_id',
    #   'type':'select_from_table',
    #   'table':'manager_group',
    #   'tablename':'mg',
    #   'header_field':'header',
    #   'value_field':'id',
    #   #'filter_on':1,
    #   'read_only':1
    # },
    # {
    #   'description':'Назначение в детализации',
    #   'name':'bp_comment_id',
    #   'type':'filter_extend_select_from_table',
    #   'tablename':'bpc',
    #   'table':'bill_part_comment',
    #   'header_field':'header',
    #   'value_field':'id',
    #   'db_name':'id',
    # },
    {
      'description':'Менеджер счёта',
      'name':'manager_id',
      'type':'select_from_table',
      'table':'manager',
      'tablename':'m',
      'header_field':'name',
      'value_field':'id',
      'filter_on':1,
      'read_only':1
    },
    # {
    #     'description':'Акты',
    #     'name':'act',
    #     'type':'1_to_m',
    #     'table':'act',
    #     'table_id':'id',
    #     'foreign_key':'bill_id',
    #     'link_edit':'./edit_form.pl?config=act&action=edit&id=<%id%>',
    #     'not_create':1,
    #     'make_delete':0,
    #     'read_only':1,

    #   'fields':[
    #     {'description':'Номер акта','type':'text','name':'number'},
    #     {'description':'Дата','name':'registered','type':'date','read_only':1},
    #     {'description':'Сумма','name':'summ','type':'text'},

    #   ]
    # },
    # {
    #   'description':'Подробнее',
    #   'name':'docs',
    #   'type':'text',
    #   'not_edit':1,
    #   # before_code=>sub{
    #   #   my $e=shift;
    #   #   if($form->{script} eq 'admin_table.pl'){
    #   #     delete($e->{not_process});
    #   #   }
    #   # },
    #   'not_process':1,
    #   # filter_code=>sub{
    #   #   my $s=$_[0]->{str};
    #   #   return &{$form->{run}->{get_more}}($s->{wt__id});
    #   # },
    #   'db_name':'id'
    # }
]