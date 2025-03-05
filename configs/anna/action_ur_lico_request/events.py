
def events_permissions(form):
  
  if form.manager['type'] == 1:
    form.make_delete=1
  else:
    for f in form.fields:
      f['read_only']=1



events={
  'permissions':[
      events_permissions
  ],
}