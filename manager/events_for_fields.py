#def email_filter_code(form,field,row):
#  if not row['email']: row['email']=''
#  return row['email']
async def emails_after_save_code(form,field):
  #print('id:',form.id)
  if field['values'] and len(field['values']):
    v=field['values'][0]
    await form.db.query(
      query=f"UPDATE manager_email set main=0 where manager_id={form.id} and id<>{v['id']}",
    )

async def gone_before_code(form,field):
  if form.id and form.ov['exists_user_card']:
    field['read_only'] = 1
    field['after_html'] = '<div style="color:red;">На данном сотруднике есть карты ОП</div>'

  
async def email_filter_code(form,field,row):
  return row['email']

async def group_id_filter_code(form,field,row):

  if row['mg__path'] and not form.id:
    ids = f"{row['mg__path']}/{row['mg__id']}"[1:].split('/')
    parent_data = await form.db.query(
      query=f"SELECT id, header FROM manager_group WHERE id IN ({','.join(ids)}) order by length(regexp_replace(path,'[^/]',''))",
    )
    link_data = []
    for obj in parent_data:
      link_data.append(f"""<a href="/edit_form/manager_group/{obj['id']}" target="_blank">{obj['header']}</a>""")
    return ' / '.join(link_data)
  elif row['mg__id']:
    return f"""<a href="/edit_form/manager_group/{row['mg__id']}" target="_blank">{row['mg__header']}</a>"""
  else:
    return ''



events={
  #'email':{
  #  'filter_code':email_filter_code
  #},
  'emails':{
    'after_save_code': emails_after_save_code,
  },
  'email':{
    'filter_code':email_filter_code
  },
  'gone': {
    'before_code': gone_before_code
  },
  'group_id': {
    'filter_code': group_id_filter_code
  }
}
