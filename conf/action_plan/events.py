from lib.anna.get_ul_list import get_ul_list_ids
def permissions(form):
  if form.manager['type']==2:
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
  #form.pre(form.manager)

  

events={
  'permissions':[
    permissions
  ],
  'before_search':[

  ]
}