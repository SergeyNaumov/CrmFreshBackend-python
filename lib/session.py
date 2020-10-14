from lib.core import exists_arg, gen_pas
from db import db,db_read,db_write
from config import config

def session_project_create(s): # создание сессии для проекта
  print('project_create')

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

  if not(exists_arg('auth_id_field',arg)): arg['auth_id_field']='id'
  if not(exists_arg('auth_log_field',arg)): arg['auth_log_field']='login'
  if not(exists_arg('auth_pas_field',arg)): arg['auth_pas_field']='password'
  if not(exists_arg('session_table',arg)): arg['session_table']='session'
  if not(exists_arg('auth_table',arg)): arg['auth_table']='manager'

  add_where=''
  if exists_arg('where',arg):
      add_where += ' AND '+arg['where']

  if exists_arg('max_fails_login',arg) and exists_arg('max_fails_login_interval',arg):
      fails=db.query(
        query='select count(*) from session_fails where login=%s and registered>=now() - interval %s second',
        values=[arg['login'],arg['max_fails_login_interval']],
        onevalue=True,
        errors=errors
      )

      if fails > arg['max_fails_login'] :
        return 'Ошибка безопасности: превышено максимальное количество входа по логину'
  
  # проверяем, сколько было попыток зайти с данного ip под данным паролем
  if exists_arg('max_fails_ip',arg) and exists_arg('max_fails_login_interval',arg):
      fails=s.db.query(
        query='select count(*) from session_fails where ip=%s and registered>=now() - interval %s second',
        values=[arg['ip'],arg['max_fails_ip_interval']],
        onevalue=True,
        errors=errors
      )

      if fails > arg['max_fails_ip'] :
          return 'Ошибка безопасности: превышено максимальное количество входа по IP'
  

  auth_id=None
  if arg['encrypt_method']=='mysql_sha2':
      auth_id=s.db.query(
        query='SELECT '+arg['auth_id_field']+' FROM '+arg['auth_table']+' WHERE '+arg['auth_log_field']+'=%s AND '+arg['auth_pas_field']+'=sha2(%s,256)'+add_where,
        values=[arg['login'],arg['password']],
        onevalue=True
      )
  else:
      auth_id=s.db.query(
          query="SELECT "+arg['auth_id_field']+' FROM '+arg['auth_table']+' WHERE '+arg['auth_log_field']+'=%s AND '+arg['auth_pas_field']+'=%s '+add_where,
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
      table=arg['session_table'],
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
  manager_table='manager'
  errors=[]
  if config['use_project']:
    session_table='project_session'
    manager_table='project_manager'

  
  ok=s.db.query(
    query='SELECT count(*) FROM '+session_table+' WHERE auth_id=%s and session_key=%s',
    values=[user_id, key],
    onevalue=1,
    errors=errors
  )
  manager={'login':'','id':False}

  if ok:
      manager=s.db.query(
        query='select * from '+manager_table+' where id=%s',
        values=[user_id],
        onerow=1,errors=errors
      );
      if manager:
        del manager['password']
        s.manager=manager
  
  s._content={
    'success':1,
    'login':manager['login'],
    'errors':errors
  }
  if manager['login']:
    s.login=manager['login']
  else:
    s._content['redirect']='/login'
    s._content['success']=0
    s.end()

def session_logout(s,**arg):
  user_id=s.get_cookie('auth_user_id')
  key=s.get_cookie('auth_key')
  if user_id.isdigit() and int(user_id) and key :
      s.db.query(
        query='DELETE FROM project_session WHERE auth_id=%s and session_key=%s',
        values=[user_id,key]
      )
  else:
      s.db.query(
        query='DELETE FROM session WHERE auth_id=%s and session_key=%s',
        values=[user_id,key]
      )


