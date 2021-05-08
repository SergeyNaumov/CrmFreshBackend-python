
def events_permissions(form):
  
  for f in form.fields:
    f['read_only']=1



events={
  'permissions':[
      events_permissions
  ],
}