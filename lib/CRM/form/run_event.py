from lib.core import exists_arg
import traceback
import inspect

async def run_event(form,event_name,arg={}):
    
    if not form.success():
      return
    
    if arg and 'field' in arg:
      field=arg['field']
      if event_name in field: # Если мы в аргументах передаём поле -- событие ищем внутри этого поля
        event_func=field[event_name]
        try:
          # data передаём третьим аргументом, если обработчик его принимает
          # (before_/after_*_code). Иначе вызываем с двумя (form, field).
          data=exists_arg('data',arg)
          try:
            nparams=len(inspect.signature(event_func).parameters)
          except (TypeError, ValueError):
            nparams=2
          if data is not None and nparams>=3:
            return await event_func(form,field,data)
          return await event_func(form,field)
        except Exception as e:
          err=traceback.format_exc()

          form.errors.append(f"ошибка в событии {event_name}: {err}")
    else:

      if event_name in form.events:
        event=form.events[event_name]
        
        if isinstance(event,list):
          for e in event:
            try:
              if arg:
                await e(form,arg)
              else:
                await e(form)
            except Exception as e:
              err=traceback.format_exc()

              form.errors.append(f"ошибка в событии {event_name}: {err}")
        else:
          try:
            if arg:
              await event(form,arg)
            else:
              #print('event_name:',event_name)
              await event(form)
          except AttributeError as e:
            err=traceback.format_exc()

            form.errors.append(f"ошибка в событии {event_name}: {err}")

