from conf.test import Config as config_test
from conf.manager_menu import Config as config_manager_menu

from lib.engine import s
from lib.core import create_fields_hash, exists_arg

configs={
  'test':config_test,
  'manager_menu':config_manager_menu
}

class error():
  def __init__(self,config):
      self.errors=['Конфиг '+config+' не найден']
      self.success=0

def read_config(**arg):
  response={}
  
  if not (arg['config'] in configs):
    return error(arg['congif'])
  
  config_class=configs[arg['config']]
  form=config_class(arg)
  form.default_config_attr(arg)
  form.set_orig_types()
  #default_config_attr(form,arg)





  return form



