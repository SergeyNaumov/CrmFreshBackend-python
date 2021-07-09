import random, re, time, datetime, os

def cnt_days_period(d1,d2):
  # Ввычисляет кол-во дней между датами
  d1=d1.split('-')
  d2=d2.split('-')
  res=str(datetime.date(int(d2[0]),int(d2[1]),int(d2[2]))-datetime.date(int(d1[0]),int(d1[1]),int(d1[2])))
  #print('rez:',str(res))
  if str(res) == '0:00:00':
    return 0
  return int(res.split()[0])

def tree_to_list(tree_list,lst,level):
  for t in tree_list:
    t['d']=('..'*level) + t['d']
    lst.append({'v':t['v'],'d':t['d']})
    if exists_arg('children',t) and len(t['children']):
      tree_to_list(t['children'],lst,level+1)

def cur_year():
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=0)
  return dat.strftime("%Y")

def exists_arg(key,dict):
  #print('dict:',key,dict)
  if (key in dict) and dict[key]:
    return dict[key]
  return False

def gen_pas(length=8,letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz012345678'):
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
    db_name=f['name']
    rez=re.search('func:\((.+)\)',db_name)
    if rez: return rez[1]
  return ''


def date_to_rus(d):
  d=str(d)
  rez=re.search('^((\d{4})-(\d{2})-(\d{2}))( \d{2}:\d{2}:\d{2})?$',d)
  
  if rez[5]:
    return f"{rez[4]}.{rez[3]}.{rez[2]} {rez[5]}"
  elif rez:
    return f"{rez[4]}.{rez[3]}.{rez[2]}"
  return ''
  # elif d:
  #   date_list=d.split('-')
  #   date_list.reverse()
  #   return '.'.join(date_list)
  


def from_datetime_get_date(dt):
  if not dt: return False
  rez=re.search('^(\d{4}-\d{2}-\d{2})( \d{2}:\d{2}(:\d{2})?)?$',dt)
  if rez:
    return rez[0]
  return False

def create_fields_hash(form):
  form.fields_hash={}
  for f in form.fields:
    if 'name' in f:
      form.fields_hash[f['name']]=f
    else:
      form.errors.append('Отсутствует name в поле: ',f)


# Возвращает расширение файла
def get_ext(filename):
    arr=filename.split('.')
    l=len(arr)
    if l>1:
        return arr[l-1]
    return ''

def get_name_and_ext(filename):
  name_and_ext_arr=re.search(r'([^\/]+)\.([^\.]+)$',filename)
  if(name_and_ext_arr):
    return name_and_ext_arr[1],name_and_ext_arr[2]

  return filename,''

def b64_split(data):
    rez=re.search(r'^data:(.+?);base64,(.+)',data)
    if rez:
        return {'mime':rez[1],'base64':rez[2]}


def random_filename(): # генерирует имя файла без расширения
    return str(time.time()).split('.')[0]+'_'+str(random.random()*10**12).split('.')[1]

# is_wt_field
check_list=[
  'text','textarea','hidden','wysiwyg','select_from_table','select_values','checkbox','switch',
  'date','time','datetime','yearmon','daymon','hidden','font-awesome','file'
]
def check_wt_field(t):
  return t in check_list
def is_wt_field(f):
  if 'orig_type' in f and f['orig_type']:
    return check_wt_field(f['orig_type'])
  else:
    return check_wt_field(f['type'])



def get_child_field(field,name):
  for f in field['fields']:
    if f['name']==name: return f
  return None

# Вывод ошибки в консоль
def print_console_error(text):
  print("\033[31m {}" .format(text),"\033[0m")

def del_file_and_resizes(**arg):
  field=arg['field']
  value=arg['value']
  name=field['name']  
  
  if not value:
    return
  
  filename_without_ext,ext=get_name_and_ext(value)
  if ext:
      # удаляем ресайзы
      if exists_arg('resize',field) and len(field['resize']):
        for r in field['resize']:
          #print('r:',r)
          f=r['file']
          f=f.replace('<%filename_without_ext%>',filename_without_ext)
          f=f.replace('<%ext%>',ext)
          
          file_for_del=field['filedir']+'/'+f
          #print('rm: ',file_for_del)
          if os.path.isfile(file_for_del):
            os.remove(file_for_del)

      # удаляем основной файл
      file_for_del=field['filedir']+'/'+value
      if os.path.isfile(file_for_del):
        os.remove(file_for_del)
        #print('del main file:',file_for_del)


