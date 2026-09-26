async def permissions(form):
    if form.id:
        form.ov=await form.db.query(
            query=f"select * from {form.work_table} where id={form.id}",
            onerow=1
        )
        if form.ov:
            form.title=f"Блок: {form.ov['header']}"

    project_id=form.request.state.project['project_id']
    if not project_id:
        form.errors.append('Доступ запрещён!')
        return 
    
    #form.foreign_key='project_id'
    #form.foreign_key_value=project_id
    
    

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