from lib.core import exists_arg, gen_pas
from db import db,db_read,db_write
from config import config
from base64 import b64decode

def session_project_create(s): # создание сессии для проекта
    pass

def session_create(s,**arg):

  errors=[]
  if not(exists_arg('login',arg)):
    arg['login']='adminX' # $R->{login}
    
    if not(exists_arg('login',arg)):
      return 'При создании сессии (не указан login)'

  if not(exists_arg('password',arg)):
    arg['password']='passwordX' # $R->{password}
    
    if not(exists_arg('password',arg)):
      return 'При создании сессии (не указан password)'

  session_table='session'
  session_fails_table='session_fails'


  #if 'session_table' in config['auth']:
  #  session_table=config['auth']['session_table']
  
  #if 'session_fails_table' in config['auth']:
  #  session_fails_table=config['auth']['session_fails_table']

  #session_table=config['auth']['session_table']
  
  auth=config['auth']

  if not(exists_arg('auth_id_field',auth)): auth['auth_id_field']='id'
  if not(exists_arg('auth_log_field',auth)): auth['auth_log_field']='login'
  if not(exists_arg('auth_pas_field',auth)): auth['auth_pas_field']='password'
  if not(exists_arg('session_table',auth)): auth['session_table']='session'
  if not(exists_arg('session_fails_table',auth)): auth['session_fails_table']='session_fails_table'
  if not(exists_arg('auth_table',auth)): auth['auth_table']='manager'

  add_where=''
  if exists_arg('where',arg):
      add_where += ' AND '+arg['where']

  if exists_arg('max_fails_login',auth) and exists_arg('max_fails_login_interval',auth):
      fails=db.query(
        query=f'select count(*) from {auth["session_fails_table"]} where login=%s and registered>=now() - interval %s second',
        values=[arg['login'],auth['max_fails_login_interval']],
        onevalue=True,
        errors=errors
      )
      if fails and fails > auth['max_fails_login'] :
        return 'Ошибка безопасности: превышено максимальное количество входа по логину'
  
  # проверяем, сколько было попыток зайти с данного ip под данным паролем
  if exists_arg('max_fails_ip',auth) and exists_arg('max_fails_login_interval',config['auth']):
      fails=s.db.query(
        query=f'select count(*) from {auth["session_fails_table"]} where ip=%s and registered>=now() - interval %s second',
        values=[arg['ip'],auth['max_fails_ip_interval']],
        onevalue=True,
        errors=errors
      )

      if fails and fails > auth['max_fails_ip'] :
          return 'Ошибка безопасности: превышено максимальное количество входа по IP'
  

  auth_id=None

  if auth['encrypt_method']=='mysql_sha2':
      auth_id=s.db.query(
        query='SELECT '+auth['manager_table_id']+' FROM '+auth['manager_table']+' WHERE '+auth['auth_log_field']+'=%s AND '+auth['auth_pas_field']+'=sha2(%s,256)'+add_where,
        values=[arg['login'],arg['password']],
        onevalue=True,
      )
  elif auth['encrypt_method']=='mysql_encrypt':
      auth_id=s.db.query(
        query='SELECT '+auth['manager_table_id']+' FROM '+auth['manager_table']+' WHERE '+auth['auth_log_field']+'=%s AND '+auth['auth_pas_field']+'=encrypt(%s,password)'+add_where,
        values=[arg['login'],arg['password']],
        onevalue=True,
        debug=1
      )
  else:
      auth_id=s.db.query(
          query="SELECT "+auth['manager_table_id']+' FROM '+auth['manager_table']+' WHERE '+auth['auth_log_field']+'=%s AND '+auth['auth_pas_field']+'=%s '+add_where,
          values=[arg['login'], arg['password']],
          onevalue=True
      );
  
  if auth_id:
    s.manager={
      'id':auth_id,
      'login':arg['login']
    }

    key=gen_pas(200)

    db.save(
      table=session_table,
      data={
        'auth_id':auth_id,
        'session_key':key
      }
    )
    s.set_cookie(name='auth_user_id',value=auth_id)
    s.set_cookie(name='auth_key',value=key)
  else:
    errors.append('авторизационные данные неверны')


  return{
    'success':not(len(errors)),
    'errors':errors
  }

def session_start(s,**arg):
  user_id=s.get_cookie('auth_user_id')
  key=s.get_cookie('auth_key')
  session_table='session'
  if 'session_table' in config['auth']:
    session_table=config['auth']['session_table']
  
  manager_table='manager'
  
  if 'manager_table' in config['auth']:
    session_table=config['auth']['manager_table']

  errors=[]
  s.use_project=config['use_project']
  manager={'login':'','id':False, 'password':''}
  


  if  exists_arg('type',config['auth']) and config['auth']['type']=='env':
    if 'authorization' in s.env:
      auth=s.env['authorization']
      login=b64decode(auth.split(' ')[1]).decode('utf-8')
      log_pas=login.split(':')
      log=log_pas[0]
      
      #print('spl:',type(log),type(log2),'log',)
      #login=login.split(':')[0]
      #login=login
      #login=login.decode('utf-8')
      print('remote_user:',s.env)
      if 'remote_user' in s.env:
        m=s.db.query(
          query=f"select *,{config['auth']['manager_table']} id from {manager_table} WHERE {config['auth']['login_field']} = %s ",
          values=[log],
          onerow=1,
        )
        if m:
          manager=m
  else:

      
      if config['use_project']:
        session_table='project_session'
        manager_table='project_manager'

      
      ok=s.db.query(
        query='SELECT count(*) FROM '+session_table+' WHERE auth_id=%s and session_key=%s',
        values=[user_id, key],
        onevalue=1,
        errors=errors
      )
      
      if ok:
          manager=s.db.query(
            query='select * from '+manager_table+' where id=%s',
            values=[user_id],
            onerow=1,errors=errors
          );

  
  if manager:
    manager['id']=str(manager['id'])
    
    del manager['password']
    s.manager=manager
      
  s._content={
    'success':1,
    'login':manager['login'],
    'errors':errors,
    #'env':s.env
  }

  if manager['login']:
    s.login=manager['login']
  else:
    #s._content['redirect']=''
    s._content['redirect']='/login'
    
    #s._content['referer']=s.request
    s._content['success']=0
    s.end()

def session_logout(s):
  user_id=s.get_cookie('auth_user_id')
  key=s.get_cookie('auth_key')
  #print('user_id:',user_id)
  if user_id and user_id.isdigit() and int(user_id) and key :
      if config['use_project']:
        s.db.query(
          query='DELETE FROM project_session WHERE auth_id=%s and session_key=%s',
          values=[user_id,key]
        )
      else:
          s.db.query(
            query='DELETE FROM session WHERE auth_id=%s and session_key=%s',
            values=[user_id,key]
          )



def project_get_permissions_for(form,login):
  manager=form.db.query(
      query="""
        SELECT 
          m.*,
          if(m.id = ow.id,1,0) is_owner,
          mg.path group_path,
          concat_ws('/',mg.path,mg.id) full_group_path
        FROM
          project_manager m
          LEFT JOIN project_manager_group mg ON (m.group_id = mg.id)
          LEFT JOIN project_manager ow ON (mg.owner_id = ow.id) 
        WHERE m.login = %s and m.project_id=%s
      """,
      values=[login,s.project.id],
      onerow=1,
      log=form.log
    
  )
  del manager['password']

def child_groups(db,group_id):
  if not len(group_id):
    return []


  group_table='manager_group'
  if 0: # s.use_project
    group_table='project_manager_group'
  
  # group_id to str for join
  j=0
  for g in group_id:
    group_id[j]=str(group_id[j])
  g_list=db.query(
    query="SELECT id from "+group_table+" where parent_id IN (" + ','.join(group_id) + ')'
  )
  for g1 in g_list:
    for g2 in child_groups(db,[g1['id']]):

      group_id.append(g2)

  return group_id
  



def get_permissions_for(form,login):
  
  manager=form.db.query(
    query="""
        SELECT 
          m.*,
          if(m.id = ow.id,1,0) is_owner,
          mg.path group_path,
          concat_ws('/',mg.path,mg.id) full_group_path
        FROM
          manager m
          LEFT JOIN manager_group mg ON (m.group_id = mg.id)
          LEFT JOIN manager ow ON (mg.owner_id = ow.id) 
        WHERE m.login = %s
    """,
    values=[login],onerow=1,log=form.log
  )
  manager['id']=str(manager['id'])
  
  if manager['password']: del manager['password']
  
  permissions_list=form.db.query(
    query='SELECT p.id, p.pname from permissions p, manager_permissions mp where p.id = mp.permissions_id and mp.manager_id = %s',
    values=[manager['id']]
  );
  manager['permissions']={};
  for p in permissions_list:
      manager['permissions'][p['pname']]=p['id']

  if manager['group_id']:
    group_id=manager['group_id']
    gr_perm_list=form.db.query(
      query="""
        SELECT
          p.id, p.pname
        from
          permissions p, manager_group_permissions mgp
        where
          p.id = mgp.permissions_id and mgp.group_id = %s
      """,
      values=[group_id]
    )
    for p in gr_perm_list:
        manager['permissions'][p['pname']]=p['id']

    manager['CHILD_GROUPS']=child_groups(form.db,[group_id])
    manager['CHILD_GROUPS_HASH']={}
    for g_id in manager['CHILD_GROUPS']:
        manager['CHILD_GROUPS_HASH'][g_id]=1
    
  manager['files_dir']='./files'
  manager['files_dir_web']='/files'
  return manager
  #print('permissions_list:',permissions_list)
