async def admin_id_by_login(form):
  login = form.request.state.manager.get('login')
  return await form.db.query(
    query='SELECT admin_id FROM admin WHERE login=%s',
    values=[login],
    onevalue=1,
    errors=form.errors,
  )


# Каждый админ видит и создаёт только свои быстрые правила
async def permissions_fast_rule(form):
  admin_id = await admin_id_by_login(form)
  if admin_id:
    form.add_where = f'wt.admin_id={admin_id}'


async def before_insert_fast_rule(form):
  admin_id = await admin_id_by_login(form)
  if admin_id:
    form.new_values['admin_id'] = admin_id


events = {
  'permissions': [permissions_fast_rule],
  'before_insert': [before_insert_fast_rule],
}
