fields=[
{
      'name':'name','description':'Название организации','type':'text','filter_on':1,
      #sphinx=>{'name':'name','type':'text'},
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   return qq{
      #     $s->{wt__name}<br>
      #     <a href="./edit_form.pl?config=addition_users_from_files_users&action=new&from_org_base=$s->{wt__id}" target="_blank">Создать </a>
      #   }
      # }
    },
    {
      'name':'phone','description':'Телефон','type':'text','filter_on':1, 
      #sphinx=>{'name':'phone','type':'text'}
    },
    {
      'name':'email','description':'Email','type':'text','filter_on':1,
      #sphinx=>{'name':'email','type':'text'}
    },
    {
      'name':'address','description':'Адрес','type':'text','filter_on':1,
      #sphinx=>{'name':'address','type':'text'}
      
    },
    {
      'name':'registered','description':'Дата и время добавления','type':'datetime','filter_on':1,
      #sphinx=>{'name':'registered','type':'attr'}, # sort=>'registered'
      #default_off=>1
    },
    {
      'name':'inn','description':'ИНН','type':'text','filter_on':1,
      'filter_type':'eq'
      #sphinx=>{'name':'inn','type':'text'},
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   return qq{
      #     $s->{wt__name}<br>
      #     <a href="/moderator/crm_fresh/tools/search_katalog/protocols.pl?search_from_inn=$s->{wt__inn}" target="_blank">искать в протоколах</a>
      #   }
      # }
    },
    {
      'name':'kpp','description':'КПП','type':'text','filter_on':1,
      #sphinx=>{'name':'kpp','type':'text'}
    },
    {
      'name':'last_participate','description':'Дата и время последнего участия','type':'date','filter_on':1,
      #sphinx=>{'name':'last_participate','type':'attr',sort=>'last_participate'},
      #default_off=>1
    },
    {
      'name':'first_participate','description':'Дата и время первого участия','type':'date','filter_on':1,
      #sphinx=>{'name':'first_participate','type':'attr',sort=>'first_participate'},
      #default_off=>1
    },
    {
      'name':'participate_count','description':'Кол-во участий','type':'text','filter_type':'range','filter_on':1,
      #sphinx=>{'name':'participate_count','type':'attr',sort=>'participate_count'}
    },
    {
      'name':'win_count','description':'Кол-во побед','type':'text','filter_type':'range','filter_on':1,
      #sphinx=>{'name':'win_count','type':'attr',sort=>'win_count'}
    },
    {
      'name':'full_okved','description':'ОКВЭД','type':'text','filter_type':'text','filter_on':1,'db_name':'inn',
      #sphinx=>{'name':'full_okved','type':'text'},
      # filter_code=>sub{
      #   my $s=$_[0]->{str};
      #   return
      #     $s->{full_okved}
      # }
    },
    {
      'name':'region_id','description':'Регион','type':'filter_extend_select_from_table',
      'filter_on':1,
      'table':'region',
      'db_name':'region_id',
      'tablename':'r',
      'filter_table':'region',
      'header_field':'header',
      'value_field':'region_id',
      'where':'country=1',
      #sphinx=>{'name':'region_id','type':'attr'},
    },
    {
      'description':'база СРО',
      'name':'f_sro',
      'db_name':'id',
      'type':'filter_extend_checkbox',
      # sphinx=>{'name':'exists_sro','type':'attr',sort=>'exists_sro'},
      # filter_code=>sub{
      #   my $e=shift;
      #   return ($e->{str}->{rn__id})?'Да':'Нет'
      # }
    },
    {
      'description':'база МЧС',
      'name':'f_mchs',
      'type':'filter_extend_checkbox',
      #sphinx=>{'name':'exists_mchs','type':'attr',sort=>'exists_mchs'},
      'db_name':'id',
      #filter_code=>sub{
      #  my $e=shift;
      #  return ($e->{str}->{rn__mchs})?'Да':'Нет'
      #}
    },
    {
      'description':'база nopriz',
      'name':'f_nopriz',
      'type':'filter_extend_checkbox',
      'db_name':'id',
      #sphinx=>{'name':'exists_nopriz','type':'attr',sort=>'exists_nopriz'},
      #filter_code=>sub{
      #  my $e=shift;
      #  return ($e->{str}->{nopriz__id})?'Да':'Нет'
      #}
    },
    {
      'description':'база Еруз',
      'name':'f_eruz',
      'type':'filter_extend_checkbox',
      'db_name':'id',
      #sphinx=>{'name':'exists_eruz','type':'attr',sort=>'exists_eruz'},
      #filter_code=>sub{
      #  my $e=shift;
      #  return ($e->{str}->{let__id})?'Да':'Нет'
      #}
    },
    {
      'description':'Выручка 2020',
      'type':'filter_extend_text',
      'filter_type':'range',
      'name':'revenue',
      'tablename':'fns',
      #sphinx=>{'name':'fns_revenue','type':'attr',sort=>'fns_revenue'},
      'filter_on':1,
      #not_order=>1,
      # filter_code=>sub{
      #   my $e=shift;return coresubs::get_triade($e->{value});
      # }
    },
    {
      'description':'Прибыль 2020',
      'type':'filter_extend_text',
      'filter_type':'range',
      'name':'profit',
      'tablename':'fns',
#      sphinx=>{'name':'fns_profit','type':'attr',sort=>'fns_profit'},
      'filter_on':1,
      #not_order=>1,
      # filter_code=>sub{
      #   my $e=shift;return coresubs::get_triade($e->{value});
      # }
    },
    {
      'description':'Баланс 2020',
      'type':'filter_extend_text',
      'filter_type':'range',
      'name':'balance',
      'tablename':'fns',
#      sphinx=>{'name':'fns_balance','type':'attr',sort=>'fns_balance'},
      'filter_on':1,
      #not_order=>1,
#      filter_code=>sub{
#        my $e=shift;return coresubs::get_triade($e->{value});
#      }
    }
]