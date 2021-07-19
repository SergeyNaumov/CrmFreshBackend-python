from lib.core import  date_to_rus
from lib.anna.get_ul_list import get_ul_list_ids
from lib.anna.get_cur_period import get_cur_period
from lib.anna.get_apt_list import get_apt_list_ids, get_all_ids_for_aptcomp
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

    if len(form.manager['apt_list_ids']):
      apteka_id=form.manager['apt_list_ids'][0]
      form.manager['apteka_settings']=form.db.query(
        query='select set1,set2 from apteka_settings where apteka_id=%s',
        values=[apteka_id],
        onerow=1
      )
      
    else:
      form.manager['apteka_settings']={
        'set1':1,'set2':1
      }
    if form.manager['apteka_settings']['set2']:
      form.manager['apt_list_ids']=get_all_ids_for_aptcomp(form,apteka_id)

    #form.pre(form.manager)
    #apteka_settings

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
    #form.pre(form.ov)
    if form.ov:
      form.ov['period']={'id':''}
      form.ov['total_good_price']=form.db.query(
        query='select sum(price) from action_plan_good apg join good g on g.id=apg.good_id where apg.action_plan_id=%s',
        values=[form.id],
        onevalue=1
      )

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