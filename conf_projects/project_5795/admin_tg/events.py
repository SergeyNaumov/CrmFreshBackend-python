async def permissions(form):
    if not(getattr(form.request.state,'project',None)):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return

    bot=await form.db.query(
        query='SELECT * from bot where project_id=%s',
        values=[form.request.state.project['project_id']],
        onerow=1
    )

    if bot:
       form.bot=bot
       form.foreign_key='bot_id'
       form.foreign_key_value=bot['id']

    else:
        form.errors('У Вас нет ни одного бота')
    
    if form.id:
        form.ov=await form.db.query(
            query="select *,sha1(concat(id,%s,tg_login)) access_key from admin_tg where id=%s",
            values=[bot['token'],form.id],
            onerow=1
        )
    

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