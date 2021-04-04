#from conf.test import Config as config_test
#from conf.manager_menu import Config as config_manager_menu

from lib.engine import s
from lib.core import create_fields_hash, exists_arg
import importlib,os

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
  form.default_config_attr(arg)
  form.set_orig_types()
  # Перенёс из routes.edit_form.process_edit_form.py
  form.run_event('permissions')
  for f in form.fields:
    if exists_arg('permissions',f): form.run_event('permissions',{'field':f})

  form.get_values()
  for f in form.fields:
    if exists_arg('before_code',f): form.run_event('before_code',{'field':f})
  #form.run_all_before_code()

  #default_config_attr(form,arg)





  return form



