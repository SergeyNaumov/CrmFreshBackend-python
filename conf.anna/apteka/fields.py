

#from lib.anna.get_apt_list import get_apt_list

def get_fields():
    return [ 
    # {
    #   'name':'registered',
    #   'description':'Дата создания',
    #   'type':'date',
    #   'read_only':1,
    #   'filter_on':1
    # },
    # {
    #   'name':'header',
    #   'description':'Наименование',
    #   'type':'text',
    #   'filter_on':1
    # }, 
    # {
    #   'name':'inn',
    #   'description':'ИНН',
    #   'type':'text',
    #   'filter_on':1
    # },
    {
      'description':'Категория аптеки',
      'name':'category',
      'type':'select_values',
      'values':[
        {'v':1,'d':'A'},
        {'v':2,'d':'B'},
        {'v':3,'d':'C'},
      ],
      'filter_on':1
    },
    {
      'name':'ur_address',
      'db_name':'id',
      'description':'Юридический адрес',
      'type':'filter_extend_select_from_table',
      'table':'apteka',
      'header_field':'ur_address',
      'before_code':ur_address_before_code,
      'value_field':'id',
      'autocomplete':1,
      'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'allready_out_on_result':1,
      #'filter_on':1
    },
    {
      'description':'Представитель аптеки',
      'name':'manager_id',
      'type':'select_from_table',
      'table':'manager',
      'tablename':'m',
      'read_only':1,
      #'header_field':'name',
      'header_field':'concat(login," (",name,")")',
      'value_field':'id',
      'where':'type=3',
      'before_code':manager_id_before_code,
      'filter_code':manager_id_filter_code
    },
    {
      'description':'Телефон представителя аптеки',
      'type':'filter_extend_text',
      'name':'manager_phone',
      'tablename':'m',
      'db_name':'phone',
      'allready_out_on_result':1,
      #'filter_code':manager_phone_filter_code
      #'filter_on':1
    },
    # {
    #   'description':'Менеджер компании Анна',
    #   'name':'anna_manager_id',
    #   'type':'select_from_table',
    #   'table':'manager',
    #   'header_field':'name',
    #   'value_field':'id',
    #   'where':'type=1'
    # }

]
def manager_id_before_code(form,field):
  if form.script == 'find_objects':
    field['header_field']='login'

  if form.manager['type']==1:
    field['read_only']=0


def manager_id_filter_code(form,field,row):
  if row['m__id']:
    return f"{row['m__login']}<br><small>({row['m__name']})</small>"
  else:
    return '-'

def ur_address_before_code(form,field):
  if form.script == 'edit_form':
    field['type']='text'
    field['orig_type']='text'
    #form.pre(field)
  else:
    if form.manager['type']==2:
      #form.pre(form.manager['apt_list_ids'])
      if len(form.manager['ul_ids']):
        field['where']=f'''id in ({','.join(form.manager['apt_list_ids'])})'''
      else:
        field['where']='0'

    #form.pre(field['where'])
    
