from lib.anna.get_apt_list import get_apt_list_ids

def events_permissions(form):
  
  for f in form.fields:
    f['read_only']=1

  if form.manager['type']==2:
    #form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
    form.manager['apt_list_ids']=get_apt_list_ids(form)
  
  #form.pre(form.manager)

def before_search(form):
    qs=form.query_search
    if form.manager['type']==2:
        qs['WHERE'].append(f'''wt.apteka_id in ({','.join(form.manager['apt_list_ids'])})''')
    #form.pre(qs)
    #apt_list_ids
events={
  'permissions':[
      events_permissions
  ],
  'before_search':[
      before_search
  ]
}