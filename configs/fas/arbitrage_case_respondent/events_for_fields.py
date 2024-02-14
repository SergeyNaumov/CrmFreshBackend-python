def case_number_filter_code(form,field,row):
    case_number=row['c__case_number']
    case_id=row['c__case_id']
    return f'<a href="https://kad.arbitr.ru/Card/{case_id}" target="_blank">{case_number}</a>'

def user_id_filter_code(form,field,row):
  v=row['tr__user_id']
  if v:
    return f'<a href="/edit_form/user/{v}" target="_blank">{v}</a>'
  return '-'


def email_filter_code(form,field,row):
    return row['email']

events={
    'case_number':{
        'filter_code':case_number_filter_code
    },
    'user_id':{
        'filter_code':user_id_filter_code
    },
    'email':{
        'filter_code':(lambda form,field,row: row['email'])
    },
    'email':{
        'filter_code':(lambda form,field,row: row['phone'])
    },

}