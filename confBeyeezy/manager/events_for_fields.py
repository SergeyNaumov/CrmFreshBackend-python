#def email_filter_code(form,field,row):
#  if not row['email']: row['email']=''
#  return row['email']
def emails_after_save_code(form,field):
  #print('id:',form.id)
  if field['values'] and len(field['values']):
    v=field['values'][0]
    form.db.query(
      query=f"UPDATE manager_email set main=0 where manager_id={form.id} and id<>{v['id']}",
      debug=1
    )

def password_before_code(form,field):
  ...

events={
  #'email':{
  #  'filter_code':email_filter_code
  #},
  'password':{
    'before_code': password_before_code
  },
  'emails':{
    'after_save_code': emails_after_save_code
  }
}