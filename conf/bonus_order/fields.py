


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
      'description': 'Юридическое лицо',
      'type':'code',
      'name':'ur_lico',
      'read_only':1,
      #'after_html':'xjshjhsjhsjhsj'
      'before_code': ur_lico_before_code
    } ,
    {
      'name':'attach',
      'description':'Файл',
      'filedir':'./files/bonus_order',
      'type':'file',
      'read_only':1,
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
      'type':'date',
      'read_only':1,
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
    },
    {
      'description':'Номер акта',
      'type':'filter_extend_text',
      'filter_type':'range',
      'name':'number',
      'tablename':'b',
      'filter_on':1,
    }

]


def ur_lico_before_code(form,field):
  field['after_html']=f'''
    <b>Акт №{form.ov['number']}</b><br>
    Юридическое лицо: {form.ov['ur_lico']}<br>

  '''
  
  #form.pre(field)