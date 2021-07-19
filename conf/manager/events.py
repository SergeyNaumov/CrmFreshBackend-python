#def pre(d):
#    form.pre(d)

def events_permissions(form):
    
    if ('superadmin' in form.manager['permissions']) or (form.manager['login']=='admin'):
      form.is_admin=1
      form.read_only=0
    else:
      form.is_admin=0
      form.make_delete=0

    if not ( str(form.manager['type']) == "1" ):
      form.errors.append('доступ запрещён!')
      #return 




    if form.id:
      ov=form.db.query(
        query="select * from manager where id=%s",
        values=[form.id],
        onerow=1
      )
      form.ov=ov
      form.title='Учётная запись: '+form.ov['name']
      
      #  {'v':1,'d':'Сотрудник компании Анна'},
      #  {'v':2,'d':'Представитель юридического лица'},
      #  {'v':3,'d':'Представитель аптеки'},
      
      # Сотрудник компании "Анна", может изменять только суперадмин
      #form.pre(form.manager)
      # Сотрудник компании Анна(1) может вносить изменения в аккаунт (2,3)
      if (ov['type']==2 or ov['type']==3) and form.manager['type']==1: 
        form.read_only=0

      

def before_search(form):
  qs=form.query_search
  #form.pre(qs['SELECT_FIELDS'])
  qs['SELECT_FIELDS'].append('group_concat(u.header SEPARATOR "; ") ur_lico_list')
  #form.explain=1

def events_before_code(form):
    pass

def before_delete(form,opt):
    pass

events={
  'permissions':[
      events_permissions
    
  ],
  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}