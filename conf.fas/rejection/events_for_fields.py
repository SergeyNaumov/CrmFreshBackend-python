from lib.core import cur_date


def id_filter_code(form,field,row):
        return f'{row["wt__id"]}<br><small style="white-space: nowrap;">{row["wt__registered"]}</small>'

def without_ftp_before_code(form,field):
  if form.script=='admin_table':
    field['value']=[1]

def registered_before_code(form,field):
  if form.script=='admin_table':
    field['value']=''
  # 'default_off':1,
  #pass
def link_filter_code(form,field,row):
  
  #form.pre(row)
  v=row['wt__link']
  if v:
    return f'<a href="{v}" target="_blank">{v}</a>'
  return '-'

def api_links_filter_code(form,field,row):
  v=row['wt__api_links']
  if v:
    return f'<a href="{v}" target="_blank">отправить</a>'
  return '-'
  
def ts_before_code(form,field):
  if form.script=='admin_table':
    cd=cur_date()
    field['value']=[f'{cd}',f'{cd}']

def user_id_filter_code(form,field,row):
  v=row['wt__user_id']
  if v:
    return f'<a href="/edit_form/user/{v}" target="_blank">{v}</a>'
  return '-'

events={
  'id':{
    'filter_code':id_filter_code
  },
  'without_ftp':{
    'before_code':without_ftp_before_code
  },
  'registered':{
    'before_code':registered_before_code
  },
  'link':{
    'filter_code':link_filter_code
  },
  'api_links':{
    'filter_code':api_links_filter_code
  },
  'ts':{
    'before_code':ts_before_code
  },
  'user_id':{
    'filter_code':user_id_filter_code
  }
}