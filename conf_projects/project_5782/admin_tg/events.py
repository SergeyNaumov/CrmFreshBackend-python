def permissions(form):
    if not(hasattr(form.s,'project_id')) or not(form.s.project_id):
        print('Доступ запрещён!')
        form.errors.append('Доступ запрещён!')
        return

    bot=form.db.query(
        query='SELECT * from bot where project_id=%s',
        values=[form.s.project_id],
        onerow=1
    )

    if bot:
       form.bot=bot
       form.foreign_key='bot_id'
       form.foreign_key_value=bot['id']

    else:
        form.errors('У Вас нет ни одного бота')
    
    if form.id:
        form.ov=form.db.query(
            query="select *,sha1(concat(id,%s,tg_login)) access_key from admin_tg where id=%s",
            values=[bot['token'],form.id],
            onerow=1
        )
    

def events_before_code(form):
    pass

def before_delete(form):
    pass
    

events={
  'permissions':[
      permissions
  ],
  'before_delete':before_delete,
  'before_code':events_before_code
}