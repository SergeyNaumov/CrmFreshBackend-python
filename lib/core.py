import random, re, time, datetime

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
    if 'name' in f:
      form.fields_hash[f['name']]=f
    else:
      print('Отсутствует name в поле: ',f)


# Возвращает расширение файла
def get_ext(filename):
    arr='basename.txt'.split('.')
    l=len(arr)
    if l>1:
        return arr[l-1]
    return ''

def b64_split(data):
    rez=re.search(r'^data:(.+?);base64,(.+)',data)
    if rez:
        return {'mime':rez[1],'base64':rez[2]}


def random_filename(): # генерирует имя файла без расширения
    str(time.time()).split('.')[0]+'_'+str(random.random()*10**12).split('.')[1]

# is_wt_field
check_list=[
  'text','textarea','hidden','wysiwyg','select_from_table','select_values','checkbox','switch',
  'date','time','datetime','yearmon','daymon','hidden','checkbox','font-awesome','file'
]
def check_wt_field(t):
  return t in check_list
def is_wt_field(f):
  if 'type_orig' in f and f['type_orig']:
    return check_wt_field(f['type_orig'])
  else:
    return check_wt_field(f['type'])

