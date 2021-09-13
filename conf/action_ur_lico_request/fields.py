



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
      'read_only':1,
      'filter_code':action_filter_code,
      'filter_on':1
    }, 
    {
      'name':'ur_lico_id',
      'description':'Юридическое лицо',
      'type':'select_from_table',
      'table':'ur_lico',
      'header_field':'header',
      'value_field':'id',
      'filter_code':ur_lico_filter_code,
      'tablename':'ul',
      'read_only':1,
      'filter_on':1
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


def action_filter_code(form,field,row):
  return f"<a href='/edit-form/action/{row['a__id']}' target='blank'>{row['a__header']}</a>"

def ur_lico_filter_code(form,field,row):
  return f"<a href='/edit-form/ur_lico/{row['ul__id']}' target='blank'>{row['ul__header']}</a>"