# uid = md5(id + header) после вставки (легаси after_insert)
async def after_insert_form_forms(form):
  await form.db.query(
    query='UPDATE form_forms SET uid=md5(concat(id,header)) WHERE id=%s',
    values=[form.id],
    errors=form.errors,
  )


events = {
  'after_insert': [after_insert_form_forms],
}
