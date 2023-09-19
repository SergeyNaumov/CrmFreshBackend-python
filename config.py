import importlib, os

config=None
conf_file=os.getenv('config')

if conf_file:
  module=importlib.import_module(conf_file)
  config=module.config
  #print('config:',config)
else:
  print('Не указан файл конфига!')
  print('Пример запуска:')
  print('export config=[имя_конфига] && uvicorn --reload  --port=5000 --workers 5')

  quit()
