def information_before_code(form,field):
  return ''


def firm_filter_code(form,field,row):
  return f'<a href="/edit_form/{row["u__id"]}" target="_blank">{row["u__firm"]}</a>'

fields=[ 
    {
      'name':'information',
      'type':'code',
      'before_code':information_before_code
    },
    {
      'description':'№акта',
      'type':'text',
      'name':'number',
      'filter_on':1
    },
    {
      'description':'data',
      'type':'date',
      'name':'dat',
      'filter_on':1
    },
    {
      'description':'ИНН',
      'type':'text',
      'autocomplete':1,
      #'tablename':'u',
      'name':'inn',
      'filter_on':1
    },


    {
      'description':'№ договора',
      'type':'text',
      'name': 'dogovor_number',
      'filter_on':1
    },
    {
      'description':'Услуга',
      'type':'text',
      'name': 'service',
      'filter_on':1
    },
    {
      'description':'Сумма',
      'type':'text',
      'name': 'summa',
      'filter_on':1
    },
#    {
    #   'description':'Организация',
    #   'type':'filter_extend_text',
    #   'tablename':'u',
    #   'name':'firm',
    #   'filter_code':firm_filter_code,
    #   'filter_on':1
    # },
    # {
    #   'description':'ИНН',
    #   'type':'filter_extend_text',
    #   'autocomplete':1,
    #   'tablename':'u',
    #   'name':'inn',
    #   'filter_on':1
    # },
    # {
    #   'description':'Тариф',
    #   'type':'filter_extend_text',
    #   'tablename':'t',
    #   'name':'tarif',
    #   'db_name':'header',
    #   'filter_on':1
    # },
    # {
    #   'description':'Юр. лицо',
    #   'type':'filter_extend_text',
    #   'tablename':'ul',
    #   'name':'ur_lico',
    #   'db_name':'firm',
    #   'filter_on':1
    # },
    # {
    #   'description':'Менеджер акта',
    #   'name':'manager_id',
    #   'type':'select_from_table',
    #   'table':'manager',
    #   'tablename':'m',
    #   'header_field':'name',
    #   'value_field':'id',
    #   'filter_on':1,
    #   'read_only':1,
    #   'tab':'main',
    # },
    # {
    #     'description':'Номер акта',
    #     'type':'text',
    #     'name':'number',
    #     'read_only':1,
    #     'filter_on':1,
    #     'tab':'paid',
    # },
    # {
    #     'description':'Сумма акта',
    #     'type':'text',
    #     'name':'summ',
    #     'read_only':1,
    #     'filter_on':1,
    #     'tab':'paid',
    # },
    # {
    #     'description':'Дата акта',
    #     'type':'date',
    #     'name':'registered',
    #     'read_only':1,
    #     'filter_on':1,
    #     'tab':'registered',
    # },


]