


def get_fields():
    return [ 
    {
      'description':'Логин',
      'type':'select_values',
      'name':'manager_id',
      'values':[],
      'filter_on':1,
      'before_code':manager_id_before_code,
      'filter_code':manager_id_filter_code
    },
    {
      'description':'Период',
      'name':'period_id',
      'tablename':'per',
      'filter_on':1,
      
      'type':'select_values',
      'filter_code':period_id_filter_code,
      'before_code':period_id_before_code,

    },
    {
      'description':'Маркетинговое мероприятие',
      'name':'action_id',
      'type':'select_from_table',
      'table':'action',
      'tablename':'a',
      'header_field':'header',
      'value_field':'id',
      'multilpe':0,
      'autocomplete':1,
      'where':'date_stop>=curdate()',
      'autocomplete_start_loaded':1, # подгружать autocomplete по умолчанию
      'before_code':action_before_code,
      'filter_code':action_filter_code,
      'filter_on':1,

    },
    {
      'description':'% выполнения',
      'name':'percent_complete',
      'type':'text',
      'filter_type':'range',
      'allready_out_on_result':1,
      'filter_code':percent_complete_filter_code
    },
    {
      'description':'Осталось выполнить %',
      'name':'left_to_complete_percent',
      'filter_type':'range',
      'type':'text',
      'allready_out_on_result':1,
      'filter_code':left_to_complete_percent_filter_code
    },
    {
      'description':'Осталось выполнить в рублях / штуках',
      'name':'left_to_complete_rub',
      'filter_type':'range',
      'type':'text',
      'allready_out_on_result':1,
      'filter_code':left_to_complete_rub_filter_code
    },
]


def period_id_filter_code(form,field,row):
  #form.pre(row)
  return f'{row["per__year"]}-{row["per__querter"]}'

def period_id_before_code(form,field):
    field['values']=form.db.query(
      query="select id v,concat(year,' ',querter,' квартал') d from prognoz_bonus_period  where date_begin>=from_days(to_days(curdate())-180) order by date_begin"
    )

def action_filter_code(form,field,row):
  if ('plugin' in form.R) and form.R['plugin']=='search_xls' and row['a__id']:
    return row['act__header']
  
  if row['a__id']:
    ur_lico_id=''
    if row['wt__manager_id'] and (row['wt__manager_id'] in form.manager_ur_lico):
      ur_lico_id=form.manager_ur_lico[row['wt__manager_id']]

    url=f'''/edit-form/action_plan/{row['wt__action_plan_id']}?open_summary=1&ur_lico_id={ur_lico_id}'''
    return f'''<a href="{url}" target="_blank">{row['a__header']} / {row['ap__header']}</a><br>'''
      # wt.id: {row['wt__id']}<br>
      # action_plan_id: {row['ap__id']}<br>
      # ur_lico_id: {row['ul__id']}<br>
      # apteka_id: {row['wt__apteka_id']} {row['a__header']}
  return ''

def action_before_code(form,field):
  
  field['where']=''

  # Ограничение для юрлиц
  if form.manager['type']==2:
    where=' 1 '
  
  # Ограничение для аптек
  if form.manager['type']==3: 
    where=' 2 '

  if form.script=='admin_table':
    
    query="SELECT id v, concat(header,'-',date_stop) d from action where date_stop>=curdate() limit 10"
    if field['where']:
      query+=' WHERE '+field['where']
    
    field['values']=form.db.query(
      query=query
    )


def percent_complete_filter_code(form,field,row):
  r=''
  if row['percent_complete']=='percent': 
    r='% за любые закупки'
  else:
    r=str(row['percent_complete'])

  return r
  #+f"<br><small><a href='/edit-form/action_plan/{row['wt__action_plan_id']}?open_summary=1' target='_blank'>сводные данные</a></small>"

def left_to_complete_percent_filter_code(form,field,row):
  return row['left_to_complete_percent']

def left_to_complete_rub_filter_code(form,field,row):
  return row['left_to_complete_rub']

def manager_id_before_code(form,field):
  # узнаём, какие логины вообще у нас есть
  ids=form.db.query(query="SELECT distinct(manager_id) FROM prognoz_bonus_pivot_ul",massive=1,str=1)
  
  if len(ids):
    field['values']=form.db.query(
      query=f"""
        SELECT
          id v,
          concat( login,if(comment='','',concat(' - ',comment))) d
        FROM
          manager
        WHERE id in ({','.join(ids)})
        ORDER BY login
      """
    )
    

def manager_id_filter_code(form,field,row):
  if row['m__comment']:
    return f"{row['m__login']} - {row['m__comment']}"
  return row['m__login']