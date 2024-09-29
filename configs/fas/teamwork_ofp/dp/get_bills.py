def process_bill_list(form, _list):
    perm=form.manager['permissions']
    for b in _list:
      # Разрешаем редактировать сумму счёта если:
      if perm.get('admin_paids'):
          # Если это менеджер платежей
          b['make_edit_summ']=True
      elif not(b['paid']) and (b['manager_id']==form.manager['id'] or form.manager['CHILD_GROUPS_HASH'].get(b['group_id']) ) :
          # или менеджер платежа
          # или руководитель менелжера платежа
          b['make_edit_summ']=True
      else:
          b['make_edit_summ']=False

async def get_bills(form,field, R):
  """
    Возвращает все счета и приложения к договору (с привязанными счетами)
  """
  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if R.get('dogovor_id'):
      bill_list=[]
      bill_for_apps_dict={}
      lst = await form.db.query(
        query=f"""
          SELECT
              b.*
          from
              docpack dp
              JOIN bill b ON b.docpack_id=dp.id
          where
              dp.{docpack_foreign_key}=%s and b.docpack_id=%s
          order by b.id desc
        """,
        values=[form.id, R['dogovor_id']]
      )
      process_bill_list(form, lst)

      for b in lst:
        if b['dogovor_app_id']==0:
          bill_list.append(b)
        else:
          if not(b['dogovor_app_id'] in bill_for_apps_dict):
            bill_for_apps_dict[b['dogovor_app_id']]=[]

          bill_for_apps_dict[b['dogovor_app_id']].append(b)

      apps_list = await form.db.query(
        query="select * from dogovor_app where dogovor_id=%s",
        values=[R['dogovor_id']]
      )

      for a in apps_list:
        a['bills']=bill_for_apps_dict.get(a['id'],[])


  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return lst, apps_list