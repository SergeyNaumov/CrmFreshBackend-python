from conf.test import Config as config_test
from lib.engine import s
from lib.core import create_fields_hash, exists_arg

configs={
  'test':config_test
}



def read_config(**arg):
  response={}
  
  if not (arg['config'] in configs):
    return {
      'success':0,
      'errors':['Конфиг '+arg['config']+' не найден']
    }
  


  config_class=configs[arg['config']]
  form=config_class(arg)
  form.default_config_attr(arg)
  #default_config_attr(form,arg)





  return form



