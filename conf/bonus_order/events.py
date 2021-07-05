from lib.anna.get_ul_list import get_ul_list_ids

def events_permissions(form):
  for f in form.fields:
    f['read_only']=1

def before_search(form):
  form.out_before_search.append('<h2 class="subheadling mb-2">История начисления бонусов</h2>')
  #form.pre(form.query_search['WHERE'])

  if form.manager['type']==2:
    #form.explain=1
    ur_lico_ids=get_ul_list_ids(form,form.manager['id'])
    form.query_search['WHERE'].append(f"partner_id in ({','.join(ur_lico_ids)})")

events={
  'permissions':[
      events_permissions
  ],
  'before_search':before_search
}