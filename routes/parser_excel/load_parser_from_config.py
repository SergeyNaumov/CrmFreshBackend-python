import importlib,os
import copy

def load_parser_from_config(confdir,conflib_dir, arg):
  parser=False
  errors=[]
  if not(os.path.isfile(f"{confdir}/{arg['config']}/__init__.py")):
    errors.append('конфиг не найден')
  if os.path.isdir(f"{confdir}/{arg['config']}") and not(len(errors)):
    try:

      module=importlib.import_module(conflib_dir+'.'+arg['config'])

      parser=copy.deepcopy(module.parser)

    except SyntaxError as e:
      errors.append(f"Ошибка при загрузке конфига {arg['config']}: {e}")
    except ModuleNotFoundError as e:
      errors.append(f"Ошибка при загрузке конфига {arg['config']}: {e}")
    except Exception as e:
      errors.append(f"ошибка при обработке конфига {arg['config']}: {e}")

    if not len(errors) and os.path.isfile(f"{confdir}/{arg['config']}/events.py"):
      try:
        module=importlib.import_module(conflib_dir+'.'+arg['config']+'.events')
        form_data['events']=module.events
      except SyntaxError as e:
        errors.append(f"Ошибка при загрузке конфига {arg['config']}/events.py: {e}")
      except ModuleNotFoundError as e:
        errors.append(f"Ошибка при загрузке конфига {arg['config']}/events.py: {e}")
      except Exception as e:
        errors.append(f"ошибка при обработке конфига {arg['config']}: {e}")

    #if not len(errors):
      #parser=Form(arg)
      #form.load_data(form_data)

    # if not len(errors) and  os.path.isfile(f"{confdir}/{arg['config']}/events_for_fields.py"):
    #   try:
    #     module=importlib.import_module(conflib_dir+'.'+arg['config']+'.events_for_fields')
    #     events=module.events
    #     for f in form.fields:
    #       if 'name' not in f:
    #         form.errors.append(f'{f["description"]}: не указано имя!')
    #         break

    #       if f['name'] in events:
    #         # все возможные события
    #         for event_name in (
    #           'permissions','before_code',

    #           'before_insert', 'before_update', 'before_save',
    #           'before_insert_code', 'before_update_code', 'before_save_code','before_delete_code',

    #           'after_add', # для memo
    #           'after_insert', 'after_update', 'after_save',
    #           'after_insert_code''after_update_code','after_save_code','after_delete_code',

    #           'code','slide_code',

    #           'filter_code',
    #         ):
    #           if event_name in events[f['name']]:
    #             f[event_name]=events[f['name']][event_name]

    #   except SyntaxError as e:
    #       errors.append(f"Ошибка при загрузке конфига {arg['config']}/events_for_fields.py: {e}")
    #   except ModuleNotFoundError as e:
    #       errors.append(f"Ошибка при загрузке конфига {arg['config']}/events_for_fields: {e}")

      #print('FIELDS:',form.fields)


  return [parser,errors]