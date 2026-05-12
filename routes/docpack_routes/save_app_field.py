from lib.core import exists_arg
async def save_app_field(form,field, R):
  #print('save_summ_bill!')
  app_id=R.get('app_id')
  field_id=R.get('field_id')
  value=R.get('value')
  if form.id:
    db=form.db
    await db.query(
      query="UPDATE dogovor_app_values set value=%s WHERE id=%s and dogovor_app_id=%s",
      values=[value, field_id,app_id]
    )
    return {
      'success':form.success(),
      'errors': form.errors
    }