#def pre(d):
#    form.pre(d)
from lib.CRM.plugins.search.xlsx import go as init_search_plugin
from lib.core import exists_arg

async def new_form_permissions(form):
  # При добавлении нового сотрудника сделать окно с обязательными полями. Логин, группа, email, ФИО
  
  if form.action=='new':
    form.cols=[]
    for f in form.fields:

      if not(f['name'] in ('login','group_id','name')):
        form.remove_field(f['name'])

      elif f['name']=='name':
        form.fields.append({
          'description':'Email',
          'name':'email',
          'type':'text',
          'regexp_rules':[
              '/^.+@.+[a-zA-Z0-9\-\_]+$/','Укажите корректный email',
          ],
        })

async def before_save(form):
  ...
  # Получаем группу для бренда:

  #form.log.append(f"{brand_id=}")
  #form.errors.append(f"{}")

async def new_form_after_insert(form):
  group_id=form.R['values']['group_id']
  
  


async def events_permissions(form):
    manager = form.manager
    if form.id:
      form.ov = form.db.query(
        query="select * from manager where id=%s",
        values=[form.id],
        onerow=1
      )
    else:
      form.ov=None
      
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
    if perm.get('manager_all_edit'):
      form.read_only=0
      form.make_delete=True
      form.not_create=False

    len_child_groups = manager.get('CHILD_GROUPS') and len(manager.get('CHILD_GROUPS'))

    if not(perm.get('manager_access')) and not(perm.get('manager_all_edit')) and not(manager.get('is_owner')) and len_child_groups:
      form.errors.append('доступ запрещён!')
      #return 




    


      

async def before_search(form):
  manager = form.manager
  perms = manager['permissions']
  qs=form.query_search
  ...

async def events_before_code(form):
    pass

async def before_delete(form):
    pass

events={
  'permissions':[
      new_form_permissions,
      events_permissions
    
  ],
  'before_save':before_save,
  'after_insert':[
      new_form_after_insert
  ],

  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}