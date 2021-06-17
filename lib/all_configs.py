#from conf.test import Config as config_test
#from conf.manager_menu import Config as config_manager_menu
from lib.session import project_get_permissions_for, get_permissions_for

from lib.engine import s
from lib.core import create_fields_hash, exists_arg
import importlib,os

def need_only_read(form):
  w1=True #(form.script=='admin_table' and form.action=='edit')
  w2=(form.script=='memo' and form.action=='get_data')
  w3=(form.script=='find_results')
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

configs={}
  #'test':config_test,
  #'manager_menu':config_manager_menu

folders = os.listdir('./conf')
for f in folders:
  if f !='__pycache__' and os.path.isdir('./conf/'+f) and os.path.isfile('./conf/'+f+'/__init__.py'):

    cur_module=dynamic_import('conf.'+f)
    configs[f]=cur_module.Config


class error():
  def __init__(self,config):
      self.errors=['Конфиг '+config+' не найден']
      self.success=0

def read_config(**arg):
  response={}
  
  if not (arg['config'] in configs):
    return error(arg['config'])
  
  config_class=configs[arg['config']]
  
  form=config_class(arg)
  form.s=s
  s.form=form
  
  form.config=arg['config']
  form.script=arg['script']

  if need_only_read(form): form.db=s.db_read
  else: form.db=s.db_write

  if 'R' in arg: form.R=arg['R']

  # Получаем manager-а 
  login=get_cur_role(
    login=s.login,
    form=form
  )
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
  form.run_all_before_code()
  
  #print('before_get_values:',form.fields[0])
  form.get_values()
  #print('after_get_values:',form.fields[0])
  

  #default_config_attr(form,arg)





  return form



