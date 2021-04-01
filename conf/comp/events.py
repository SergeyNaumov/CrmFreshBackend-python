
def events_permissions(form):
  
  if ('superadmin' in form.manager['permissions']):
      form.is_admin=1
      form.read_only=0
      form.make_delete=1
  else:
      form.is_admin=0


  if (form.manager['type'] == "1"  ) or form.is_admin:
      form.read_only=0
  
  if(form.id):
    form.get_values()
    
    form.is_owner=0
    
    if(form.manager['id'] == form.values['manager_id']):
      #form.log.append('is_owner: ' + str(form.is_owner) )
      form.is_owner=1
      form.fields.insert(0,{
        'description':'',
        'name':'links',
        'type':'code',
        'after_html':f'<a href="/edit-form/order_change_company?comp_id={form.id}" target="_blank">Создать заявку на изменение данных</a>'
      })



events={
  'permissions':[
      events_permissions
  ],
}