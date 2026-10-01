# В легаси template.pl permissions всегда разрешал редактирование
#from config import config as cfg
async def permissions_template(form):
  form.read_only = 0
  form.make_delete = 1
  
  if form.action=='fast_rule' and form.id:
    form.response={
      'success':True,
      'data': await form.db.query(query="SELECT run_code FROM fast_rule where fast_rule_id=%s",values=[form.id],onevalue=1)
    }
    


# Легаси reset_cache_time: сброс кеша шаблона (без shell-очистки nginx)
async def after_save_template(form):
  if form.id:
    await form.db.query(
      query='UPDATE template SET reset_cache_time=UNIX_TIMESTAMP() WHERE template_id=%s',
      values=[form.id],
      errors=form.errors,
    )


events = {
  'permissions': [permissions_template],
  'after_save': [after_save_template],
}
