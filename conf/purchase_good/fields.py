#from .conf.action.header_before_code import header_before_code

def get_fields():
    return [ 
      {
        'description':'Название маркетингового мероприятия',
        'name':'action_id',
        'db_name':'id',
        'type':'filter_extend_select_from_table',
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
        'type':'filter_extend_select_from_table',
        'table':'action_plan',
        'name':'action_plan_id',
        'db_name':'id',
        'header_field':'header',
        'value_field':'id',
        'tablename':'ap',
        'autocomplete':1,
        'depend_filter':['action_id'], # фильтр зависит от указанных
        'before_code':action_plan_id_before_code,
        'filter_on':1,
      },
      {
        'description':'Период действия акции',
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
        'description':'Закуплено товаров, шт',
        'name':'cnt',
        'type':'text',
        'filter_on':1,
      },
      {
        'description':'Сумма',
        'name':'summ',
        'type':'text',
#        'filter_on':1,
      },
      {
        'description':'Штрих-код',
        'name':'code',
        'type':'text',
#        'filter_on':1,
      },
      {
        'description':'Аптека',
        'name':'apteka_id',
        #'autocomplete':1,
        'type':'select_from_table',
        'table':'apteka',
        'tablename':'a',
        'header_field':'ur_address',
        'value_field':'id',
        'filter_on':1,
        'before_code':apteka_id_before_code,
        #'filter_code':apteka_filter_code
      },
      {
        'description':'Юр. лицо',
        'name':'ur_lico_id',
        #'autocomplete':1,
        'type':'filter_extend_select_from_table',
        'table':'ur_lico',
        'tablename':'ul',
        'header_field':'header',
        'value_field':'id',
        'db_name':'id',
        'filter_on':1,
        'before_code':ur_lico_id_before_code
      },

      # {
      #   'description':'Поставщик',
      #   'autocomplete':1,
      #   'name':'supplier_id',
      #   'type':'select_from_table',
      #   'table':'supplier',
      #   'tablename':'s',
      #   'header_field':'header',
      #   'value_field':'id',
      #   'filter_on':1,
      # },

    ]

def apteka_filter_code(form,field,row):
  return f'''{row['wt__id']} => {row['a__ur_address']}'''
def apteka_id_before_code(form,field):
  # для юридического лица выводим только те аптеки, которые закреплены за ним
  if form.manager['type']==2:
    #field['autocomplete']=1
    field['where']=f' id in ({ ",".join(form.manager["apt_list_ids"]) }) '
    #del(field['autocomplete'])
    
def ur_lico_id_before_code(form,field):
  if form.manager['type']==2:
    field['autocomplete']=0
    if len(form.manager["apt_list_ids"]):
      #form.pre(form.manager)
      field['where']=f' id in ({ ",".join(form.manager["ur_lico_ids"]) }) '

    del(field['autocomplete'])

def dates_filter_code(form,field,row):
  return f"{row['act__date_start']} ... {row['act__date_stop']}"

def action_filter_code(form,field,row):
  if row['act__id']:
    return f'''<a href="/edit-form/action/{row['act__id']}" target="_blank">{row['act__header']}</a>'''
  return ''
def suppliers_filter_code(form,field,row):
  #form.pre(row)
  if 'suppliers2' in row:
    return row['suppliers2']
  else:
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
    

    #if len(field['values']):
    #  field['value']=field['values'][0]['v']


    #form.pre(form.manager['type'])

def action_plan_id_before_code(form,field):
  # Делаем так, чтобы автокомлит-фильтр "план акции" зависел от фильтра "акции" (добавляем depend_where)
  if form.script=='autocomplete':
    if 'filters_values' in form.R and form.R['filters_values'] and 'action_id' in form.R['filters_values']:
      actions=form.R['filters_values']['action_id']
      ids=[]
      if len(actions):
        for action_id in actions:
          ids.append(str(action_id))
        if len(ids):
          field['depend_where']='action_id in ('+','.join(ids)+')'
        