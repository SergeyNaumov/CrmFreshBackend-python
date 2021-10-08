from lib.anna.get_apt_list import get_apt_list_ids

def events_permissions(form):
  
  for f in form.fields:
    f['read_only']=1

  if form.manager['type'] in (1,2):
    form.make_delete=1
    form.read_only=0
  
  if form.manager['type']==2:
    form.manager['apt_list_ids']=get_apt_list_ids(form)


  if form.id:
    form.ov=form.db.query(
      query=f'select * from {form.work_table} where id={form.id}',
      onerow=1
    )

  #form.pre({
  #  'make_delete': form.make_delete,
  #  'read_only': form.read_only,
  #  'list': form.manager['apt_list_ids'] } 
  #)
  
  #form.pre(form.manager)
def before_delete(form):
  #form.pre(form.manager['apt_list_ids'])
  #form.pre(form.ov['apteka_id'])
  if not(str(form.ov['apteka_id']) in form.manager['apt_list_ids']):
    form.errors.append(f'''Запрещено удалять данный запрос ''')

def before_search(form):
    qs=form.query_search

    if form.manager['type']==2:
        qs['WHERE'].append(f'''wt.apteka_id in ({','.join(form.manager['apt_list_ids'])})''')
    #form.pre(qs)
    #apt_list_ids
events={
  'permissions':[
      events_permissions
  ],
  'before_search':[
      before_search
  ],
  'before_delete':before_delete

}