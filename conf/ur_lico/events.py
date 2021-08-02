
def events_permissions(form):
  for f in form.fields:
    f['read_only']=1


def before_search(form):
  qs=form.query_search
  qs['SELECT_FIELDS'].append('count( distinct a.id) cnt_apt')
  

  if 'manager_id' in qs['on_filters_hash'] and qs['on_filters_hash']['manager_id']:
    qs['WHERE'].append('concat(m1.login," ",m1.name) like %s')
    qs['VALUES'].append('%'+qs['on_filters_hash']['manager_id']+'%')
    
  qs['SELECT_FIELDS'].append('group_concat(distinct concat(m1.login," ",m1.name) SEPARATOR ";<br>") as pred_ul')
    #pass
  #form.pre(qs)
  #form.pre(qs['on_filters_hash']['manager_id'])

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}