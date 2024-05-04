fields=[ 
    {
      'description':'Тариф',
      'type':'filter_extend_select_from_table',
      'name':'f_tarif',
      'table':'tarif',
      'header_field':'header',
      'value_field':'id',
      'tablename':'t',
      'filter_on':True

    },
    {
      'description':'Менеджер счёта',
      'name':'manager_id',
      'type':'select_from_table',
      'table':'manager',
      'tablename':'m',
      'header_field':'name',
      'value_field':'id',
      'filter_on':1,
      'read_only':1,
      'tab':'main',
    },
    {
      'description':'Номер счёта',
      'type':'text',
      'filter_on':1,
      'name':'number',
      'read_only':1,
      'tab':'main',
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
      'read_only':1,
      'tab':'main',

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
      'description':'Юр.Лицо',
      'name':'c_ur_lico_id',
      'type':'code',
      'tab':'main',

    },
    {
      'description':'Название компании',
      'name':'firm',
      'type':'filter_extend_text',
      'tablename':'u',
      'filter_on':1,

    },


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

    },
    {
      'description':'Компания',
      'name':'firm_c',
      'type':'code',
      'tab':'main',

    },
    {
      'description':'Тариф',
      'type':'code',
      'name':'tarif',
      'tab':'main',

    },

    {
      'description':'Наименование услуги',
      'type':'text',
      'name':'service_name',
      'tab':'main',
    },
    {
      'description':'Сумма счёта',
      'type':'text',
      'filter_type':'range',
      'filter_on':1,
      'name':'summ',
      'tab':'main',
    },
    {
      'description':'Комментарий',
      'type':'textarea',
      'filter_on':1,
      'name':'comment',
      'tab':'main',
    },
    {
        'description':'Дата выставления',
        'type':'date',
        'name':'registered',
        'read_only':1,
        'tab':'main',

    },

    {
        'description':'Оплата производилась',
        'type':'checkbox',
        'name':'paid',
        'read_only':1,
        'filter_on':0,
        'tab':'paid',
        'frontend':{'ajax':{'name':'paid','timeout':100}},
    },
    {
        'description':'Тип оплаты',
        'tab':'paid',
        'name':'paid_type',
        'type':'select_values',
        'values':[
          {'v':1,'d':'Безналичные'},
          {'v':2,'d':'Наличные'},
        ]
    },
    {
        'description':'Дата оплаты',
        'type':'date',
        'name':'paid_date',
        'read_only':1,
        'filter_on':1,
        'hide':True,
        'tab':'paid',

    },
    {
        'description':'Сумма платежа',
        'type':'text',
        'name':'paid_summ',
        'read_only':1,
        'hide':True,
        'tab':'paid',
        'filter_on':1,
    },
]