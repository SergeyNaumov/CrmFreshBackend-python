from lib.core import exists_arg
def get_acts(form,field, R):
  if optional_sub:=field.get('get_acts'):
    return optional_sub(form,field,R)

  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if exists_arg('bill_id',R):

    lst=form.db.query(
      query=f"""
        SELECT
          a.id, concat('/edit_form/act/',a.id) link,
          concat('Акт №',a.number,' от ',a.registered,' (',a.summ,' руб)') header
        FROM
          docpack dp
          join bill b ON b.docpack_id=dp.id
          join act a ON a.bill_id=b.id
        WHERE dp.user_id=%s and b.id=%s
        ORDER BY a.id desc
      """,
      values=[form.id, R['bill_id']]
    )

  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return lst

def action_get_acts(form,field, R):
  lst=get_acts(form,field, R)
  return {'success':form.success(),'errors':form.errors, 'list':lst}