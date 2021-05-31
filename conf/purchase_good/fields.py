def get_fields():
    return [ 
      {
        'description':'Мероприятие',
        'name':'action_id',
        'type':'select_from_table',
        'table':'action',
        'tablename':'act',
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
        'description':'Группа товаров',
        'type':'filter_extend_text',
        'name':'action_plan_header',
        'tablename':'ap',
        'db_name':'header',
        'filter_on':1,
      },
      {
        'description':'Выводить даты',
        'name':'date_start',
        'type':'checkbox',
        'not_process':True,
        'tablename':'act',
        'default_off':1,
        'filter_code':dates_filter_code,
        'filter_type':'checkbox',
        'filter_on':1,
      },
      {
        'description':'Поставщики для акции',
        'name':'suppliers',
        'type':'checkbox',
        'filter_type':'checkbox',
        'not_process':True,
        'tablename':'act',
        'default_off':1,
        'filter_code':suppliers_filter_code,
        'filter_on':1,
      },
      # {
      #   'description':'Начало мероприятия',
      #   'name':'date_start',
      #   'type':'filter_extend_date',
      #   'tablename':'act',
      #   'default_off':1,
      #   'filter_on':1,
      # },
      # {
      #   'description':'Окончание мероприятия',
      #   'name':'date_stop',
      #   'type':'filter_extend_date',
      #   'tablename':'act',
      #   'default_off':1,
      #   'filter_on':1,
      # },
      {
        'description':'Наименование товара',
        'name':'header',
        'type':'text',
        'autocomplete':1,
        'filter_on':1,
      },
      {
        'description':'Кол-во',
        'name':'cnt',
        'type':'text',
        'filter_on':1,
      },
      {
        'description':'Сумма',
        'name':'summ',
        'type':'text',
        'filter_on':1,
      },
      {
        'description':'Штрих-код',
        'name':'code',
        'type':'text',
        'filter_on':1,
      },
      {
        'description':'Аптека',
        'name':'apteka_id',
        'autocomplete':1,
        'type':'select_from_table',
        'table':'apteka',
        'tablename':'a',
        'header_field':'ur_address',
        'value_field':'id',
        'filter_on':1,
      },
      {
        'description':'Поставщик',
        'autocomplete':1,
        'name':'supplier_id',
        'type':'select_from_table',
        'table':'supplier',
        'tablename':'s',
        'header_field':'header',
        'value_field':'id',
        'filter_on':1,
      },

    ]



def dates_filter_code(form,field,row):
  return f"{row['act__date_start']} ... {row['act__date_stop']}"

def action_filter_code(form,field,row):
  if row['act__id']:
    return f'''<a href="/edit-form/action/{row['act__id']}" target="_blank">{row['act__header']}</a>'''
  return ''
def suppliers_filter_code(form,field,row):
  return row['suppliers2']

def action_before_code(form,field):
  manager_type=form.manager['type']
  
  field['where']=''

  # Ограничение для юрлиц
  if form.manager['type']==2:
    where=' 1 '
  
  # Ограничение для аптек
  if form.manager['type']==3: 
    where=' 2 '

  if form.script=='admin_table':
    
    query="SELECT id v,header d from action limit 10"
    if field['where']:
      query+=' WHERE '+field['where']
    
    field['values']=form.db.query(
      query=query
    )
    

    if len(field['values']):
      field['value']=field['values'][0]['v']


    form.pre(form.manager['type'])