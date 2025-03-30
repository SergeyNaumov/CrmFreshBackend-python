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
  brand_id = await form.db.query(query="select brand_id from manager_group where id=%s", values=[group_id],onevalue=1)
  await form.db.save(
    table="manager_email",
    data={
      'manager_id':form.id,
      'main':1,
      'brand_id':brand_id,
      'email':form.R['values']['email']
    },
    debug=1
  )
  #form.errors.append('check!')


async def events_permissions(form):
    manager = form.manager
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

    if manager['login']!='admin' and not( perm.get('manager_access') ) and not(perm.get('manager_all_edit') )  and not(manager.get('is_owner') and len(manager['CHILD_GROUPS'])):

      form.errors.append('доступ запрещён!')
      #return 




    if form.id:
      manager = form.manager
      ov=await form.db.query(
        query="select * from manager where id=%s",
        values=[form.id],
        onerow=1
      )

      if not perm.get('manager_all_edit') and ov and manager.get('CHILD_GROUPS') and ov.get('group_id') not in manager.get('CHILD_GROUPS'):
        form.errors.append('доступ запрещён!')

      ov['exists_user_card'] = await form.db.query(
          query=f"SELECT id FROM user WHERE manager_id={form.id} LIMIT 1", onevalue=1
      )
      form.ov=ov
      form.title='Учётная запись: '+form.ov['name']
      if manager.get('is_owner') and len(manager['CHILD_GROUPS']) and ov['group_id'] in manager['CHILD_GROUPS']:
        form.read_only=0
        for field in form.fields:
          if field.get('tab') and field['tab'] == 'kpi':
            field['read_only'] = False
          elif field.get('tab') and field['tab'] == 'permissions' and not manager['permissions']['is_admin']:
            field['read_only'] = True
          elif field.get('tab') and field['tab'] == 'hr' and not field['name'] == 'born_date':
            field['read_only'] = True
          elif field.get('tab') and field['tab'] == 'main' and field['name'] in ['login', 'group_id']:
            field['read_only'] = True


      

async def before_search(form):
  manager = form.manager
  perms = manager['permissions']
  qs=form.query_search
  #form.pre('email' in qs['on_filters_hash'])
  # Фильтр email включен - добавляем в результаты
  if 'email' in qs['on_filters_hash']:
    qs['SELECT_FIELDS'].append("group_concat(me.email SEPARATOR ', ') email  ")

  if perms['manager_all_edit']:
    ...
  else:
    qs['WHERE'].append(f"wt.group_id in ({','.join(map(str, manager['CHILD_GROUPS']))})")
  #form.pre(qs['SELECT_FIELDS'])
  #qs['SELECT_FIELDS'].append('if(wt.type=4, uf.header ,group_concat(u.header SEPARATOR "; ")) ur_lico_list')
  #form.explain=1

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