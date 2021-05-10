def events_permissions(form):
  if form.id:
    form.ov=form.db.query(
      query=f'''
        SELECT
          wt.id, wt.date, wt.manufacturer_id, wt.action_id,
          a.header action, man.header manufacturer

        FROM
          purchase wt
          LEFT JOIN action a ON a.id=wt.action_id
          LEFT JOIN manufacturer man ON man.id=wt.manufacturer_id
        WHERE wt.id={form.id}
      ''',
      onerow=1
    )
    
  for f in form.fields:
    f['read_only']=1

events={
  'permissions':[
      events_permissions
  ],
}