async def permissions(form):
    #form.s.project_id=0
    
    #print('PERMISSIONS RUNNED',form.s.project_id)
    if not(getattr(form.request.state,'project',None)):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return 
    bot_id=await form.db.query(
        query='SELECT id from bot where project_id=%s',
        values=[form.request.state.project['project_id']],
        onevalue=1
    )
    #form.pre({'bot_id:': bot_id})
    if bot_id:
       form.foreign_key='bot_id'
       form.foreign_key_value=bot_id
        #form.load_data({'foreign_key':'bot_id','foreign_key_value':form.s.project_id})
    #else:
    #    form.errors.append('Боты не найдены, обратитесь к администратору')
    #print('PERMISSIONS!',form.foreign_key,form.s.project_id  )

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