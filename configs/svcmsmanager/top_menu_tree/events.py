async def permissions(form):
    project_id=form.request.state.project['project_id']
    if not project_id:
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return 
    
    form.foreign_key='project_id'
    form.foreign_key_value=project_id  
    form.load_data({'foreign_key':'project_id','foreign_key_value':project_id})
    print('PERMISSIONS!',form.foreign_key,project_id  )

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