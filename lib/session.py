from lib.core import exists_arg, gen_pas
from db import db,db_read,db_write
#from lib.engine import s

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
      fails=db.query(
        query='select count(*) from session_fails where ip=%s and registered>=now() - interval %s second',
        values=arg['ip'],
        onevalue=True,
        errors=errors
      )

      if fails > arg['max_fails_ip'] :
          return 'Ошибка безопасности: превышено максимальное количество входа по IP'
  

  auth_id=-1
  if arg['encrypt_method']=='mysql_encrypt':
      auth_id=db.query(
        query='SELECT '+arg['auth_id_field']+' FROM '+arg['auth_table']+' WHERE '+arg['auth_log_field']+'=%s AND '+arg['auth_pas_field']+'=ENCRYPT(%s,password) '+add_where,
        values=[arg['login'],arg['password']],
        onevalue=True
      )
  else:
      auth_id=db.query(
          query="SELECT "+arg['auth_id_field']+' FROM '+arg['auth_table']+' WHERE '+arg['auth_log_field']+'=%s AND '+arg['auth_pas_field']+'=%s '+add_where,
          values=[arg['login'], arg['password']],
          onevalue=True
      );

  if auth_id>0:
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

    s.set_cookie(name='auth_user_id')

def session_start(s,**arg):
  user_id=s.get_cookie('auth_user_id')
  key=s.get_cookie('auth_key')

