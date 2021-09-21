


def attach_filter_code(form,field,row):
  #
  if row['wt__attach']:
    full_path='/files/bonus_order/'+row['wt__attach']
    return f'<a href="{full_path}" target="blank">скачать</a>'
  else:
    return ''
  
def attach_before_code(form,field):
  if form.script=='admin_table': # для того, чтобы не отображался как фильтр
    form.fields_hash['attach']['type']='code'



def get_fields():
    return [ 
    {
      'name':'attach',
      'description':'Файл',
      'filedir':'./files/bonus_order',
      'type':'file',
      'before_code':attach_before_code,
      #'filter_on':1,
      'filter_code':attach_filter_code

    },
    {
      'description':'Юридическое лицо',
      'filter_on':1,
      'name':'ur_lico_id',
      'type':'filter_extend_select_from_table',
      'tablename':'ul',
      'table':'ur_lico',
      'header_field':'header',
      'value_field':'id',

    },
    {
      'description':'Дата и время добавления',
      'name':'registered',
      'type':'datetime',
      'defaul_off':1,
      'filter_on':1
    },
    {
      'description':'Статус',
      'name':'status',
      'type':'select_values',
      'filter_on':1,
      'values':[
        {'v':1,'d':'в работе'},
        {'v':2,'d':'обработан'},
      ]
    }

]