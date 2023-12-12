def links_before_code(form,field):
  if form.ov:
    out=[f"<div><a href='/edit_form/user/{form.ov['user_id']}' target='_blank'>Карточка ОП</a></div>"]
    exists_ids=form.db.query(
      query="SELECT teamwork_ofp_id from teamwork_ofp where user_id=%s",
      values=[form.ov['user_id']],
      massive=1
    )
    for ofp_id in exists_ids:
      out.append(f"<div><a href='/teamwork_ofp/user/{ofp_id}' target='_blank'>Карточка ОФП</a></div>")
    return "".join(out)

def firm_before_code(form,field):
  if form.ov:
    field['after_html']=form.ov['firm']

def inn_before_code(form,field):
  if form.ov:
    field['after_html']=form.ov['inn']

def manager_before_code(form,field):
  if form.manager['permissions'].get('card_bbg_make_change_manager'):
    field['read_only']=0


events={
  'links':{
    'before_code':links_before_code
  },
  'firm':{
    'before_code':firm_before_code
  },
  'inn':{
    'before_code':inn_before_code
  },
  'manager_id':{
    'before_code':manager_before_code
  },
  'manager_bbg':{
    'before_code':manager_before_code
  }
}