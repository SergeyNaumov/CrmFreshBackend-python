from lib.core import exists_arg
def permissions(form):
  if form.id:
    form.ov=form.db.query(
      query=f'select * from {form.work_table} where {form.work_table_id}={form.id}',
      onerow=1
    )

  perm = form.manager['permissions']
  
  #if not exists_arg('blank_document',perm):
  #  form.errors.append('Доступ запрещён!')

def after_save(form):
  form.db.query(
    query=f'UPDATE blank_document set registered=now() where id = {form.id}'
  )
  

events={
  'permissions':permissions,
  'after_save': after_save
}