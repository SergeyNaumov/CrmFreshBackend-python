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
    {
      'description':'Номер акта',
      'type':'filter_extend_text',
      'name':'act_number',
      'db_name':'number',
      'tablename':'act',
      'filter_on':1,
      'read_only':1
    },
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
    {
        'description':'Реквизиты',
        'add_description':'ИНН, Наименование',
        'type':'select_from_table',
        'table':'buhgalter_card_requisits',
        'name':'requisits_id',
        'header_field':'firm', # 
        'value_field':'id',
        'not_filter':1,
        #regexp=>'^\d+$',
        #regexp=>'^\d+$',
        'autocomplete':1,
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{script}=~m{auto_complete}){
        #         $e->{out_header}=q{concat(inn,': ',firm, if(edo=1,' ЭДО настроен',''))},
        #     }
        #     if($form->{old_values}->{user_id}){
        #         $e->{autocomplete}=0;
        #         $e->{'sql':}.=' WHERE user_id='.$form->{old_values}->{user_id};
        #     }
        #     #pre($form);
        # },
        # code=>sub{
        #     my $e=shift;
        #     $e->{field}.=qq{<br><a href="?config=$form->{config}&id=$form->{id}&action=create_requsits">создать на основании реквизитов в основной карте</a><hr>}
        # },
        'sql':"SELECT id,if(inn<>'',concat(inn,': ',firm, if(edo=1,' ЭДО настроен','')),firm) header from buhgalter_card_requisits"
    },
    
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
    {
        'description':'Номер платёжного поручения',
        'type':'text',
        'name':'payment_order',
        'read_only':1
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # }
    },
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
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # },
        'filter_on':1,
      # after_save=>sub{
      #   my $e=shift;
      #   my %to=();
      #   #pre($form->{manager});
      #   #pre([
      #   #  $form->{old_values}->{m_id},
      #   #  $form->{old_values}->{m_email},
      #   #]);
      #   my $ov=$form->{old_values};
        
      #   my $own=core_strateg::get_owner(
      #     cur_manager=>{
      #       id=>$ov->{m_id},
      #       group_path=>$ov->{m_group_path},
      #       group_id=>$ov->{m_group_id},
      #     },
      #     connect=>$form->{dbh}
      #   );
        
      #   if(!$ov->{paid} && $e->{value}){
      #     if($ov->{m_email} && $ov->{m_id}!=$form->{manager}->{id}){
      #       $to{$ov->{m_email}}=1
      #     }
      #     if($own->{email} && $own->{id}!=$form->{manager}->{id}){
      #       $to{$own->{email}}=1
      #     }
      #     my $to_str=join(',',keys(%to));
      #     if($to_str){
      #         send_mes({
      #           to=>$to_str,
      #           subject=>qq{$ov->{firm} Счёт №$ov->{number} оплачен},
      #           message=>qq{
      #             Для компании <a href="http://$ENV{HTTP_HOST}/edit_form.pl?config=user&action=edit&id=$ov->{user_id}">$ov->{firm}</a><br>
      #             <a href="http://$ENV{HTTP_HOST}/edit_form.pl?config=bill&action=edit&id=$form->{id}">Счёт №$ov->{number}</a><br>
      #             Сумма: $form->{new_values}->{summ}<br>
      #             дата оплаты: $form->{new_values}->{paid_date}
      #           }
      #         })
      #     }
      #     if($ov->{requisits_id}){
      #       my $sth=$form->{dbh}->prepare('SELECT edo,edo_id,transfer_1c from buhgalter_card_requisits where id=?');
      #       $sth->execute($ov->{requisits_id});
      #       my $edo=$sth->fetchrow_hashref();
            
      #       if($edo->{edo} && $edo->{edo_id} && !$edo->{transfer_1c}){
      #         send_mes({
      #           to=>'krushin@digitalstrateg.ru,svetlanakrash@digitalstrateg.ru',
      #           subject=>qq{$ov->{firm} добавление в 1С},
      #           message=>qq{
      #             Для компании <a href="http://$ENV{HTTP_HOST}/edit_form.pl?config=user&action=edit&id=$ov->{user_id}">$ov->{firm}</a><br>
      #             <a href="http://$ENV{HTTP_HOST}/edit_form.pl?config=bill&action=edit&id=$form->{id}">Счёт №$ov->{number}</a><br>
      #             ID в ЭДО = $edo->{edo_id}
      #           }
      #         });
      #         my $sth=$form->{dbh}->prepare('UPDATE buhgalter_card_requisits set transfer_1c=1 where id=?');
      #         $sth->execute($ov->{requisits_id});
      #       }
      #     }
      #   }
      # },
      # code=>sub{
      #   my $e=shift;
      #   if($form->{old_values}->{avance_fact_number}){
      #     $e->{field}.=qq{
      #       <hr>
      #       <b>Авансовая счёт-фактура №$form->{old_values}->{avance_fact_number}</b><br>
      #       с печатями: <a href="/tools/load_document.pl?type=av_fact&bill_id=$form->{id}&format=doc">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id=$form->{id}&format=pdf">pdf</a><br>
      #       без печатей: <a href="/tools/load_document.pl?type=av_fact&bill_id=$form->{id}&format=doc&without_print=1">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id=$form->{id}&format=pdf&&without_print=1">pdf</a><br>
      #       <hr>
      #     }
      #   }
      #   return $e->{field};
      # }
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

    {
      'description':'Оплачен до',
      'type':'date',
      'name':'paid_to',
      
      
      'read_only':1
      #   before_code=>sub{
      #       my $e=shift;
      #       if($form->{manager}{is_admin}){
      #           $e->{read_only}=0;
      #       }
      #   },
      # code=>sub{
      #   my $e=shift; my $max;
      #   if(my $user_id=$form->{old_values}->{user_id}){
      #     my $sth=$form->{connects}->{strateg_read}->prepare(q{
      #     SELECT
      #       max(paid_to)
      #     FROM
      #       docpack dp
      #       join bill b ON (b.docpack_id=dp.id)
      #     WHERE
      #       dp.user_id=?
      #     });
      #     $sth->execute($user_id);
      #     $max=$sth->fetchrow;
          
      #   }
      #   #pre($form->{old_values});
      #   if($max){
      #     $e->{field}.=qq{ <small>максимальная дата оплаты для данной компании: $max </small>}
      #   }
      #   return $e->{field};
      # }
    },
    {
      'description':'Группа счёта',
      'name':'group_id',
      'type':'select_from_table',
      'table':'manager_group',
      'tablename':'mg',
      'header_field':'header',
      'value_field':'id',
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
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # },
    },
    {
        'description':'Акты',
        'name':'act',
        'type':'1_to_m',
        'table':'act',
        'table_id':'id',
        'foreign_key':'bill_id',
        'link_edit':'./edit_form.pl?config=act&action=edit&id=<%id%>',
        'not_create':1,
        'make_delete':0,
        'read_only':1,
        # before_code=>sub{
        #     my $e=shift;
        #     if($form->{manager}{is_admin}){
        #         $e->{read_only}=0;
        #     }
        # },
        # before_code=>sub{
        #     my $e=shift;
        #     $e->{make_delete}=1 if($form->{manager}->{permissions}->{admin_paids} || $form->{manager}->{login} eq 'admin');
        #     if(
        #         ($form->{manager}->{permissions}->{admin_paids} || $form->{manager}->{login} eq 'admin')
        #         ||
        #         $form->{old_values}->{paid}
        #         ||
        #         $form->{old_values}->{manager_id}==$form->{manager}->{id}
        #     ){
        #     $e->{not_create}=0;
        #     $e->{read_only}=0;
        #     $e->{link_add}=qq{./edit_form.pl?config=act&action=new&bill_id=$form->{id}};
        #     #pre('ok');
        #     }
            
        # },
      'fields':[
        {
          'description':'Номер акта','type':'text','name':'number',
          # slide_code=>sub{
          #   my $e=shift; my $v=shift;
          #   my $out=qq{
          #     <b>Акт:</b> $v->{number__value}<br>
          #     с печатями: <a href="/tools/load_document.pl?type=act&act_id=$v->{id}&format=doc">doc</a> | <a href="/tools/load_document.pl?type=act&act_id=$v->{id}&format=pdf">pdf</a><br>
          #     без печатей: <a href="/tools/load_document.pl?type=act&act_id=$v->{id}&format=doc&without_print=1">doc</a> | <a href="/tools/load_document.pl?type=act&act_id=$v->{id}&format=pdf&without_print=1">pdf</a>
          #   };
          #   my $without_nds_dat=$form->{old_values}->{without_nds_dat};
          #   $without_nds_dat=~s{[^\d]}{}g;
          #   my $registered=$v->{registered__value};
          #   $registered=~s{[^\d]}{}g;
          #   $without_nds_dat+=0;
          #   #pre({
          #   #  with_nds=>$form->{old_values}->{with_nds},
          #   #  without_nds_dat=>$without_nds_dat,
          #   #  registered=>$registered
          #   #});
            
          #   if($form->{old_values}->{with_nds} && (!$without_nds_dat || $registered<$without_nds_dat) ){
          #     $out.=qq{
          #       <hr>
          #       <b>Счёт-фактура:</b> $v->{number__value}<br>
          #       с печатями: <a href="/tools/load_document.pl?type=fact&act_id=$v->{id}&format=doc">doc</a> | <a href="/tools/load_document.pl?type=fact&act_id=$v->{id}&format=pdf">pdf</a><br>
          #       без печатей: <a href="/tools/load_document.pl?type=fact&act_id=$v->{id}&format=doc&without_print=1">doc</a> | <a href="/tools/load_document.pl?type=fact&act_id=$v->{id}&format=pdf&without_print=1">pdf</a><br>
          #     };
          #   }
          #   return $out;
            
          # }
        },
        {'description':'Дата','name':'registered','type':'date','read_only':1},
        {'description':'Сумма','name':'summ','type':'text'},

      ]
    },
    {
      'description':'Подробнее',
      'name':'docs',
      'type':'text',
      'not_edit':1,
      # before_code=>sub{
      #   my $e=shift;
      #   if($form->{script} eq 'admin_table.pl'){
      #     delete($e->{not_process});
      #   }
      # },
      'not_process':1,
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   return &{$form->{run}->{get_more}}($s->{wt__id});
      # },
      'db_name':'id'
    }
]