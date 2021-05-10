
def events_permissions(form):
  if form.id:
    form.ov=form.db.query(
      query='select * from action where id=%s',
      values=[form.id],
      onerow=1
    )

    if form.ov:
      form.title='Маркетинговое мероприятие '+form.ov['header']

  new_fields=[]
  for f in form.fields:
    f['read_only']=1
    if form.id:
      if not (f['name'] in ['date_start','date_stop']):
         new_fields.append(f)

      if  f['name'] =='date_stop':
        new_fields.append({
          'description':'Даты подписки',
          'type':'code',
          'after_html':f'<p><b>Дата подписки:</b> {form.ov["date_start"]} - {form.ov["date_stop"]}</p>',
          'name':'dates'
        })
    else:
      new_fields.append(f)

  form.fields=new_fields

events={
  'permissions':[
      events_permissions
  ],
}