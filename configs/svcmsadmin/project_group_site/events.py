# Легаси project_group_site.permissions: создаём запись настроек, если её ещё нет
async def permissions_project_group_site(form):
  if form.script != 'edit_form':
    return
  if not str(form.id).isdigit():
    form.errors.append('Некорректный вызов')
    return

  count = await form.db.query(
    query='SELECT count(*) FROM project_group_site WHERE project_id=%s',
    values=[form.id],
    onevalue=1,
    errors=form.errors,
  )
  if not count:
    await form.db.save(
      table='project_group_site',
      data={'project_id': form.id},
      errors=form.errors,
    )


events = {
  'permissions': [permissions_project_group_site],
}
