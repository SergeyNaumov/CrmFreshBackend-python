#def email_filter_code(form,field,row):
#  if not row['email']: row['email']=''
#  return row['email']
async def emails_after_save_code(form,field):
  #print('id:',form.id)
  if field['values'] and len(field['values']):
    v=field['values'][0]
    await form.db.query(
      query=f"UPDATE manager_email set main=0 where manager_id={form.id} and id<>{v['id']}",
    )
  
async def email_filter_code(form,field,row):
  return row['email']

events={
  #'email':{
  #  'filter_code':email_filter_code
  #},
  'emails':{
    'after_save_code': emails_after_save_code,
  },
  'email':{
    'filter_code':email_filter_code
  }
}
