from lib.core import exists_arg
import traceback

def run_event(form,event_name,arg={}):
    
    if not form.success():
      return
    
    #print('RUN EVENT:',event_name,arg)  

    if arg and 'field' in arg:
      field=arg['field']
      if event_name in field: # Если мы в аргументах передаём поле -- событие ищем внутри этого поля
        event_func=field[event_name]
        try:
          if event_name in ('slide_code', 'after_add'):
            data=exists_arg('data',arg) or {}
            return event_func(form,field,data)
          else:
            return event_func(form,field)
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
                e(form,arg)
              else:
                e(form)
            except Exception as e:
              err=traceback.format_exc()

              form.errors.append(f"ошибка в событии {event_name}: {err}")
        else:

          try:
            if arg:
              event(form,arg)
            else:
              event(form)
          except AttributeError as e:
            err=traceback.format_exc()

            form.errors.append(f"ошибка в событии {event_name}: {err}")

