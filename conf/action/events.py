
def events_permissions(form):
  #if(form.script=='')
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
  #form.pre(form.script)

  if form.script in ['find_objects']:
    for f in form.fields:
      if f['name']=='date_start':
        f['description']='Период подписки'
      
      if f['name']=='date_stop':
        f['description']='Подписка'

  if form.script=='admin_table':
    form.javascript['admin_table']=form.template(
      './conf/action/templates/admin_table.js',
    )


def before_search(form):
  #form.pre()
  form.query_search['WHERE'].append('wt.date_stop>=curdate()')
  #form.out_before_search.append('<h2 class="subheadling mb-2">История начисления бонусов</h2>')
  #form.query_search

events={
  'permissions':[
      events_permissions
  ],
  'before_search':[
      before_search
  ]
}