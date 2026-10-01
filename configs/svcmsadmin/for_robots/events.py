# Легаси robots_txt_permissions: при открытии карточки создаём запись, если её нет
async def permissions_for_robots(form):
  if form.script != 'edit_form' or not form.id:
    return
  count = await form.db.query(
    query='SELECT count(*) FROM for_robots_id WHERE domain_id=%s',
    values=[form.id],
    onevalue=1,
    errors=form.errors,
  )
  if not count:
    await form.db.save(
      table='for_robots_id',
      data={'domain_id': form.id},
      errors=form.errors,
    )


events = {
  'permissions': [permissions_for_robots],
}
