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
    if form.manager.get('login')=='beyeezymanager' or perm.get('admin'):
      form.read_only=0
      form.make_delete=True
      form.not_create=False
    
    #if not(perm.get('manager_access')) and not(perm.get('manager_all_edit')):
    #  form.errors.append('доступ запрещён!')





    if form.id:
      ov=form.db.query(
        query="select * from manager where id=%s",
        values=[form.id],
        onerow=1
      )
      form.ov=ov
      form.title='Учётная запись: '+form.ov['name']
      


      



def events_before_code(form):
    pass

def before_delete(form):
    form.errors.append('запрещено удалять менеджеров')

events={
  'permissions':[
      events_permissions
    
  ],
 # 'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}