def email_filter_code(form,field,row):
  if not row['email']: row['email']=''
  return row['email']
events={
  'email':{
    'filter_code':email_filter_code
  } 
}