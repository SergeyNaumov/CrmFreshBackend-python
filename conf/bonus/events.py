def events_permissions(form):
  for f in form.fields:
    f['read_only']=1

def before_search(form):
  form.out_before_search.append('<h2 class="subheadling mb-2">История начисления бонусов</h2>')

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}