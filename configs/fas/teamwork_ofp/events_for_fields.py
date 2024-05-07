from config import config
from lib.core_crm import get_manager, get_owner, get_email_list_from_manager_id
from lib.core import cur_date, date_to_rus, exists_arg
from lib.send_mes import send_mes


  
def group_id_before_code(form,field):
  #form.pre(form.manager['login'])
  if form.manager['login'] in ('sed','admin','akulov','pzm'):
    #form.pre(['is sed'])
    field['read_only']=False

  if form.id and form.ov and form.ov.get('mfg__owner') == form.manager.get('id'):
    # руководителю менеджера ОП разрешаем редактировать это поле
    field['read_only']=False

  #form.pre([form.read_only, field['read_only'] ])
# Юрист
async def manager_before_code(form,field):
  
  if form.manager['login'] in ('sed','admin','akulov','pzm') or form.is_group_owner:
    field['read_only']=False

  if not(field['read_only']) and form.ov and not(form.ov['group_id']):
    # Если не выбрана группа юристов, то запрещаем менять
    field['read_only']=True
    field['after_html']='<span style="color: red;">запрещено выбирать юриста, потому что не выбрана группа</span>'
  #if form.ov:
  #  form.pre([form.ov['mfg__owner'], form.manager['id']])
  #if form.manager['login'] in ('admin','naumova','sheglova','sed','akulov','zia','strogov','pan'):
  #  field['read_only']=False

  name=field['name']
  if form.ov and form.ov[name]:
    manager_email=''
    to_out=[]
    if form.ov[f"{name}_email"]:
      #manager_email=f'<a href="mailto:{form.ov["manager_from_email"]}">{form.ov["manager_from_email"]}</a> ;'
      to_out.append(f'<a href="mailto:{form.ov[name+"_email"]}">{form.ov[name+"_email"]}</a>')
    if form.ov[name+'_phone']:
      if tel:=form.ov[name+'_phone']:
        to_out.append(f"тел: <a href='tel: {tel}'>{tel}</a>")

    if len(to_out):
      field['after_html']=f'''<small> {';'.join(to_out)}</small>'''

    # для поля "менеджер" выводим руководителя
    if name=='manager_from':
      manager_from=await get_manager(
        id=form.ov['manager_from'],
        db=form.db
      )
      if manager_from:
        owner_from=await get_owner(
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
      
  #form.pre(field)
  if form.is_group_owner and form.ov and form.ov['mgu__id']:
    field['where']=f"group_id={form.manager['group_id']}"

  if field['where']:
    if v:=field.get('value'):
      field['where']+=f" or id={v}"


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

# для поля "вид продукта"
def product_before_code(form,field):
    ap=form.param('add_param')
    if ap=='13':
        field['value']=8
        field['values']=[{'v':'8', 'd':'Подготовка документации'}]

def dat_session_before_code(form,field):
  if (not(form.ov) or not form.ov['block_card']) and (form.is_manager_from or form.is_manager_to):
            field['read_only']=False

def contacts_before_code(form,field):
  if form.id and form.ov['user_id']:
    field['foreign_key_value']=form.ov['user_id']
  else:
    field['foreign_key_value']=''
    field['read_only']=1
    field['after_html']='отображение контактов невозможно, поскольку данная карта не привязана к карте ОП'

def firm_before_code(form,field):
  #print('FIRM CODE!')
  user_id=form.user_id
  html=''


  if form.script=='edit_form':
    field['type']='code'
    field['full_str']=1
    if user_id:
      html=f'''
        {form.ov["firm"]}<br>

        Карточка ОП: <a href="/edit_form/user/{user_id}" target="_blank">{config["BaseUrl"]}edit_form/user/{user_id}</a>
      '''
    else:
      html = "<span style='color: red'>id не было введено на этапе создания карточки СР</span>"

    field['html']=html

def firm_filter_code(form,field,row):
  ofp_link=f'<a href="/edit_form/teamwork_ofp/{row["wt__teamwork_ofp_id"]}" target="_blank">в карту ОФП</a>'

  op_link=''
  if row['u__firm']:
    op_link=f' | <a href="/edit_form/user/{row["u__id"]}" target="_blank">в карту ОП</a>'

  return f'{row["u__firm"] or row["wt__firm"]}<br><small>{ofp_link} {op_link}</small>'

def inn_filter_code(form,field,row):
  #ofp_link=f'<a href="/edit_form/teamwork_ofp/{row["wt__teamwork_ofp_id"]}" target="_blank">в карту ОФП</a>'

  op_link=''
  if not(row['u__inn']):
    row['u__inn']='-'
  

  return row['u__inn']

def inn_before_code(form,field):
  if form.script=='edit_form':
    field['type']='code'
    field['html']=f"{form.ov['inn']}"
    #form.pre(form.ov)

def manager_id_before_code(form,field):

  # Делаем бутофорское поле "менеджер", подтягиваем значение из user.manager_id
  if form.script=='edit_form':
    field['type']='select_from_table'
    field['not_process']=1
    if form.manager['login'] in ('akulov','sed','fas'):
      field['read_only']=False

    if form.ov and 'mf__id' in form.ov:
      field['value']=form.ov['mf__id']

    #form.pre(form.ov)

# После добавления комментария:
async def comment_after_add(form,field,data):
  # сообщение должно уходить: Юристу, менеджеру ср, руководителю менеджера
  manager_id=form.manager['id']

  to={7576: True} # pzm
  to[manager_id]=True

  for recipent_id in [form.ov['manager_to'], form.ov['manager_to2'], form.ov['manager_from']]:
    if recipent_id:
      
      #if manager_id!=recipent_id:
      to[recipent_id]=True

      # для отправки руководителям
      manager=await get_manager(id=recipent_id, db=form.db)
      if manager: 
        owner=await get_owner(cur_manager=manager,db=form.db)
        if owner and owner['id']: #and manager_id!=owner['id']:
          to[owner['id']]=True


      



  last_comments=await form.db.query(
    query="SELECT * from teamwork_ofp_memo where teamwork_ofp_id=%s order by id desc limit 2",
    values=[form.id],
  )
  #print('to:',to)

  to_emails=await get_email_list_from_manager_id(form.db, to)
  #print(f"to_emails: ", ', ',to_emails)
  #print(f"to_emails: ", ', '.join(to_emails))
  #to_emails={}
  if len(to_emails):
    regnumber_str=''
    if form.ov['regnumber']:
      regnumber_str=f"Реестровый номер: {form.ov['regnumber']}"

    if len(last_comments)>1:
      # Не первый комментарий в карте
      #print('subject:',f"Новый комментарий, совместная работа ОФП {form.ov['brand']} / {form.ov['firm']} / {form.ov['product_label']}")
      send_mes(
        from_addr='info@fascrm.ru',
        to=','.join(to_emails.keys()),
        #to='svcomplex@yandex.ru',
        subject=f"Новый комментарий, совместная работа ОФП {form.ov['brand']} / {form.ov['firm']} / {form.ov['product_label']}",
        message=f"Наименование компании: {form.ov['link']}<br>"+\
            f"Менеджер: {form.manager['name']}<br>"+\
            f"Комментарий: {data['comment']}<br>"+\
            regnumber_str
      )
      # if form.id==1:
      #   send_mes0(
      #     from_addr='info@fascrm.ru',
      #     to=','.join(to_emails.keys()),
      #     #to='svcomplex@yandex.ru',
      #     subject=f"Новый комментарий, совместная работа ОФП {form.ov['brand']} / {form.ov['firm']} / {form.ov['product_label']}",
      #     message=f"Наименование компании: {form.ov['link']}<br>"+\
      #         f"Менеджер: {form.manager['name']}<br>"+\
      #         f"Комментарий: {data['comment']}<br>"+\
      #         regnumber_str
      #   )
    else:
      # первый комментарий в карте
      send_mes(
        from_addr='info@fascrm.ru',
        #to='svcomplex@yandex.ru',#
        to=','.join(to_emails.keys()),
        subject=f"Первый комментарий в карточке совместной работы ОФП / {form.ov['firm']} / {form.ov['product_label']}",
        message=f"Наименование компании: {form.ov['link']}<br>"+\
            f"Менеджер: {form.manager['name']}<br>"+\
            f"Комментарий: {data['comment']}<br>"+\
            regnumber_str
      )
    


events={
  'born':{
    'before_code':born_before_code
  },
  'firm':{
    'before_code':firm_before_code,
    'filter_code':firm_filter_code
  },
  'inn':{
    'before_code':inn_before_code,
    'filter_code':inn_filter_code
  },
  'manager_id':{
    'before_code':manager_id_before_code,
  },
  #'manager_from':{
  #  'before_code':manager_before_code
  #},
  'group_id':{
    'before_code':group_id_before_code
  },
  'manager_to':{
    'before_code':manager_before_code
  },
  'manager_to2':{
    'before_code':manager_to2_before_code
  },
  'client_status':{
    'before_code':client_status_before_code
  },
  'product':{
    'before_code':product_before_code
  },
  'dat_session':{
    'before_code':dat_session_before_code
  },
  'contacts':{
    'before_code':contacts_before_code
  },
  
  'comment1': {
      'after_add':comment_after_add
  }

  
}
