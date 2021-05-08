from lib.core import exists_arg

def run_event(form,event_name,arg={}):
    
    if not form.success():
      return
      
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
        #print('events:',form.events)
        event=form.events[event_name]
        #print('run_event for form:',event_name)
        #print('TYPE:',type(event))
        #event(form)
        if isinstance(event,list):
          for e in event:
            if arg:
              #print('arg:',arg)
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

