from lib.core_crm import get_manager, get_owner
def get_acts(form,field, R):
  db=form.db
  perm=form.manager['permissions']

  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if R.get('bill_id'):
    lst=db.query(
      query="""
        SELECT
          a.id, concat('/edit_form/act/',a.id) link,
          concat('Акт №',a.number,' от ',DATE_FORMAT(a.registered,%s),' (',a.summ,' руб)') header,
          a.manager_id
        FROM
          docpack dp
          join bill b ON b.docpack_id=dp.id
          join act a ON a.bill_id=b.id
        WHERE dp.user_id=%s and b.id=%s
        ORDER BY a.id desc
      """,
      values=['%d.%m.%y',form.id, R['bill_id']]
    )


    #perm['make_delete_act_paids']=True

    for act in lst:

      # менежер акта
      act_manager=get_manager(db=db, id=act['manager_id'])
      #print('act_manager:',act_manager, act['manager_id'])

      # руководитель менеджера акта
      act_owner=None
      if act['manager_id']:
        act_owner=get_owner(db=db, manager_id=act['manager_id'])

      if act_manager and act_manager['id']==form.manager['id']:
        # менеджер акта
        act['make_delete']=True

      elif act_owner and act_owner==form.manager['id']:
        # руководитель менеджера платежа
        act['make_delete']=True

      elif perm.get('make_delete_act_paids'):
        act['make_delete']=True

      else:
        act['make_delete']=False

  else:
    form.errors.append('отсутствует параметр bill_id')
  return lst