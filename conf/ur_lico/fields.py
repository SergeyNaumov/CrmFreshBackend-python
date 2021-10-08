



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
      'description':'Юридическое лицо',
      'name':'f_header',
      'type':'filter_extend_select_from_table',
      'header_field':'header',
      'value_field':'id',
      'autocomplete':1,
      'table':'ur_lico',
      'tablename':'wt',
      'db_name':'id',
      'before_code':before_code_header,
      'filter_code':filter_code_header,
      'filter_on':1
    },
    {
      'description':'Юридический адрес',
      'name':'f_ur_address',
      'type':'filter_extend_select_from_table',
      'header_field':'ur_address',
      'value_field':'id',
      'autocomplete':1,
      'table':'ur_lico',
      'tablename':'wt',
      'db_name':'id',
      'before_code':before_code_ur_address,
      'filter_on':1
    },

    {
      'name':'header',
      'description':'Юридическое лицо',
      'type':'text',
      #'filter_code':filter_code_header,
      'not_filter':1,
      #'autocomplete':1,
      #'filter_on':1
    }, 

    {
      'name':'ur_address',
      'description':'Юридический адрес',
      'type':'text',
      'not_filter':1,
      #'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },
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
      'description':'Менеджер компании АннА',
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
    {
      'description':'Представитель юридического лица',
      'name':'manager_id',
      'type':'filter_extend_text',
      'tablename':'m1',
      'db_name':'func::concat(login," ",name," ",name_f," ",name_i," ",name_o)',
      'table':'manager',
      'not_process':1,
      'where':'type=2',
      'filter_code':filter_code_manager_id
    }
]

def before_code_header(form,field):
  where=''
  #form.pre(form.manager)
  field['values']=form.db.query(
    query=f'select id v,header d from ur_lico where header order by header limit 50'
  )

def before_code_ur_address(form,field):
  where=''
  #form.pre(form.manager)
  field['values']=form.db.query(
    query=f'select id v,ur_address d from ur_lico where ur_address order by ur_address  limit 50'
  )


# def before_code_anna_manager_id(form,field):
#   field['values']=form.db.query(
#     query="select id v, concat(name_f,' ',name_i,' ',name_o) h from manager where type=1"
#   )

#   form.pre(field)
def filter_code_manager_id(form,field,row):
  return row['pred_ul']
  
  #f"{row['m1__login']}<br>{row['m1__name_f']} {row['m1__name_i']} {row['m1__name_o']}"
def filter_code_anna_manager_id(form,field,row):
  return f'''{row['m2__name_f']} {row['m2__name_i']} {row['m2__name_o']}'''
def filter_code_header(form,field,row):
  #form.pre(row)
  return f'''{row['wt__header']} <small>аптек: {row['cnt_apt']}</small>'''
