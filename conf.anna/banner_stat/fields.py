def get_fields():
    return [ 
    {
      'description':'Дата и время',
      'type':'datetime',
      'name':'ts',
      'filter_on':1
    },
    {
      'name':'header',
      'description':'Название баннера',      
      'type':'text',
      'filter_on':1,
      'tablename':'b',
      'filter_code':banner_filter_code,
      'filter_on':1
    },
    {
      'description':'Аккант',
      'type':'select_from_table',
      'name':'manager_id',
      'table':'manager',
      'header_field':'login',
      'value_field':'id',
      'tablename':'m',
      'filter_on':1
    },
    {
      'description':'Тип аккаунта',
      'type':'filter_extend_select_values',
      'name':'type',
      'tablename':'m',
      'values':[
        {'v':1,'d':'Менеджер'},
        {'v':2,'d':'Юридическое лицо'},
        {'v':3,'d':'Аптека'},
        {'v':4,'d':'Фармацевт'},
      ],
      'filter_on':1
    },
    {
      'description':'Действие',
      'type':'select_values',
      'name':'action',
      'values':[
        {'v':'show','d':'показ'},
        {'v':'click','d':'клик'},
      ],
      'filter_on':1
    },
    {
      'description':'Юридическое лицо',
      'name':'ur_lico_id',
      'type':'filter_extend_select_from_table',
      'tablename':'ul',
      'autocomplete':1,
      'table':'ur_lico',
      'header_field':'header',
      'value_field':'id',
      'filter_code':ur_lico_id_filter_code,
      'not_process':1

    },
    {
      'description':'Аптека',
      'name':'apteka_id',
      'type':'filter_extend_select_from_table',
      'tablename':'apt',
      'autocomplete':1,
      'table':'apteka',
      'header_field':'ur_address',
      'value_field':'id',
      'filter_code':apteka_id_filter_code,
      'not_process':1
    }

]

def ur_lico_id_filter_code(form,field,row):
  t=row['m__type']
  if t==2: # юр. лицо
    return row['ul__header']
  elif t==3: # аптека
    return row['ul2__header']
  
  return '-'

def apteka_id_filter_code(form,field,row):
  t=row['m__type']
  if t==3: # аптека
    return row['apt__ur_address']
  return '-'

def banner_filter_code(form,field,row):
  return f"""<a href="/edit_form/banner/{row['wt__banner_id']}" target="_blank">{row['b__header']}</a>"""