from lib.core import exists_arg
from lib.anna.get_apt_list import get_apt_list_ids, get_apt_list
def get_old_values(form):
  ov={}
  form.apteka_subscribe=[]
  form.ur_lico_subscribe=[]

  #print('apt_list_ids:',form.manager['apt_list_ids'])
  if form.manager['type']==2:
    apt_list_ids=','.join(form.manager['apt_list_ids'])
    ur_lico_ids=','.join(form.manager['ur_lico_ids'])
    query=f'''
            SELECT
              wt.*,
              group_concat(distinct aul.ur_lico_id) subscribed_ur_lico_id,
              group_concat(distinct aul_r.ur_lico_id) requested_ur_lico_id,
              group_concat( distinct aa.apteka_id) subscribed_apteka_id
            FROM
              action wt
              LEFT JOIN action_ur_lico as aul ON (aul.action_id=wt.id and aul.ur_lico_id in ({ ur_lico_ids }))
              LEFT  JOIN action_ur_lico_request as aul_r ON (aul_r.action_id=wt.id and aul_r.ur_lico_id in ({ ur_lico_ids }))
              LEFT  JOIN action_apteka as aa ON (wt.id=aa.action_id and aa.apteka_id in ({ apt_list_ids }))
            WHERE wt.id=%s
            GROUP BY wt.id
        
        '''

    ov=form.db.query(
        query=query,
        #errors=form.errors,
        #debug=1,
        onerow=1,
        values=[form.id]
    )
    if not ov: return
    ov['subscribed_on_action']=0
    if ov['subscribed_ur_lico_id']:
      ov['subscribed_ur_lico_id']=ov['subscribed_ur_lico_id'].split(',')
    else:
      ov['subscribed_ur_lico_id']=[]

    if ov['subscribed_apteka_id']:
      ov['subscribed_apteka_id']=ov['subscribed_apteka_id'].split(',')
    else:
      ov['subscribed_apteka_id']=[]
    
    if ov['requested_ur_lico_id']:
      ov['requested_ur_lico_id']=ov['requested_ur_lico_id'].split(',')
    else:
      ov['requested_ur_lico_id']=[]
    




    #print('ov:',ov)
    for u in form.manager['ur_lico_list']:
      v=0
      if str(u['id']) in ov['subscribed_ur_lico_id']: v=2 # подписанных
      elif str(u['id']) in ov['requested_ur_lico_id']: v=1 # отправил запрос на подписку
      else: v=0

      form.ur_lico_subscribe.append(
        {
          'id':u['id'],
          'action_id':form.id,
          'v':str(v),
          'name':u['name'],
          'apt_cnt':len(list(set(u['apt_ids']) & set(ov['subscribed_apteka_id'])))
        }
      )
  

    if len(ov['subscribed_ur_lico_id']):
      ov['subscribed_on_action']=1
  elif form.manager['type']==3:
    
    form.manager['apt_list_ids']=get_apt_list_ids(form)
    form.manager['apt_list']=get_apt_list(form)
    apt_list_ids=form.manager['apt_list_ids']
    #form.pre(form.manager['apt_list_ids'])
    #form.pre();
    
    ov=form.db.query(
        query=f'''
          select
            wt.*, 
            if(group_concat( distinct aa.apteka_id),1,0) subscribed_apteka_id,
            if(group_concat(distinct aa_r.apteka_id),1,0) requested_apteka_id
          from
            action wt
            LEFT JOIN action_apteka_request as aa_r ON (aa_r.action_id=wt.id and aa_r.apteka_id in ({ ','.join(apt_list_ids) }))
            LEFT  JOIN action_apteka as aa ON (wt.id=aa.action_id and aa.apteka_id in ({ ','.join(apt_list_ids) }))
          where wt.id={form.id} group by wt.id 
      ''',
        debug=form.log,
        onerow=1
      )
    ov['apteka_id']=form.manager['apteka_settings']['id']




    ov['subscribed_on_action']=0

    



      
      

  else:
    ov=form.db.query(
      query='''
        select
          wt.*
        from
          action wt
        where wt.id=%s
      ''',
      values=[form.id],
      onerow=1
    )
    ov['subscribed_on_action']=0
    ov['subscribed_ur_lico_id']=[]
    ov['requested_ur_lico_id']=[]
    ov['subscribed_apteka_id']=[]
  
  return ov