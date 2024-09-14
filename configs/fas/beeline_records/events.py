from lib.core import join_ids

def seconds_to_hhmmss(seconds):
  hours = seconds // 3600
  minutes = (seconds % 3600) // 60
  seconds = seconds % 60
  return f"{hours}:{minutes}:{seconds}"

async def permissions(form):
  add_where=[]
  manager=form.manager ; login=manager.get('login')
  if login in ('sed','pzm','akulov','admin'):
    ...
  elif manager.get('is_owner') and len(manager['CHILD_GROUPS']):
    # Если это руководитель, то ограничение по своим группам
    add_where.append(f"m.group_id in ({join_ids(manager['CHILD_GROUPS'])})")
  else:
    add_where.append(f"m.id={manager['id']}")

  if len(add_where):
    form.add_where=' AND '.join(add_where)

async def after_save(form):
    pass
    # form.nv=get_values(form)
    # #print('nv:',form.nv)
async def before_search(form):
  qs=form.query_search
  tables="\n".join(qs['TABLES'])
  if len(qs['WHERE']): # and form.manager['login']=='admin':
    query=f"""
      select
        m.name, sum(if(wt.direction='INBOUND',duration,0)) inbound, sum(if(wt.direction='OUTBOUND',duration,0)) outbound
      FROM
        {tables}
      WHERE {' AND '.join(qs['WHERE'])} GROUP BY wt.manager_id ORDER BY m.name
    """

    total_result = await form.db.query(
      query=query,
      values=qs['VALUES']
    )
    total_inbound=0 ; total_outbound=0
    for t in total_result:
      total_inbound+=t['inbound'] ; total_outbound+=t['outbound']
      t['total']=seconds_to_hhmmss(t['inbound']+t['outbound'])

      t['inbound']=seconds_to_hhmmss(t['inbound'])
      t['outbound']=seconds_to_hhmmss(t['outbound'])


    total=seconds_to_hhmmss(total_inbound+total_outbound)
    total_inbound=seconds_to_hhmmss(total_inbound)
    total_outbound=seconds_to_hhmmss(total_outbound)

    form.out_before_search=[form.template(
      './conf/beeline_records/templates/before_search.html',
      list=total_result, total_inbound=total_inbound, total_outbound=total_outbound,
      total=total
    )]

events={
  'permissions':[
      permissions,
      
  ],
  'after_save':after_save,
  'before_search':before_search
}