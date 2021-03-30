
def events_permissions(form):
  if(form.id):
    form.get_values()
    #form.log.append(form.values)
    #form.log.append(form.manager)
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

    #form.log.append('is_owner: ' + str(form.is_owner) )
    if not (form.manager['login'] == 'admin'):
      form.read_only=1

events={
  'permissions':[
      events_permissions
  ],
}