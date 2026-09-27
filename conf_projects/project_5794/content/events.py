#def permissions(form):
    #form.s.project_id=0
    #print('EVENTS PERMISSIONS!')
    #print('project_id:',form.s.project_id)
    #if not(getattr(form.request.state,'project',None)) or not(form.s.project_id):
    #    form.errors.append('Доступ запрещён!')
    #    return
    
    #form.foreign_key='project_id'
    #form.foreign_key_value=form.s.project_id
    
    

async def events_before_code(form):
    pass

async def before_delete(form):
    pass
    

events={
  'permissions':[
      #permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}