def information_before_code(form,field):
  backend_base=form.s.config.get('BackendBase')
  #form.pre(backend_base)
  if not(form.id) or not(form.ov):
    return

  ov=form.ov
  field['after_html']=f"<a href='/edit_form/user/{ov['user_id']}' target='_blank'>{ov['firm']}</a><br>"+\
  f"Тариф: {ov['tarif_header']}<br><br>"+\
  f"Договор <a href='/edit_form/bill/{ov['bill_id']}' target='_blank'>№{ov['dogovor_number']} от {ov['dogovor_registered']}</a><br>"+\
  f"""<div style="margin-left: 20px; margin-bottom: 10px;">
    без печатей: <a href="{backend_base}/docpack/load-dogovor/{ov['docpack_id']}/doc/0">doc</a> | <a href="{backend_base}/docpack/load-dogovor/{ov['docpack_id']}/pdf/0">pdf</a><br>
    с печатями: <a href="{backend_base}/docpack/load-dogovor/{ov['docpack_id']}/doc/1">doc</a> | <a href="{backend_base}/docpack/load-dogovor/{ov['docpack_id']}/pdf/1">pdf</a>
  </div>
  """+\
  f"Счёт <a href='/edit_form/bill/{ov['bill_id']}' target='_blank'>№{ov['bill_number']} от {ov['bill_registered']}</a><br>"+\
  f"""<div style="margin-left: 20px">
    без печатей: <a href="{backend_base}/docpack/load-bill/{ov['docpack_id']}/{ov['bill_id']}/doc/0">doc</a> | <a href="{backend_base}/docpack/load-bill/{ov['docpack_id']}/{ov['bill_id']}/pdf/0">pdf</a><br>
    с печатями: <a href="{backend_base}/docpack/load-bill/{ov['docpack_id']}/{ov['bill_id']}/doc/1">doc</a> | <a href="{backend_base}/docpack/load-bill/{ov['docpack_id']}/{ov['bill_id']}/pdf/1">pdf</a>
  </div><br>
  """+\
  f"Акт №{ov['number']} от {ov['registered']}</a><br>"+\
  f"""<div style="margin-left: 20px">
    без печатей: <a href="{backend_base}/docpack/load-act/{ov['docpack_id']}/{form.id}/doc/0">doc</a> | <a href="{backend_base}/docpack/load-act/{ov['docpack_id']}/{form.id}/pdf/0">pdf</a><br>
    с печатями: <a href="{backend_base}/docpack/load-act/{ov['docpack_id']}/{form.id}/doc/1">doc</a> | <a href="{backend_base}/docpack/load-act/{ov['docpack_id']}/{form.id}/pdf/1">pdf</a>
  </div><br><br>
  """

def firm_filter_code(form,field,row):
  return f'<a href="/edit_form/{row["u__id"]}" target="_blank">{row["u__firm"]}</a>'

fields=[ 
    {
      'name':'information',
      'type':'code',
      'before_code':information_before_code
    },
    {
      'description':'Организация',
      'type':'filter_extend_text',
      'tablename':'u',
      'name':'firm',
      'filter_code':firm_filter_code,
      'filter_on':1
    },
    {
      'description':'ИНН',
      'type':'filter_extend_text',
      'autocomplete':1,
      'tablename':'u',
      'name':'inn',
      'filter_on':1
    },
    {
      'description':'Тариф',
      'type':'filter_extend_text',
      'tablename':'t',
      'name':'tarif',
      'db_name':'header',
      'filter_on':1
    },
    {
      'description':'Юр. лицо',
      'type':'filter_extend_text',
      'tablename':'ul',
      'name':'ur_lico',
      'db_name':'firm',
      'filter_on':1
    },
    {
      'description':'Менеджер акта',
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
        'description':'Номер акта',
        'type':'text',
        'name':'number',
        'read_only':1,
        'filter_on':1,
        'tab':'paid',
    },
    {
        'description':'Сумма акта',
        'type':'text',
        'name':'summ',
        'read_only':1,
        'filter_on':1,
        'tab':'paid',
    },
    {
        'description':'Дата акта',
        'type':'date',
        'name':'registered',
        'read_only':1,
        'filter_on':1,
        'tab':'registered',
    },
    # {
    #   'description':'Номер счёта',
    #   'type':'text',
    #   'filter_on':1,
    #   'name':'number',
    #   'read_only':1,
    #   'tab':'main',
    # },
    # {
    #   'description':'Номер договора',
    #   'type':'filter_extend_text',
      
    #   'name':'d_number',
    #   'db_name':'number',
    #   'tablename':'d',
    #   'read_only':1
    # },
    # {
    #   'description':'Номер договора',
    #   'name':'d1_number',
    #   'type':'code',
    #   'read_only':1,
    #   'tab':'main',

    # },

    # {
    #       'description':'Реквизиты(ИНН или название)',
    #       'name':'requis',
    #       'db_name':'inn',
    #       'type':'filter_extend_text',
    #       'tablename':'bcr',
    #       # filter_code=>sub{
    #       #   my $s=$_[0]->{str};
    #       #   #pre($s);
    #       #   my $out='Не выбрано';
    #       #   if($s->{bcr__inn} || $s->{bcr__firm}){
    #       #     $out=qq{$s->{bcr__inn} : $s->{bcr__firm}};
    #       #   }
    #       #   return $out;
    #       # }
    # },
    
    # {
    #   'description':'Юр.Лицо',
    #   'name':'c_ur_lico_id',
    #   'type':'code',
    #   'tab':'main',

    # },
    # {
    #   'description':'Название компании',
    #   'name':'firm',
    #   'type':'filter_extend_text',
    #   'tablename':'u',
    #   'filter_on':1,

    # },


    # {
    #   'description':'Оплата на юрлицо',
    #   'type':'filter_extend_select_from_table',
    #   'sql':"select id,concat(firm,' ',comment) from ur_lico order by header",
    #   'name':'ur_lico_id',
    #   'table':'ur_lico',
    #   'header_field':'firm',
    #   'value_field':'id',
    #   'tablename':'ul',
    #   'db_name':'id',

    # },
    # {
    #   'description':'Компания',
    #   'name':'firm_c',
    #   'type':'code',
    #   'tab':'main',

    # },
    # {
    #   'description':'Тариф',
    #   'type':'code',
    #   'name':'tarif',
    #   'tab':'main',

    # },

    # {
    #   'description':'Наименование услуги',
    #   'type':'text',
    #   'name':'service_name',
    #   'tab':'main',
    # },
    # {
    #   'description':'Сумма',
    #   'type':'text',
    #   'filter_type':'range',
    #   'filter_on':1,
    #   'name':'summ',
    #   'tab':'main',
    # },
    # {
    #   'description':'Комментарий',
    #   'type':'textarea',
    #   'filter_on':1,
    #   'name':'comment',
    #   'tab':'main',
    # },
    # {
    #     'description':'Дата выставления',
    #     'type':'date',
    #     'name':'registered',
    #     'read_only':1,
    #     'tab':'main',

    # },

    # {
    #     'description':'Оплата производилась',
    #     'type':'checkbox',
    #     'name':'paid',
    #     'read_only':1,
    #     'filter_on':0,
    #     'tab':'paid',
    #     'frontend':{'ajax':{'name':'paid','timeout':100}},
    # },
    # {
    #     'description':'Дата оплаты',
    #     'type':'date',
    #     'name':'paid_date',
    #     'read_only':1,
    #     'filter_on':1,
    #     'hide':True,
    #     'tab':'paid',

    # },

]