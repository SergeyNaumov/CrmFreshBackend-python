#def pre(d):
#    form.pre(d)
from lib.CRM.plugins.search.xlsx import go as init_search_plugin
from lib.core import exists_arg
def events_permissions(form):
    #form.pre(form.manager)
    #return 
    if ('superadmin' in form.manager['permissions']) or (form.manager['login']=='admin'):
      form.is_admin=1
      form.not_create=0
      form.make_delete=1
      form.read_only=0
      init_search_plugin(form)
      
    else:
      form.is_admin=0
      form.make_delete=0

    perm=form.manager['permissions']
    if perm['manager_all_edit']:
      form.read_only=0
      form.make_delete=True
      form.not_create=False
    
    if not(perm['manager_access']) and not(perm['manager_all_edit']):
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
      


      

def before_search(form):
  qs=form.query_search
  #form.pre('email' in qs['on_filters_hash'])
  # Фильтр email включен - добавляем в результаты
  if 'email' in qs['on_filters_hash']:
    qs['SELECT_FIELDS'].append("group_concat(me.email SEPARATOR ', ') email  ")

  #form.pre(qs['SELECT_FIELDS'])
  #qs['SELECT_FIELDS'].append('if(wt.type=4, uf.header ,group_concat(u.header SEPARATOR "; ")) ur_lico_list')
  #form.explain=1

def events_before_code(form):
    pass

def before_delete(form):
    pass

events={
  'permissions':[
      events_permissions
    
  ],
  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}