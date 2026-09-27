async def permissions(form):
    if not(getattr(form.request.state,'project',None)):
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

    photo_field=form.get_field('photo')
    photo_field['filedir']=f"./files/project_{form.request.state.project['project_id']}/bot_subscribe"


    
    

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