# allow в легаси project_permission.pl был hidden со значением 1
async def set_allow(form):
  form.new_values['allow']=1


events = {
  'before_insert': [set_allow],
  'before_update': [set_allow],
}
