def permissions_before_code(**arg):
  form=arg['form']
  field=arg['field']

  # Для администратора или для менеджера с галкой открываем возможность изменять права доступа
  if form.is_admin:
    field['read_only']=0

def manager_brand_access_before_code(form,field):
  ...

def access_role_before_code(form,field):
  if form.manager['permissions'].get('manager_make_change_role'):
    field['read_only']=0
    field['make_delete']=1

async def current_role_before_code(form,field):
  field['read_only']=1

  if form.is_admin or form.manager['permissions'].get('manager_make_change_role'):
    field['read_only']=0
  ids = await form.db.query(
    query=f"select role from manager_role where manager_id={form.manager['id']}",
    massive=1,
    str=1
  )


  if len(ids):
    field['where']=f"id in ({','.join(ids)})"
  else:
    field['read_only']=1

fields=[
    {
       'description':'Доступные роли',
       'name':'access_roles',
       'type':'1_to_m',
       'cols':2,
       'table':'manager_role',
       'table_id':'id',
       'foreign_key':'manager_id',
       'read_only':0,
       'fields':[
          {
            'description':'Роль',
            'name':'role',
            'type':'select_from_table',
            'table':'manager',
            'header_field':'name',
            'value_field':'id'
          }
       ],
       #'before_code':access_role_before_code,
       'tab':'permissions',

    },
    {
      'description':'Текущая роль',
      'type':'select_from_table',
      'name':'current_role',
      'table':'manager',
      'header_field':'name',
      'value_field':'id',
      'tab':'permissions',
      #'before_code':current_role_before_code
    },
    {
      #'before_code': permissions_before_code,
      'description':'Права учётной записи',
      'type':'multiconnect',
      'tree_use':0,
      'tree_table':'permissions',
      'relation_tree_order':'sort',
      'name':'permissions',
      'tablename':'p',
      'relation_table':'permissions',
      'relation_save_table':'manager_permissions',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'manager_id',
      'relation_save_table_id_relation':'permissions_id',
      'tab':'permissions',
      #'not_order':1,
      #'read_only':1
    },
]