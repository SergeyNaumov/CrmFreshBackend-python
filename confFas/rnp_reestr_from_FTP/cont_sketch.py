$form={
  title => 'Реестр РНП',
  work_table => 'rnp_reestr_from_FTP',
  work_table_id => 'id',
  read_only=>1,
  not_create=>1,
  make_delete=>0,
  #explain=>1,
  events=>{
    permissions=>sub{
      $form->{dbh}=$form->{connects}->{protocols_records};
      if($form->{action} eq 'go_transfer'){
        go_transfer::run($form);
        exit;
      }
      my $i=1;
      foreach my $f (@{$form->{fields}}){
        #$f->{description}="$i $f->{description}"; $i++;
        if(undef($f->{filter_on})){
          $f->{filter_on}=1;
        }
        
      }
    }
  },
  run=>{
    get_triade=>sub{ # бьёт число на триады
      my $s=shift; my $dr;
      $s=~s/(\.\d+)$//;
      #if($s=~m/(\.\d+)$/){
      #  $dr=$1; $s=~s/(\.\d+)$//;
      #}
      my $sr=join('',reverse(split //,$s));
      $sr=~s/(\d{3})/$1\ /g;
      return join('',reverse(split //,$sr)).$dr;
    }
  },
  search_links=>[
    {link=>'./admin_table.pl?config=rnp_reestr_from_FTP_assignment',description=>'Список менеджеров для распределения',target=>'_blank'},
    {link=>'./admin_table.pl?config=rnp_reestr_from_FTP_assignment_otk',description=>'Для распределения ОТК',target=>'_blank'},
    {link=>'./admin_table.pl?config=rnp_reestr_from_FTP_assignment_dt',description=>'Для распределения ДТ',target=>'_blank'},
  ],
  plugins => [
     'find::to_xls2'
  ],
  QUERY_SEARCH_TABLES=>[
    {table=>'rnp_reestr_from_FTP',alias=>'wt'},
    {table=>'rosexport.managers',alias=>'m',link=>'wt.manager_id=m.id',left_join=>1},
    {table=>'rosexport.users',alias=>'u',link=>'wt.user_id=u.id',left_join=>1},
    {table=>'rosexport.managers',alias=>'m_otk',link=>'wt.manager_otk=m_otk.id',left_join=>1,for_fields=>['manager_otk']},
    {table=>'rosexport.managers',alias=>'m_dt2',link=>'wt.manager_dt2=m_dt2.id',left_join=>1,for_fields=>['manager_dt2']},
    {table=>'rosexport.users',alias=>'u_otk',link=>'wt.manager_otk_users_id=u_otk.id',left_join=>1,for_fields=>['manager_otk_is_double']},
    {table=>'rosexport.users',alias=>'u_dt2',link=>'wt.manager_dt2_users_id=u_dt2.id',left_join=>1,for_fields=>['manager_dt2_is_double']},
  ],
  fields=>[
    {
      description=>'Время добавления в базу',
      type=>'datetime',
      name=>'registered',
      default_off=>1
    },
    {
      description=>'Время распределения',
      type=>'datetime',
      name=>'time_manager_set',
      default_off=>1
    },
    {
      description=>'Менеджер',
      type=>'filter_extend_select_from_table',
      table=>'rosexport.managers',
      tablename=>'m',
      name=>'manager_id',
      header_field=>'name',
      value_field=>'id'
    },
    {
      description=>'Дубль',
      name=>'is_double',
      type=>'checkbox',
      filter_code=>sub{
        my $e=shift;
        my $str=$e->{str};
        return qq{
          $e->{value}<br>
          <a href="./edit_form.pl?config=users_card&action=edit&id=$str->{u__id}" target="_blank">$str->{u__firm}</a>
        }
      }
    },
    {description=>'Реестровый номер',type=>'text',name=>'reestr_number'},
    {description=>'Дата подтверждения',type=>'date',name=>'approve_date',default_off=>1},
    {
      description=>'Статус примечания',type=>'select_values',name=>'note_status',
      values=>[
        {v=>1,d=>'Отказ во включение в РНП'},
        {v=>2,d=>'Опубликована'},
        {v=>3,d=>'Заявка на исключение сведений'},
        {v=>4,d=>'Информация исключена из РНП на время судебного разбирательства'},
        {v=>5,d=>'Информация исключена из РНП. Архив'},
      ]
    },
    {
      description=>'ФЗ',name=>'law_type',type=>'select_values',
      values=>[
        {v=>1,d=>'44 ФЗ'},
        {v=>2,d=>'223 ФЗ'},
        {v=>3,d=>'615 ФЗ'},
      ]
    },
    {description=>'Номер закупки',type=>'text',name=>'purchase_number'},
    {description=>'Объект закупки',type=>'',name=>'purchase_object'},
    {
      description=>'Начальная цена контракта',type=>'text',filter_type=>'range',name=>'start_price',
      filter_code=>sub{
        my $e=shift;
        return &{$form->{run}->{get_triade}}($e->{value});
      }
    },
    {description=>'ИНН организации',type=>'text',name=>'client_inn'},
    {description=>'Название организации',type=>'text',name=>'client_name'},
    {description=>'Город организации',type=>'text',name=>'client_address'},
    {description=>'ИНН заказчика',type=>'text',name=>'customer_inn'},
    {description=>'КПП заказчика',type=>'text',name=>'customer_kpp'},
    {description=>'Название заказчика',type=>'text',name=>'customer_name'},
    {description=>'Адрес заказчика',type=>'text',name=>'customer_address'},
    {description=>'fas код',type=>'text',name=>'fas_code'},
    {description=>'fas имя',type=>'text',name=>'fas_name'},
    {description=>'Город УФАС',type=>'text',name=>'fas_region'},
    {
      description=>'Причина',type=>'select_values',name=>'include_reason',
      values=>[
        {v=>1,d=>'Уклонение победителя от заключения контракта'},
        {v=>2,d=>'Уклонение единственного участника от заключения контракта'},
        {v=>3,d=>'Уклонение победителя от заключения контракта'},
        {v=>4,d=>'Расторжение контракта'},
        {v=>5,d=>'Отмена контракта'},
        {v=>6,d=>'Решение суда по отмене договора'},
      ]
    },
    {
      description=>'Причина1',
      name=>'reason_1',
      type=>'text'
    },
    {
      description=>'Причина2',
      name=>'reason_2',
      type=>'text'
    },
    {
      description=>'Менеджер ОТК',
      name=>'manager_otk',
      type=>'select_from_table',
      table=>'rosexport.managers',
      header_field=>'name',
      value_field=>'id',
      filter_on=>0,
      tablename=>'m_otk'
    },
    {
      description=>'Дубль (при распределении на ОТК)',
      name=>'manager_otk_is_double',
      filter_on=>0,
      type=>'checkbox',
      filter_code=>sub{
        my $e=shift;
        my $str=$e->{str};
        my $firm=$str->{u_otk__firm} || '---';
        return qq{
          $e->{value}<br>
          <a href="./edit_form.pl?config=users_card&action=edit&id=$str->{u_otk__id}" target="_blank">$firm</a>
        }
      }
    },
    {
      description=>'Момент распределения ОТК',
      name=>'manager_otk_moment',
      type=>'datetime',
      filter_on=>0,
      default_off=>1,

    },
    {
      description=>'Менеджер ДТ2',
      name=>'manager_dt2',
      type=>'select_from_table',
      table=>'rosexport.managers',
      header_field=>'name',
      value_field=>'id',
      filter_on=>0,
      tablename=>'m_dt2'
    },
    {
      description=>'Дубль (при распределении на ДТ2)',
      name=>'manager_dt2_is_double',
      filter_on=>0,
      type=>'checkbox',
      filter_code=>sub{
        my $e=shift;
        my $str=$e->{str};
        my $firm=$str->{u_dt2__firm} || '---';
        return qq{
          $e->{value}<br>
          <a href="./edit_form.pl?config=users_card&action=edit&id=$str->{u_dt2__id}" target="_blank">$firm</a>
        }
      }
    },
    {
      description=>'Момент распределения ДТ2',
      name=>'manager_dt2_moment',
      type=>'datetime',
      filter_on=>0,
      default_off=>1,

    },
    # {
    #   description=>'Компания при распределении на ОТК',
    #   name=>'manager_otk_users_id',
    #   type=>'filter_extend_text',
    #   db_name=>'firm',
    #   filter_on=>0,
    #   tablename=>'u_otk'
    # },
    # {
    #   description=>'',
    #   name=>'',
    #   type=>''
    # },
  ]
};
