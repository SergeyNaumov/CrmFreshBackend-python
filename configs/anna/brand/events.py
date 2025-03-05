
def events_permissions(form):
  if('superadmin' in form.manager['permissions']):
    form.read_only=0
  
events={
  'permissions':[
      events_permissions
  ],
}