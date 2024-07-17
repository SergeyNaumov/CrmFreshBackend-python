import random, re, time, datetime, os

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_triade(x):
  return '{0:,}'.format(x).replace(',', '`')

def join_ids(ids):
  result=''
  idx=0
  str_list=[str(_id) for _id in ids]
  return ','.join(str_list)

def cnt_days_period(d1,d2):
  # Ввычисляет кол-во дней между датами
  
  if not(isinstance(d1,str)): d1=str(d1)
  if not(isinstance(d2,str)): d2=str(d2)
  d1=d1.split('-')
  d2=d2.split('-')
  res=str(datetime.date(int(d2[0]),int(d2[1]),int(d2[2]))-datetime.date(int(d1[0]),int(d1[1]),int(d1[2])))
  #print('rez:',str(res))
  if str(res) == '0:00:00':
    return 0
  return int(res.split()[0])+1

def tree_to_list(tree_list,lst,level):
  for t in tree_list:
    t['d']=('..'*level) + t['d']
    lst.append({'v':t['v'],'d':t['d']})
    if exists_arg('children',t) and len(t['children']):
      tree_to_list(t['children'],lst,level+1)



def exists_arg(key,dict):
  #print('dict:',key,dict)
  # Сложная структура
  if isinstance(key,str):
    keys=key.split(';')
  
    if len(keys)>1:
      dict2=dict
      v=False
      for k in keys:
        if not(k in dict2):
          return False
        dict2=dict2[k]
      return dict2
  # Простая структура
  
  if (key in dict) and dict[key]:
    return dict[key]
  return False

def gen_pas(length=8,letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz012345678'):
  return ''.join(random.choice(letters) for i in range(length))
  
def cur_year():
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=0)
  return dat.strftime("%Y")

def cur_date(delta=0,format="%Y-%m-%d"):
  dat = datetime.date.today()
  dat = dat + datetime.timedelta(days=delta)
  return dat.strftime(format)

def cur_hour():
  now=datetime.datetime.now()
  return now.hour
  
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
  if rez and rez[5]:
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
  rez=re.search('^(\d{4}-\d{2}-\d{2})\s*(\d{2}:\d{2}(:\d{2})?)?$',dt)
  if rez:
    return rez[0]
  else:
    if rez:=re.search('^(\d{4}-\d{2}-\d{2}).*$',dt):
      print('res: ',rez)
      return rez[1]

def create_fields_hash(form):
  form.fields_hash={}
  for f in form.fields:
    if 'name' in f:
      form.fields_hash[f['name']]=f
    elif not f.get('type') in ('header'):
      form.errors.append(f'Отсутствует name в поле: {f["description"]}')


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
    return str(time.time()).split('.')[0]+'_'+gen_pas(2)

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
  #print('VALUE:',value)
  if not value:
    return
  
  filename_without_ext,ext=get_name_and_ext(value)
  #print('filename_without_ext:',filename_without_ext, 'ext:',ext)
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
        


