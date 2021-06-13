from lib.core import exists_arg

def get_old_values(form):
  ov={}
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
    if not ov['subscribed_ur_lico_id']: ov['subscribed_ur_lico_id']=''
    if not ov['subscribed_apteka_id']: ov['subscribed_apteka_id']=''
    if not ov['requested_ur_lico_id']: ov['requested_ur_lico_id']=''
    ov['subscribed_ur_lico_id']=ov['subscribed_ur_lico_id'].split(',')
    ov['subscribed_apteka_id']=ov['subscribed_apteka_id'].split(',')
    
    print('ov:',ov)
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
  else:
    ov=form.db.query(
      query='select * from action where id=%s',
      values=[form.id],
      onerow=1
    )
    ov['subscribed_ur_lico_id']=[]
    ov['requested_ur_lico_id']=[]
    ov['subscribed_apteka_id']=[]
  
  return ov