import re


# Права: редактировать могут только timonenkova/isavnin (легаси workers.conf)
async def permissions_workers(form):
  login = (form.request.state.manager or {}).get('login') or ''
  if re.search(r'(t|T)imonenkova|isavnin', login):
    form.make_delete = 1
    form.read_only = 0
    form.not_create = 0
  else:
    form.make_delete = 0
    form.read_only = 1
    form.not_create = 1


# Пишем историю изменений оклада/плана/процента (легаси before_update)
async def before_update_workers(form):
  fields = (
    ('oklad', 'worker_oklads'),
    ('plan', 'worker_plan'),
    ('percent', 'worker_percent'),
  )
  for name, table in fields:
    new_value = form.new_values.get(name)
    old_value = form.values.get(name)
    if str(new_value) != str(old_value):
      await form.db.query(
        query=f'INSERT INTO {table}(user_id,value) VALUES(%s,%s)',
        values=[form.id, old_value],
        errors=form.errors,
      )


events = {
  'permissions': [permissions_workers],
  'before_update': [before_update_workers],
}
