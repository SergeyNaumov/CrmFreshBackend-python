def run_event(form,event_name,arg={}):
    
    
    if 'field' in arg:
      field=arg['field']
      if event_name in field:
        event_func=field[event_name]
        print('run event for field',event_name,field)
        event_func(form,field)
    
    else:
      if event_name in form.events:
        print('events:',form.events)
        event=form.events[event_name]
        print('run_event for form:',event_name)
        print('TYPE:',type(event))
        #event(form)
        if isinstance(event,list):
          print('is list!')
          for e in event:
            e(form,arg)
        else:
          event(form,arg)

