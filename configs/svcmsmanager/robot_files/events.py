async def permissions(form):
    #print('EVENTS PERMISSIONS!')
    project_id=form.request.state.project['project_id']
    if not project_id:
        form.errors.append('Доступ запрещён!')
        return 
    
    form.foreign_key='project_id'
    form.foreign_key_value=project_id
    
    

async def events_before_code(form):
    pass

async def before_delete(form):
    pass
    

events={
  'permissions':[
      permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}