from lib.core import cur_date
def registered_before_code(form,field):
  cd=cur_date()
  field['value']=[cd,cd]

def is_double2_filter_code(form,field,row):
  v='нет'
  if row['wt__'+field['name']]==1: v='да'
  return f'{v}<br><small style="white-space: nowrap;">{row["wt__ts"]}</small>'

def link_filter_code(form,field,row):
  url=row["wt__link"]
  if url:
    return f'<a href="{url}" target="_blank">{url}</a>'
  return '-'
  
def download_link_filter_code(form,field,row):
  url=row['wt__download_link']
  #form.pre(row['wt__download_link'])
  if url:
    return f'<a href="{url}" target="_blank">{url}</a>'
  else:
    return '-'

def api_links_filter_code(form,field,row):
  if row["wt__api_links"]:
    return f'<a href="{row["wt__api_links"]}" target="_blank">отправить</a>'

def user_id2_filter_code(form,field,row):    
  if row["wt__user_id"]:
    return f'<a href="/edit_form/user/{row["wt__user_id2"]}" target="_blank">{row["wt__user_id2"]}</a>'
  return '-'


events={
  'registered':{
    'before_code':registered_before_code
  },
  'is_double2':{
    'filter_code':is_double2_filter_code
  },
  'link':{
    'filter_code':link_filter_code
  },
  'download_link':{
    'filter_code':download_link_filter_code
  },
  'api_links':{
    'filter_code':api_links_filter_code
  },
  'user_id2':{
    'filter_code':user_id2_filter_code
  }
}