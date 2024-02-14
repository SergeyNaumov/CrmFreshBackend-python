#def pre(d):
#    form.pre(d)
from lib.CRM.plugins.search.xlsx import go as init_search_plugin
from lib.core import exists_arg
def events_permissions(form):
    perm=form.manager['permissions']

    if('manager_admin' in perm) or (form.manager['login']=='admin'):
      form.is_admin=1
      form.read_only=0
      form.make_delete=1
      form.not_create=0
    else:
      form.errors.append('Доступ запрещён')
    
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