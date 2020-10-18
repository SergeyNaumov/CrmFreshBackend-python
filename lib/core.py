import random
import datetime
import re

def cur_year():
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=0)
  return dat.strftime("%Y")

def exists_arg(key,dict):
  if (key in dict) and dict[key]:
    return dict[key]
  return False

def gen_pas(length=8):
  letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
  return ''.join(random.choice(letters) for i in range(length))
  
def cur_date(delta=0,format="%Y-%m-%d"):
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=delta)
  return dat.strftime(format)


def is_errors(form):

  if isinstance(form,dict):
    return ( ('errors' in form) and len(form['errors']) )
  else:
    return (hasattr(form,'errors') and len(form.errors))

def get_func(f):
  db_name=f['name']
  if exists_arg('db_name',f):
    db_name=name
    rez=re.search('func:\((.+)\)',db_name)
    if rez: return rez[1]
  return ''

def from_datetime_get_date(dt):
  if not dt: return False
  rez=re.search('^(\d{4}-\d{2}-\d{2})( \d{2}:\d{2}:\d{2})?$',dt)
  if rez: return rez[1]
  return False

def create_fields_hash(form):
  form.fields_hash={}
  for f in form.fields:
    form.fields_hash[f['name']]=f



# is_wt_field
check_list=[
  'text','textarea','hidden','wysiwyg','select_from_table','select_values',
  'date','time','datetime','yearmon','daymon','hidden','checkbox','switch','font-awesome','file'
]
def check_wt_field(t):
  return t in check_list
def is_wt_field(f):

  if 'type_orig' in f and f['type_orig']:
    return check_wt_field(f['type_orig'])
  else:
    return check_wt_field(f['type'])

