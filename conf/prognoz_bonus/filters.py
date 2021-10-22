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
      'filter_code':ur_lico_id_filter_code,
      'before_code':ur_lico_id_before_code
    },
    {
      'description':'Выводить сводные данные',
      'type':'checkbox',
      'value':1,
      'name':'out_action',
      'filter_on':1,

      'before_code':out_action_before_code,
      'not_process':1
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
def ur_lico_id_before_code(form,field):
  if form.manager['type']==2:
    field['where']=f''' id in ({','.join(form.manager['ur_lico_ids'])})'''
    field['autocomplete']=0

def ur_lico_id_filter_code(form,field,row):
  

  links=[f'''<a href="/edit-form/{form.work_table}/{row['wt__id']}" target="_blank">посмотреть прогнозный бонус</a>''']
  
  if (1 in form.query_search['on_filters_hash']['out_action']):
    url=f"/edit-form/action_plan/{row['ap__id']}?open_summary=1&prev={row['prev']}"
    if form.manager['type']==1:
      url+=f"&ur_lico_id={row['u__id']}"
      
    links.append(f'''<a href="{url}" target="_blank">сводные данные</a>''')

  return f'''
    {row['u__header']}<br> <small>{ ' | '.join(links) }</small>'''

def action_id_filter_code(form,field,row):
  return f'{row["a__header"]} ({row["a__date_start"]}..{row["a__date_stop"]})'

def period_id_filter_code(form,field,row):
  #form.pre(row)
  return f'{row["pbp__year"]}, {row["pbp__querter"]} квартал'
def period_id_before_code(form,field):
    field['values']=form.db.query(
      query="select id v,concat(year,' ',querter,' квартал') d from prognoz_bonus_period  where date_begin>=from_days(to_days(curdate())-180) order by date_begin"
    )


def out_action_before_code(form,field):
  field['value']=[1]
  #print('in_before_code:',field['value'])