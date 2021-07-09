from lib.core import  date_to_rus
from lib.anna.get_ul_list import get_ul_list_ids
from lib.anna.get_cur_period import get_cur_period
from lib.anna.get_apt_list import get_apt_list_ids
def permissions(form):
  
  params=form.R['cgi_params']
  form.manager['ur_lico_ids']=[]
  form.manager['apt_list_ids']=[]

  if form.script=='edit_form' and form.id and 'cgi_params' in form.R and 'manager_id' in form.R['cgi_params']:
    manager_id=form.R['cgi_params']['manager_id']
    form.manager['ur_lico_ids']=get_ul_list_ids(form,manager_id)
    form.manager['apt_list_ids']=get_apt_list_ids(form,manager_id)

  if form.manager['type']==2:
    form.manager['ur_lico_ids']=get_ul_list_ids(form,form.manager['id'])
    form.manager['apt_list_ids']=get_apt_list_ids(form)
    
  if form.manager['type']==3:
    form.manager['apt_list_ids']=get_apt_list_ids(form)
  if form.script=='edit_form' and form.id and form.action =='edit':
    form.ov=form.db.query(
        query="""
            select
                ap.*, a.date_start, a.date_stop
            from
                action_plan ap
                LEFT join action a ON a.id=ap.action_id
            where ap.id=%s""",
        values=[form.id],
        onerow=1
    )
    if form.ov:
      form.ov['period']={'id':''}

      if 'prev' in params:
        form.ov['period']=get_cur_period(form,1)
      else:
        form.ov['period']=get_cur_period(form)
    
    if form.ov:
      form.title='Маркетинговое мероприятие '+form.ov['header']
    #form.pre(form.ov)

  

events={
  'permissions':[
    permissions
  ],
  'before_search':[

  ]
}