from lib.engine import s
from lib.core import create_fields_hash, exists_arg
from lib.session import project_get_permissions_for, get_permissions_for

def form_self():
  return s


def need_only_read(form):
  w1=True #(form.script=='admin_table' and form.action=='edit')
  w2=(form.script=='memo' and form.action=='get_data')
  w3=(form.script=='find_results')
  if w1: #  or w2 or w3
    return True

  return False

def get_cur_role(**arg):
  form=arg['form']
  if(form.config == 'manager'):
    return arg['login']
  
  manager_table='manager'
  manager_role_table='manager_role'
  if s.use_project:
      manager_role_table='project_manager_role'
      manager_table='project_manager'
  
  r=s.db.query(
    query="""
      SELECT
        m2.login
      FROM
        """+manager_table+' m JOIN '+manager_role_table+""" mr ON (m.id = mr.manager_id)
        JOIN """+manager_table+""" m2  ON (m2.id = mr.role AND m.current_role = m2.id)
      WHERE m.login=%s
    """,
    values=[arg['login']],
    onevalue=1,
    errors=form.errors
  )

  if r:
    return r
  else:
    return arg['login']

def default_config_attr(form,arg): # Атрибуты формы по умолчанию
    script=arg['script']
    form.config=arg['config']
    form.script=script

    if 'R' in arg:
      form.R=arg['R']

    # Атрибуты по умолчанию
    s.form=form
    # read_only
    if not hasattr(form,'read_only'): form.read_only=0

    # make_delete
    if not hasattr(form,'make_delete'):
      if form.read_only:
        form.make_delete=0
      else:
        form.make_delete=1

    # make_create
    if not hasattr(form,'make_create'):
      if form.read_only:
        form.make_create=0
      else:
        form.make_create=1

    

    create_fields_hash(form)


    if exists_arg('action',arg): form.action=arg['action']
    
    if exists_arg('id',arg) and arg['id'].isnumeric():
      form.id=arg['id']

    if not form.work_table: form.work_table=arg['config']
    
    if need_only_read(form) :
        form.db=s.db_read
    else:
       form.db=s.db_write



    # Получаем manager-а 
    login=get_cur_role(
      login=s.login,
      form=form
    )
    if s.use_project:
      form.manager=project_get_permissions_for(form,login)
    else:
      form.manager=get_permissions_for(form,login)


    form.self=form_self
    # Доделать!
    #return form