
def events_permissions(form):
  for f in form.fields:
    f['read_only']=1


def before_search(form):
  #form.pre(form.query_search)
  form.query_search['SELECT_FIELDS'].append('count( distinct a.id) cnt_apt')

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}