from lib.send_mes import send_mes
from lib.core_crm import get_manager, get_owner, get_email_list_from_manager_id

async def links_before_code(form,field):
  if form.ov:
    out=[f"<div><a href='/edit_form/user/{form.ov['user_id']}' target='_blank'>Карточка ОП</a></div>"]
    exists_ids=await form.db.query(
      query="SELECT teamwork_ofp_id from teamwork_ofp where user_id=%s",
      values=[form.ov['user_id']],
      massive=1
    )
    for ofp_id in exists_ids:
      out.append(f"<div><a href='/teamwork_ofp/user/{ofp_id}' target='_blank'>Карточка ОФП</a></div>")
    field['after_html']="".join(out)

def firm_before_code(form,field):
  if form.ov:
    field['after_html']=form.ov['firm']

def inn_before_code(form,field):
  if form.ov:
    field['after_html']=form.ov['inn']


def manager_before_code(form,field):
  if form.manager['permissions'].get('card_bbg_make_change_manager'):
    field['read_only']=0
  return field
#print('is events for fields')

async def memo_after_add(form,field,data):
  if ov:=form.ov:
    firm=form.ov['firm']
    manager_dict={}
    if manager_id:=ov['manager_id']:
      manager_dict[manager_id]=1
      cur_manager=await get_manager( id=manager_id, db=form.db )
      if owner:=await get_owner(cur_manager=cur_manager,db=form.db):
        manager_dict[owner['id']]=1

    if manager_id:=ov['manager_bbg']:
      manager_dict[manager_id]=1
      cur_manager=await get_manager( id=manager_id, db=form.db )
      if owner:=await get_owner(cur_manager=cur_manager,db=form.db):
        manager_dict[owner['id']]=1

    if len(list(manager_dict.keys())):
      #print('manager_dict:',manager_dict)
      to=await get_email_list_from_manager_id(form.db, manager_dict)
      to['dmn@reg-rf.pro']=True
      message=f"Только что {form.manager['name']} добавил комментарий: {data.get('body')}<br>"+\
      f"в карту ББГ: <a href='{form.s.config['system_url']}edit_form/user_bbg/{form.id}'>{firm}</a>"

      send_mes(
        from_addr='info@fascrm.ru',
        to=','.join(to.keys()),
        subject=f"Добавлен комментарий карточку ББГ {firm}",
        message=message
      )
      #print('to:',to)
      #print('memo_after_add:',message)

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
  },
  'memo':{
    'after_add':memo_after_add
  }
}
