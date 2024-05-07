from lib.core import cur_year,cur_date
from fastapi import FastAPI, APIRouter
from config import config
#from db import db,db_read,db_write
from lib.engine import s
from lib.session import *
from lib.send_mes import send_mes

router = APIRouter()
@router.get('/test')
async def test():
  return {'okay':await s.db.query(query="SELECT * from managers where login='naumov'",onerow=1)}

# Левое меню по-умолчанию
@router.get('/left-menu')
async def leftmenu():
  errors=[]
  manager=None
  manager_menu_table=None
  left_menu=[]

  if(config['use_project']):
      manager=await s.db.query(
        query=f'select *,concat("/edit_form/project_manager/",{config["auth"]["manager_table_id"]}) link from project_manager where project_id=%s and login=%s',
        values=[s.project_id,s.login]
      )
      manager_menu_table='project_manager_menu'
      left_menu=await s.db(
        query='SELECT * from '+manager_menu_table+'  order by sort',
        errors=errors,
        tree_use=1
      )
  else:
      
      manager=await s.db.query(
        query=f"select *,concat('/edit_form/manager/',{config['auth']['manager_table_id']}) link from {config['auth']['manager_table']} where login=%s",
        values=[s.login],
        onerow=1,
      )
      
      manager['permissions']=await s.db.query(
        query='SELECT permissions_id from manager_permissions where manager_id=%s',
        values=[manager['id']],
        massive=1
      )
      j=0

      for p in manager['permissions']: 
        manager['permissions'][j]=str(manager['permissions'][j])
        j+=1
        
      #manager['permissions'][0::,0] = manager['permissions'][0::,0].astype(str)
      
      perm_str='0'
      if len(manager['permissions']):
        perm_str=','.join(manager['permissions'])

      left_menu=await s.db.query(
        query="""
          SELECT
            mm.*,group_concat(concat(mmp.permission_id,':',denied) SEPARATOR ';') perm
          from
            manager_menu mm
            LEFT JOIN manager_menu_permissions mmp ON mmp.menu_id=mm.id
          where
            
            (
              mmp.id is null
                OR 
              (mmp.denied=0 and mmp.permission_id in ("""+perm_str+""") )
                OR
              (mmp.denied=1 and mmp.permission_id not in ("""+perm_str+""") ) 
            )
          GROUP BY mm.id
          ORDER BY mm.sort
        """,
        errors=errors,
        tree_use=1
      )
      if ('menu' in config) and config['menu'] and len(config['menu']):
        left_menu=config.menu
      
  
  
  del manager['password']
  return {
    'left_menu':left_menu,
    'errors':errors,
    'success': not len(errors),
  }

# Стартовая страница
@router.get('/startpage')
async def startpage():

  errors=s.errors
  manager=None
  manager_menu_table=None
  left_menu=[]
  if hasattr(s,'login'):

    if(config['use_project']):
        manager=await s.db.query(
          query=f'select *,concat("/edit_form/project_manager/",{config["auth"]["manager_table_id"]}) link from project_manager where project_id=%s and login=%s',
          values=[s.project_id,s.login]
        )
        manager_menu_table='project_manager_menu'

    else:
        manager=await s.db.query(
          query=f"select *,concat('/edit_form/manager/',{config['auth']['manager_table_id']}) link from {config['auth']['manager_table']} where login=%s",
          values=[s.login],
          onerow=1,
        )
  else:
    errors.append('Ошибка авторизации')
  
  




  CY=cur_year()
  if manager and ('password' in manager): del manager['password']


  left_menu_controller='/left-menu'
  
  auth=config['auth']
  # если используются роли
  if config['auth']['use_roles'] and manager['current_role']:
    

    if role_login:=await s.db.query(
      query=f"select {auth['auth_log_field']} from {auth['manager_table']} where {auth['manager_table_id']}=%s",
      values=[manager['current_role']],
      onevalue=1
    ):
        manager['role_login']=role_login
  
  # В конфиге настроен вывод на ссылку карточки        
  if auth.get('out_manager_card_link'):
    manager['out_manager_card_link']=True
  if exists_arg('left-menu',s.config['controllers']):
    left_menu_controller=s.config['controllers']['left_menu']
  response={
    'title':config['title'],
    'copyright':config['copyright'].replace('{{cur_year}}',CY),
    'left_menu_controller':left_menu_controller,
    'errors':errors,
    'success': not len(errors),
    'manager':manager
  }
  

  
  if 'app_components' in config:
    response['app_components'] = config['app_components']
  
  
  if not(manager):
    response['redirect']=config['BaseUrl']+'/login'
  
  if 'bottom_menu' in config:
    
    response['bottom_menu']=config['bottom_menu']
  
  
  return response

# get-events
@router.get('/get-events')
async def get_events():
  return {'success':1,'message':''}

# Авторизация
@router.post('/login')
async def login(R: dict):
  response={'success':0}
  if R:
    if config['use_project']:
      response=await session_project_create(
        s,
        login=R['login'],
        password=R['password'],
        ip=s.env['x-real-ip'],
        #encrypt_method=config['encrypt_method'],
        max_fails_login=3,
        max_fails_login_interval=3600,
        max_fails_ip=20,
        max_fails_ip_interval=3600

      )
    else:
      response=await session_create(
        s,
        login=R['login'],
        password=R['password'],
        ip=s.env['x-real-ip'],
        #encrypt_method=config['encrypt_method'],
        max_fails_login=3,
        max_fails_login_interval=3600,
        max_fails_ip=20,
        max_fails_ip_interval=3600
      )

  return response

@router.get('/send_mes')
async def sm_test():
  send_mes({'a':1,'b':2,'c':3})
  return {'sended':True}

@router.get('/logout')
async def logout():
  await session_logout(s)
  return {"success":1}
