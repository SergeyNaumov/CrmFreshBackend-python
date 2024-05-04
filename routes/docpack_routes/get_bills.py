from lib.core import exists_arg
async def get_bills(form,field, R):
  if optional_sub:=field.get('get_bills'):
    return await optional_sub(form,field,R)

  docpack_foreign_key=field['docpack_foreign_key']
  lst=[]
  if exists_arg('dogovor_id',R):
      lst=await form.db.query(
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
      #for l in lst:
      #  l['act_list']=[]

  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return lst

async def action_get_bills(form,field, R):
  lst = await get_bills(form,field, R)
  return {'success':form.success(),'errors':form.errors, 'list':lst}