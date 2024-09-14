async def get_bills(form,field, R):

  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if R.get('dogovor_id'):
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
      perm=form.manager['permissions']

      #pprint(form.manager['permissions'])
      # проставляем make_edit_summ:
      for b in lst:

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

       # b['act_list']=

        #from pprint import pprint
        #pprint(b)

  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return lst