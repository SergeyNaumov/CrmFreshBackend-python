from lib.anna.get_apt_list import get_apt_list_ids
def events_permissions(form):
  
  for f in form.fields:
    f['read_only']=1
  if form.manager['type']==3:
    form.errors.append('доступ запрещён!')

def before_search(form):
  if form.manager['type']==2:
    apt_list_ids=get_apt_list_ids(form,form.manager['id'])
    if not len(apt_list_ids):
      apt_list_ids=['0']

    form.query_search['WHERE'].append('wt.id in ('+','.join(apt_list_ids)+')')
    #form.pre(form.query_search['WHERE'])
    


events={
  'permissions':[
      events_permissions
  ],
  'before_search':[
      before_search
  ]
}