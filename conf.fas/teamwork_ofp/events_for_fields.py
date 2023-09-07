from config import config
from lib.core_crm import get_manager, get_owner
from lib.core import cur_date, date_to_rus


def firm_code(form,field):
  #print('FIRM CODE!')
  user_id=form.user_id
  html=''
  if user_id:
    html=f'Карточка ОП: <a href="/edit_form/user/{user_id}" target="_blank">{config["BaseUrl"]}edit_form/user/{user_id}</a>'
  else:
    html = "<span style='color: red'>id не было введено на этапе создания карточки СР</span>"

  field['after_html']=html
  


# Менеджер
def manager_before_code(form,field):
  
  if form.manager['login'] in ('sed','admin','akulov'):
    
    field['read_only']=False

  name=field['name']
  if form.ov and form.ov[name]:
    manager_email=''
    to_out=[]
    if form.ov[f"{name}_email"]:
      #manager_email=f'<a href="mailto:{form.ov["manager_from_email"]}">{form.ov["manager_from_email"]}</a> ;'
      to_out.append(f'<a href="mailto:{form.ov[name+"_email"]}">{form.ov[name+"_email"]}</a>')
    if form.ov[name+'_phone']:
      to_out.append("тел: "+form.ov[name+'_phone'])

    if len(to_out):
      field['after_html']=f'''<small> {';'.join(to_out)}</small>'''

    # для поля "менеджер" выводим руководителя
    if name=='manager_from':
      manager_from=get_manager(
        id=form.ov['manager_from'],
        db=form.db
      )
      if manager_from:
        owner_from=get_owner(
          cur_manager=manager_from,
          db=form.db
        )
        if owner_from:
          to_out=[]
          if owner_from['name']: to_out.append(owner_from['name'])
          if owner_from['email']: to_out.append(f'<a href="mailto:{owner_from["email"]}">{owner_from["email"]}</a>')
          if owner_from["phone"]: to_out.append(owner_from["phone"])
          if len(to_out):
            field['after_html']+=f'<div style="margin-bottom: 20px;"><small>Руководитель: {" ; ".join(to_out)}</small></div>'
      



def manager_to2_before_code(form,field):
  if form.manager['login'] in ('naumova','sheglova','sed','akulov','zia','strogov','pan'):
    field['read_only']=False

  manager_before_code(form,field)

def born_before_code(form,field):
  if form.script=='admin_table':
    d=cur_date()
    field['value']=[d,d]

  #form.pre(form.script)
# для поля "статус клиента"
def client_status_before_code(form,field):
  #return 
  if form.is_manager_to:    
    if not(form.ov['block_card']):
      field['read_only']=0
      field['regexp_rules']=[
        '/^[1-9]$/','Выберите значение'
      ]

events={
  'born':{
    'before_code':born_before_code
  },
  'firm':{
    'before_code':firm_code
  },
  'manager_from':{
    'before_code':manager_before_code
  },
  'manager_to':{
    'before_code':manager_before_code
  },
  'manager_to2':{
    'before_code':manager_to2_before_code
  },
  'client_status':{
    'before_code':client_status_before_code
  }

}