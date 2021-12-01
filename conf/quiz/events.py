from lib.core import date_to_rus
def events_permissions(form):
  if('superadmin' in form.manager['permissions']):
    form.not_create=0
    form.make_delete=1
    form.make_edit=1
    form.read_only=0

  if form.script=='table':
    form.title='Тестирование'
    if('superadmin' in form.manager['permissions']):
        form.links=[
            {
                'type':'url',
                'link':'/admin_table/quiz',
                'description':'Перейти к редактированию'
            },
        ]
    query=f"""
      SELECT id, header,link, dat_begin,dat_end
      FROM {form.work_table}
    """
    if form.manager['type']!=1:
      query+=' WHERE dat_end>=curdate()'
    
    form.data=form.db.query(
        query=query,
        log=form.log,
        errors=form.errors,
        arrays=1
    )

    for d in form.data:
      d['link']=f'<a href="{d["link"]}" target="_blank">{d["link"]}</a>'
      d['period']=f"{date_to_rus(d['dat_begin']) } - {date_to_rus(d['dat_end']) }"
      for for_del in ('id','dat_begin','dat_end'):
          del d[for_del]

  # else:
  #   form.not_create=1
  #   form.make_delete=0
  #   form.make_edit=0
  #   form.read_only=1
  
events={
  'permissions':[
      events_permissions
  ],
}