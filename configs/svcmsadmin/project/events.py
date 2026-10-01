# События уровня формы.
# permissions -- готовим старые значения (хостинг + структуры) для before_code.
async def load_old_values(form):
  form.old_values = {}
  form.old_struct_public = []
  if not form.id:
    return

  row = await form.db.query(
    query='''
      SELECT ph.size_project, ph.size_template, ph.paid_on_year
      FROM project p
      LEFT JOIN domain d ON d.project_id=p.project_id
      LEFT JOIN project_hosting ph ON ph.domain_id=d.domain_id
      WHERE p.project_id=%s
      LIMIT 1
    ''',
    values=[form.id],
    onerow=1,
    errors=form.errors,
  )
  form.old_values = row or {}

  rows = await form.db.query(
    query='''
      SELECT p.struct_public_id
      FROM struct_public p, project_struct_public st
      WHERE p.struct_public_id=st.struct_public_id
        AND st.project_id=%s
    ''',
    values=[form.id],
    errors=form.errors,
  )
  form.old_struct_public = [r['struct_public_id'] for r in (rows or [])]


# after_insert -- фиксируем дату создания проекта.
async def set_registered(form):
  if not form.id:
    return
  await form.db.query(
    query='UPDATE project SET registered=NOW() WHERE project_id=%s',
    values=[form.id],
    errors=form.errors,
  )


events = {
  'permissions': load_old_values,
  'after_insert': set_registered,
}
