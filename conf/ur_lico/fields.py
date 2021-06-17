



def get_fields():
    return [ 
    {
      'name':'inn',
      'description':'ИНН',
      'type':'text',
      'read_only':1,
      'filter_on':1
    },
    {
      'name':'header',
      'description':'Наименование',
      'type':'text',
      'filter_code':filter_code_header,
      #'make_change_in_search':1,
      'filter_on':1
    }, 
    # {
    #   'name':'inn',
    #   'description':'ИНН',
    #   'type':'text',
    #   'filter_on':1
    # },
    {
      'name':'ur_address',
      'description':'Юридический адрес',
      'type':'text',
      'filter_on':1
    },
    # {
    #   'description':'Телефон',
    #   'type':'text',
    #   'name':'phone',
    #   'filter_on':1
    # },
    # {
    #   'description':'Представитель юридического лица',
    #   'name':'manager_id',
    #   'type':'select_from_table',
    #   'table':'manager',
    #   'tablename':'m1',
    #   'header_field':'name',
    #   'value_field':'id',
    #   'where':'type=2'
    # },
    {
      'description':'Менеджер компании Анна',
      'name':'anna_manager_id',
      'type':'select_from_table',
      'table':'manager',
      'tablename':'m2',
      'header_field':'name',
      'value_field':'id',
      'where':'type=1',
      # 
      'query':"SELECT id v, concat(name_f,' ',name_i,' ',name_o) d from manager ",
      #'before_code':before_code_anna_manager_id,
      'filter_code':filter_code_anna_manager_id,
      'filter_on':1
    },
]

# def before_code_anna_manager_id(form,field):
#   field['values']=form.db.query(
#     query="select id v, concat(name_f,' ',name_i,' ',name_o) h from manager where type=1"
#   )

#   form.pre(field)

def filter_code_anna_manager_id(form,field,row):
  return f'''{row['m2__name_f']} {row['m2__name_i']} {row['m2__name_o']}'''
def filter_code_header(form,field,row):
  #form.pre(row)
  return f'''{row['wt__header']} <small>аптек: {row['cnt_apt']}</small>'''
