from lib.core import cur_year,cur_date
from fastapi import FastAPI, APIRouter
from config import config
#from db import db,db_read,db_write
from lib.engine import s
from lib.session import *

router = APIRouter()
# Главная
@router.get('/mainpage')
async def mainpage():
  curdate=cur_date(format="%d.%m.%Y")
  response={'curdate':curdate}
  if s.project:
    response['manager']=s.db.query(
      query='SELECT id,login,name,position, concat("/edit-form/project_manager/",id) link from project_manager where project_id=%s and id=%s',
      values=[s.project['id']],
      onerow=1
    )

    response['news_list']=s.db.query(
      query='SELECT header,DATE_FORMAT(a.registered, "%e.%m.%y") registered,body from project_crm_news WHERE project_id=%s order by registered desc limit 5',
      values=[s.project['id']]
    )
  else:
    
    response['manager']=s.db.getrow(
      table="manager",
      select_fields='id,login,name,position, concat("/edit-form/manager/",id) link',
      where='id=%s',
      values=[s.manager['id']],
      str=1,
    )

    response['news_list']=s.db.query(
      query='SELECT header,DATE_FORMAT(registered, %s) registered, body from crm_news order by registered desc limit 5',
      values=["%e.%m.%y"]
    )
  
  if not response['manager']:
    print('отсутствует запись с manager.id=='+s.manager['id'])

  return response

# Стартовая страница
@router.get('/startpage')
async def startpage():
  errors=[]
  manager=None
  manager_menu_table=None
  left_menu=[]

  if(config['use_project']):
      manager=s.db.query(
        query='select *,concat("/edit_form/project_manager/",id) link from project_manager where project_id=%s and login=%s',
        values=[s.project_id,s.login]
      )
      manager_menu_table='project_manager_menu'
      left_menu=s.db(
        query='SELECT * from '+manager_menu_table+'  order by sort',
        errors=errors,
        tree_use=1
      )

  else:

      manager=s.db.query(
        query='select *,concat("/edit_form/manager/",id) link from manager where login=%s',
        values=[s.login],
        onerow=1,
        debug=1
      )
      
      manager['permissions']=s.db.query(
        query='SELECT permissions_id from manager_permissions where manager_id=%s',
        values=[manager['id']],
        massive=1
      )
      j=0

      for p in manager['permissions']: 
        manager['permissions'][j]=str(manager['permissions'][j])
        #print(f'P:{p},  j:{j}')
        j+=1
      #manager['permissions'][0::,0] = manager['permissions'][0::,0].astype(str)
      
      perm_str='0'
      if len(manager['permissions']):
        perm_str=','.join(manager['permissions'])

      left_menu=s.db.query(
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
      
  CY=cur_year()
  
  del manager['password']
  return {
    'title':config['title'],
    'copyright':config['copyright'].replace('{{cur_year}}',CY),
    'left_menu':left_menu,
    'errors':errors,
    'success': not len(errors),
    'manager':manager
  }



  return {"startpage":True}


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
      response=session_project_create(
        s,
        login=R['login'],
        password=R['password'],
        ip=s.env['x-real-ip'],
        encrypt_method=config['encrypt_method'],
        max_fails_login=3,
        max_fails_login_interval=3600,
        max_fails_ip=20,
        max_fails_ip_interval=3600

      )
    else:
      response=session_create(
        s,
        login=R['login'],
        password=R['password'],
        ip=s.env['x-real-ip'],
        encrypt_method=config['encrypt_methon'],
        max_fails_login=3,
        max_fails_login_interval=3600,
        max_fails_ip=20,
        max_fails_ip_interval=3600
      )

  return response

@router.get('/logout')
async def logout():
  session_logout(s)
  return {"success":1}
