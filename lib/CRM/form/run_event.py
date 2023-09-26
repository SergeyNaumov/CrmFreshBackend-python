from lib.core import exists_arg

def run_event(form,event_name,arg={}):
    
    if not form.success():
      return
    
    #print('RUN EVENT:',event_name,arg)  

    if arg and 'field' in arg:
      field=arg['field']
      if event_name in field: # Если мы в аргументах передаём поле -- событие ищем внутри этого поля
        event_func=field[event_name]
        
        if event_name=='slide_code':
          data=exists_arg('data',arg) or {}
          return event_func(form,field,data)
        else:
          return event_func(form,field)
    
    else:

      if event_name in form.events:
        event=form.events[event_name]

        if isinstance(event,list):

          for e in event:
            if arg:
              e(form,arg)
            else:
              e(form)
        else:

          try:
            if arg:
              event(form,arg)
            else:
              event(form)
          except AttributeError as e:
            form.errors.append(str(e))

