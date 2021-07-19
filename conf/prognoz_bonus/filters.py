import os.path



def get_filters():
  return [ 
    {
      'description':'Юридическое лицо',
      'name':'ur_lico_id',
      'type':'select_from_table',
      'table':'ur_lico',
      'tablename':'u',
      'header_field':'header',
      'value_field':'id',
      'autocomplete':1,
      'filter_on':1,
      'filter_code':ur_lico_id_filter_code
    },
    {
      'description':'Период',
      'name':'period_id',
      'tablename':'pbp',
      'filter_on':1,
      'type':'filter_extend_select_values',
      'filter_code':period_id_filter_code,
      'before_code':period_id_before_code,

    },
    {
      'description':'Маркетинговое мероприятие',
      'name':'action_id',
      'type':'select_from_table',
      'table':'action',
      'tablename':'a',
      'header_field':'concat(header," (",date_start,"..",date_stop,")")',
      'value_field':'id',
      #'where':'date_stop>=curdate()',
      #'autocomplete':1,
      #'autocomplete_start_loaded':1,
      'filter_code':action_id_filter_code,
      'filter_on':1
    },


  ]

def ur_lico_id_filter_code(form,field,row):
  return f'''
    {row['u__header']}<br>
    <small><a href="/edit-form/{form.work_table}/{row['wt__id']}" target="_blank">посмотреть прогнозный бонус</a></small>'''

def action_id_filter_code(form,field,row):
  return f'{row["a__header"]} ({row["a__date_start"]}..{row["a__date_stop"]})'

def period_id_filter_code(form,field,row):
  #form.pre(row)
  return f'{row["pbp__year"]}, {row["pbp__querter"]} квартал'
def period_id_before_code(form,field):
    field['values']=form.db.query(
      query="select id v,concat(year,' ',querter,' квартал') d from prognoz_bonus_period order by date_begin"
    )
