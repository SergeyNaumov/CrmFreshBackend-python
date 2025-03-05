



def get_fields():
    return [ 
    {
      'name':'ts',
      'description':'Дата и время заявки',
      'type':'date',
      'read_only':1,
      'filter_on':1
    },
    {
      'name':'action_id',
      'description':'Акция',
      'type':'select_from_table',
      'table':'action',
      'header_field':'header',
      'value_field':'id',
      'tablename':'a',
      'autocomple':1,
      'filter_code':action_filter_code,
      'filter_on':1
    }, 
    {
      'name':'apteka_id',
      'description':'Аптека',
      'type':'select_from_table',
      'table':'apteka',
      'header_field':'ur_address',
      'value_field':'id',
      'before_code':apteka_before_code,
      'filter_code':apteka_filter_code,
      'tablename':'apt',
      'filter_on':1
    },
    {
      'description':'Юр. лицо',
      'type':'filter_extend_select_from_table',
      'name':'ur_lico_id',
      'db_name':'id',
      'table':'ur_lico',
      'tablename':'ul',
      'header_field':'header',
      'value_field':'id',
      'db_name':'header',
      #'filter_code':ur_lico_id_filter_code

    },
    {
      'description':'Статус',
      'type':'select_values',
      'name':'status',
      'filter_on':1,
      'values':[
        {'v':'1','d':'В работе'},
        {'v':'2','d':'В закрыто'},
      ]
    }
]

def apteka_before_code(form,field):
  if form.manager['type']==2:
    field['where']='id in ('+','.join(form.manager['apt_list_ids'])+')'

def action_filter_code(form,field,row):
  return f"<a href='/edit-form/action/{row['a__id']}' target='blank'>{row['a__header']}</a>"

def apteka_filter_code(form,field,row):
  return f"<a href='/edit-form/apteka/{row['apt__id']}' target='blank'>{row['apt__ur_address']}</a>"

def ur_lico_id_filter_code(form,field,row):
  return row['ul__header']