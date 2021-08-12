from lib.anna.get_ul_list import get_ul_list_ids

def events_permissions(form):
  for f in form.fields:
    f['read_only']=1

def before_search_tables(form):
  qs=form.query_search
  #form.out_before_search.append('<h2 class="subheadling mb-2">История начисления бонусов</h2>')
  #form.pre(form.query_search['WHERE'])
  
  R=form.R
  if form.manager['type']==2:
    #form.explain=1
    ur_lico_ids=get_ul_list_ids(form,form.manager['id'])
    qs['WHERE'].append(f"partner_id in ({','.join(ur_lico_ids)})")
  
  qs['on_filters_hash']['attach']=[]
  R['query'].append(['attach',[]])


events={
  'permissions':[
      events_permissions
  ],
  'before_search_tables':before_search_tables
}