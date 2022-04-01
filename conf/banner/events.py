#def pre(d):
#    form.pre(d)
#from lib.CRM.plugins.search.xlsx import go as init_search_plugin

def events_permissions(form):
    
    if ('superadmin' in form.manager['permissions']) or (form.manager['login']=='admin'):
      form.is_admin=1
      form.read_only=0
      form.not_create=0
      #init_search_plugin(form)
      
    else:
      form.is_admin=0
      form.make_delete=0
      form.not_create=True

    if not ( str(form.manager['type']) == "1" ):
      form.errors.append('доступ запрещён!')
      #return 




      

def before_search(form):
  pass

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