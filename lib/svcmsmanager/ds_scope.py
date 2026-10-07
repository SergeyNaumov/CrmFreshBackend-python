"""Guard'ы принадлежности записи проекту для ds-конфигов.

Регистрируются в conf/ds_*/events.py как before_code / before_update /
before_delete. Работают только если у формы заданы foreign_key и
foreign_key_value (проектная привязка; value задаёт events.permissions).

Смысл: админ одного проекта не должен открывать/менять/удалять записи другого
проекта, подменив id.
"""


def _scoped(form):
  """foreign_key задан и есть значение проекта?"""
  fk = getattr(form, 'foreign_key', '') or ''
  fkv = getattr(form, 'foreign_key_value', '')
  return fk, fkv


async def scope_on_read(form):
  """before_code: загруженная запись (form.values) принадлежит текущему проекту?"""
  fk, fkv = _scoped(form)
  if not (fk and fkv not in ('', None, 0, '0') and getattr(form, 'id', None)):
    return

  val = None
  values = getattr(form, 'values', None)
  if isinstance(values, dict) and fk in values:
    val = values.get(fk)
  elif getattr(form, 'db', None) and getattr(form, 'work_table', ''):
    val = await form.db.query(
      query=f'SELECT {fk} FROM {form.work_table} WHERE {form.work_table_id}=%s',
      values=[form.id], onevalue=1, errors=[],
    )

  if val is not None and str(val) != str(fkv):
    form.errors.append('Запись принадлежит другому проекту. Действие запрещено.')


async def _scope_check(form):
  """Строка с таким id существует и принадлежит текущему проекту?"""
  fk, fkv = _scoped(form)
  if not (fk and fkv not in ('', None, 0, '0') and getattr(form, 'id', None)):
    return
  cnt = await form.db.query(
    query=(f'SELECT COUNT(*) FROM {form.work_table} '
           f'WHERE {form.work_table_id}=%s AND {fk}=%s'),
    values=[form.id, fkv], onevalue=1, errors=[],
  )
  if not cnt:
    form.errors.append('Запись принадлежит другому проекту. Действие запрещено.')


async def scope_before_update(form):
  await _scope_check(form)


async def scope_before_delete(form):
  await _scope_check(form)
