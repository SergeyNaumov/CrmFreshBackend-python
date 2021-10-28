#def pre(d):
#    form.pre(d)
from lib.anna.get_apt_list import get_apt_list_ids
from lib.send_mes import send_mes 
def get_ov(form):
  form.ov=form.db.query(
    query='''
      select
        wt.*,
        mph.id mph__id,
        mph.apteka_id
      from
        manager wt
        LEFT JOIN manager_pharmacist mph ON mph.id=wt.id
      where wt.id=%s
    ''',
    values=[form.id],
    onerow=1
  )
  
  return form.ov

def events_permissions(form):

    if form.action=='new':
      form.title='Создание фармацевта'
      
    if form.manager['type'] in (1, 2,3):
      form.make_delete=1
      form.not_create=0
      form.read_only=0

    if form.manager['type'] in (2,3):
      apt_list_ids=get_apt_list_ids(form)
      form.manager['apt_list_ids']=apt_list_ids

      if not len(apt_list_ids):
        form.errors('Вы не можете администрировать фармацевтов, поскольку не привязаны ни к одной аптеке')
    
    if form.manager['type']=='4':
      form.errors.append('Доступ запрещён')


    if form.id:
      ov=get_ov(form)
      
      #form.ov=ov
      form.title='Фармацевт: '+form.ov['name']
      
      #  {'v':1,'d':'Сотрудник компании Анна'},
      #  {'v':2,'d':'Представитель юридического лица'},
      #  {'v':3,'d':'Представитель аптеки'},
      
      # Сотрудник компании "Анна", может изменять только суперадмин
      #form.pre(form.manager)
      # Сотрудник компании Анна(1) может вносить изменения в аккаунт (2,3)
      if ov['type']==4: 
        form.read_only=0 # -- запретили редактировать всем
      else:
        form.read_only=1

      form.ov=ov
      

def before_search(form):
  qs=form.query_search
  if form.manager['type'] in (2,3):

    qs['WHERE'].append(f"mph.apteka_id in ( {','.join(form.manager['apt_list_ids']) } )")
  qs['SELECT_FIELDS'].append('group_concat(u.header SEPARATOR "; ") ur_lico_list')
  

def events_before_code(form):
    pass

def before_delete(form):
    if form.manager['type']==1:
      pass

    elif form.manager['type'] in (2,3) :
      
      # если удаляет чужое
      if str(form.ov['apteka_id']) not in form.manager['apt_list_ids']:
        form.errors.append('У Вас нет права удалять данную аптеку')
    else:
      form.errors.append('Удаление запрещено')
    

def after_save(form):
    nv=form.new_values
    data={
      'id':form.id,
      'apteka_id':nv['apteka_id']
    }
  
    form.db.save(
      table='manager_pharmacist',
      errors=form.errors,
      replace=1,
      data=data
    )
    #form.pre({'nv':nv})
    get_ov(form)
    form.ov['apteka_id']=nv['apteka_id']

    if form.action == 'insert' and nv['email']:
      send_mes(
        to=nv['email'],
        subject='Новая учётная запись в сисиеме АннА',
        message=f"""
          Уважаемый(ая) {nv['name']}!<br><br>
          Только что для Вас была создана учётная запись в системе АннА:<br>
          Логин: {nv['login']}<br>
          Пароль: {nv['password']}<br>
          <hr>
          Адрес для входа: {form.s.config['system_url']}
        """
      )

  

def before_insert(form):
  if 'login' in form.new_values:
    exists=form.db.query(
      query='select id from manager where login=%s',
      values=[form.new_values['login']],
      errors=form.errors,
      onevalue=1
    )
    if exists:
      form.errors.append(f"Логин {form.new_values['login']} уже занят")
  


events={
  'permissions':[
      events_permissions
    
  ],
  'before_insert':before_insert,
  'after_save':after_save,
  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}