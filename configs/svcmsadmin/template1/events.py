# В легаси template1.permissions всегда разрешал редактирование, но без удаления
async def permissions_template1(form):
  form.read_only = 0
  form.make_delete = 0


# Легаси reset_cache_time: сброс кеша шаблона
async def after_save_template1(form):
  if form.id:
    await form.db.query(
      query='UPDATE template SET reset_cache_time=UNIX_TIMESTAMP() WHERE template_id=%s',
      values=[form.id],
      errors=form.errors,
    )


events = {
  'permissions': [permissions_template1],
  'after_save': [after_save_template1],
}
