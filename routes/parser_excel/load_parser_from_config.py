import importlib,os, inspect
import copy

async def load_parser_from_config(confdir,conflib_dir, arg):
  parser=False
  errors=[]
  if not(os.path.isfile(f"{confdir}/{arg['config']}/__init__.py")):
    errors.append('конфиг не найден')
  if os.path.isdir(f"{confdir}/{arg['config']}") and not(len(errors)):
    try:
      #print('PARSER - 0: ', conflib_dir.replace('/','.')+'.'+arg['config'])
      module=importlib.import_module(conflib_dir.replace('/','.')+'.'+arg['config'])
      #print('PARSER - 1')
      if inspect.iscoroutinefunction(module.get_parser):
        parser=await module.get_parser()
      else:
        parser=module.get_parser()

      #print('PARSER: ',parser)
    except SyntaxError as e:
      errors.append(f"Ошибка при загрузке конфига -1 {arg['config']}: {e}")
    except ModuleNotFoundError as e:
      errors.append(f"Ошибка при загрузке конфига -2 {arg['config']}: {e} / {conflib_dir}.{arg['config']} ")
    except Exception as e:
      errors.append(f"ошибка при обработке конфига -3 {arg['config']}: {e}")

    if not len(errors) and os.path.isfile(f"{confdir}/{arg['config']}/events.py"):
      try:
        module=importlib.import_module(conflib_dir+'.'+arg['config']+'.events')
        form_data['events']=module.events
      except SyntaxError as e:
        errors.append(f"Ошибка при загрузке конфига -4 {arg['config']}/events.py: {e}")
      except ModuleNotFoundError as e:
        errors.append(f"Ошибка при загрузке конфига -5 {arg['config']}/events.py: {e}")
      except Exception as e:
        errors.append(f"ошибка при обработке конфига -6 {arg['config']}: {e}")


  return [parser,errors]

def load_parser_from_config_sync(confdir, conflib_dir, arg):
  parser = False
  errors = []
  form_data = {}  # Добавил, так как form_data используется в коде
  print(f'confdir: {confdir}')
  if not os.path.isfile(f"{confdir}/{arg['config']}/__init__.py"):
      errors.append('конфиг не найден')
  
  if os.path.isdir(f"{confdir}/{arg['config']}") and not len(errors):
      try:
          module = importlib.import_module(conflib_dir.replace('/', '.') + '.' + arg['config'])
          # Убрали await, вызываем синхронно
          parser = module.get_parser()
          
      except SyntaxError as e:
          errors.append(f"Ошибка при загрузке конфига -1 {arg['config']}: {e}")
      except ModuleNotFoundError as e:
          errors.append(f"Ошибка при загрузке конфига -2 {arg['config']}: {e} / {conflib_dir}.{arg['config']} ")
      except Exception as e:
          errors.append(f"ошибка при обработке конфига -3 {arg['config']}: {e}")

      if not len(errors) and os.path.isfile(f"{confdir}/{arg['config']}/events.py"):
          try:
              module = importlib.import_module(conflib_dir + '.' + arg['config'] + '.events')
              form_data['events'] = module.events
          except SyntaxError as e:
              errors.append(f"Ошибка при загрузке конфига -4 {arg['config']}/events.py: {e}")
          except ModuleNotFoundError as e:
              errors.append(f"Ошибка при загрузке конфига -5 {arg['config']}/events.py: {e}")
          except Exception as e:
              errors.append(f"ошибка при обработке конфига -6 {arg['config']}: {e}")
  
  return parser, errors