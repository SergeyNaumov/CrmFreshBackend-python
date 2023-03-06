import importlib,os

from lib.session import project_get_permissions_for, get_permissions_for

from lib.engine import s
from lib.core import exists_arg

from config import config as sysconfig
from lib.CRM.form import Form
import copy

def need_only_read(form):
  w1=True #(form.script=='admin_table' and form.action=='edit')
  #w2=(form.script=='memo' and form.action=='get_data')
  #w3=(form.script=='find_results')
  if w1: #  or w2 or w3
    return True

  return False

def get_cur_role(**arg):
  form=arg['form']
  if(form.config == 'manager'):
    return arg['login']
  
  manager_table='manager'
  manager_role_table='manager_role'
  if s.use_project:
      manager_role_table='project_manager_role'
      manager_table='project_manager'
  
  r=s.db.query(
    query="""
      SELECT
        m2.login
      FROM
        """+manager_table+' m JOIN '+manager_role_table+""" mr ON (m.id = mr.manager_id)
        JOIN """+manager_table+""" m2  ON (m2.id = mr.role AND m.current_role = m2.id)
      WHERE m.login=%s
    """,
    values=[arg['login']],
    onevalue=1,
    errors=form.errors
  )

  if r:
    return r
  else:
    return arg['login']

def dynamic_import(module):
    return importlib.import_module(module)

# configs={}
#   #'test':config_test,
#   #'manager_menu':config_manager_menu


# folders = os.listdir('./conf')
# for f in folders:
#   if f !='__pycache__' and os.path.isdir('./conf/'+f) and os.path.isfile('./conf/'+f+'/__init__.py'):

#     cur_module=dynamic_import('conf.'+f)
#     configs[f]=cur_module.Config


class error():
  def __init__(self,errors):
      self.errors=errors
      self.success=0

      

def load_form_from_dir(confdir,conflib_dir, arg):
  form=False
  errors=[]
  if os.path.isdir(f"{confdir}/{arg['config']}") and os.path.isfile(f"{confdir}/{arg['config']}/__init__.py"):
    try:
      module=importlib.import_module(conflib_dir+'.'+arg['config'])
      
      form_data=copy.deepcopy(module.form)
    except SyntaxError as e:
      errors.append(f"1Ошибка при загрузке конфига {arg['config']}: {e}")
    except ModuleNotFoundError as e:
      errors.append(f"2Ошибка при загрузке конфига {arg['config']}: {e}\n{conflib_dir+'.'+arg['config']}")
    
    if not len(errors) and os.path.isfile(f"{confdir}/{arg['config']}/events.py"):
      try:
        module=importlib.import_module(conflib_dir+'.'+arg['config']+'.events')
        form_data['events']=module.events
      except SyntaxError as e:
        errors.append(f"1Ошибка при загрузке конфига {arg['config']}/events.py: {e}")
      except ModuleNotFoundError as e:
        errors.append(f"2Ошибка при загрузке конфига {arg['config']}/events.py: {e}")
    
    if not len(errors):
      form=Form(arg)  
      form.load_data(form_data)
    
    if not len(errors) and  os.path.isfile(f"{confdir}/{arg['config']}/events_for_fields.py"):
      try:
        module=importlib.import_module(conflib_dir+'.'+arg['config']+'.events_for_fields')
        events=module.events
        for f in form.fields:
          if 'name' not in f:
            form.errors.append(f'{f["description"]}: не указано имя!')
            break
          
          if f['name'] in events:
            for postfix in ['before_code','permissions','filter_code','code']:
              if postfix in events[f['name']]:
                f[postfix]=events[f['name']][postfix]

      except SyntaxError as e:
          errors.append(f"1Ошибка при загрузке конфига {arg['config']}/events_for_fields.py: {e}")
      except ModuleNotFoundError as e:
          errors.append(f"2Ошибка при загрузке конфига {arg['config']}/events_for_fields: {e}")
          
      #print('FIELDS:',form.fields)
        

  return [form,errors]

def read_config(**arg):
  response={}
  
  # попытка загрузки локального конфига
  #print('STEP1')
  if len(s.errors): return error(s.errors)
  [form,errors]=load_form_from_dir(f'./conf', f'conf',arg)
  if len(errors): return error(errors)
  
  # Если локальной папки нет -- загружаем глобальный конфиг
  if not(form) and hasattr(s,'project_id'):
    [form,errors]=load_form_from_dir(f'./conf_projects/project_{s.project_id}', f'conf_projects.project_{s.project_id}',arg)
    if len(errors): return error(errors)

  if not(form):    
    return error([f'конфиг {arg["config"]} не найден'])

  
  form.s=s
  s.form=form
  if 'after_read_form_config' in sysconfig:
      sysconfig['after_read_form_config'](form)

  form.config=arg['config']
  form.script=arg['script']



  if need_only_read(form): form.db=s.db_read
  else: form.db=s.db_write

  if 'R' in arg: form.R=arg['R']

  # Получаем manager-а 
  auth=sysconfig['auth']
  if auth['use_roles']:
    login=get_cur_role(
      login=s.login,
      form=form
    )
  
  if auth['use_permissions']:
    if s.use_project:
      form.manager=project_get_permissions_for(form,login)
    else:
      form.manager=get_permissions_for(form,login)
  
  # Атрибуты по умолчанию
  if exists_arg('id',arg): form.id=arg['id']
  if exists_arg('action',arg): form.action=arg['action']
  if not form.work_table: form.work_table=arg['config']
  
  form.run_event('permissions')

  form.default_config_attr(arg)
  form.set_orig_types()
  
  # Перенёс из routes.edit_form.process_edit_form.py
  #form.get_values()
  
  form.get_values()
  form.run_all_before_code()
  form.get_fields_values()

  return form



