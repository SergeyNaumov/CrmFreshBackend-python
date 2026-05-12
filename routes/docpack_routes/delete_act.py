from lib.core_crm import get_manager, get_owner
from lib.core import exists_arg
async def action_delete_act(form,field,R):

  act_id=exists_arg('act_id',R)
  db=form.db
  perm=form.manager['permissions']
  perm['make_delete_act_paids']=True
  if not(act_id):
    form.errors.append('отсутствует параметр act_id')

  

  if form.success():
    act=await db.query(
      query="SELECT * from act where id=%s",
      values=[act_id],
      onerow=1
    )
    if act:
      # менежер акта
      act_manager=await get_manager(db=db, id=act['manager_id'])
      #print('act_manager:',act_manager, act['manager_id'])

      # руководитель менеджера акта
      act_owner=None
      if act['manager_id']:
        act_owner=await get_owner(db=db, manager_id=act['manager_id'])

      make_delete=False
      if act_manager and act_manager['id']==form.manager['id']:
        # менеджер акта
        make_delete=True

      elif act_owner and act_owner==form.manager['id']:
        # руководитель менеджера платежа
        make_delete=True

      elif perm.get('make_delete_act_paids'):
        make_delete=True

      else:
        make_delete=False

      if make_delete:
        await db.query(
          query='delete from act where id=%s',
          values=[act_id]
        )
      else:
        form.errors.append('Вам запрещено удалять этот акт')

    else:
      form.errors.appent('акт не найден')


  return {'success':form.success(),'errors':form.errors}
