from fastapi import APIRouter, Request
import sys
# 2026-09-27: remove global s from login.py, migrate to request.state.engine
from lib.all_configs import read_config
from lib.session import session_start

router = APIRouter()

@router.get('/login')
async def login(R:dict, request: Request): # 2026-09-27: added request: Request
  # 2026-09-27: removed global s, use request.state.engine directly, project_id via request
  s=request.state.engine # 2026-09-27: engine is on request.state directly, no need to read engine first
  errors=[]; _login=''
  if not('login' in R): errors.append('нет login'); return {'success':0,'errors':errors}
  _login=R['login']
  
  s=await session_start(s=s, login=_login, password=R.get('password', ''), errors=errors) # 2026-09-27: engine is on request.state, not global s
  if errors or not s.request.state.manager['id']:
    login=R.pop('login')
    return {'success':1,'login':login,'errors':errors} # 2026-09-27: no global db.get_db needed

@router.post('/test')
async def test(R: dict, request: Request): # 2026-09-27: added request: Request
  errors=[]
  try:
    s=request.state.engine # 2026-09-27: removed global s=await db.get_db() (returns None)
    # 2026-09-27: project_id from request.state, need to fix this
    response={'errors': errors, 'success':1, 'project_id':s.project['id']} # 2026-09-27: engine is on request.state directly, not global
  except Exception as e:
    errors.append(str(e)); response={'errors': errors, 'success':0} # 2026-09-27: no global db here
  finally:
    if errors and len(errors): response['success']=0
  return response

@router.get('/left-menu')
async def left_menu(R: dict, request: Request): # 2026-09-27: added request: Request
  errors=[]; s=request.state.engine # 2026-09-27: removed global s
  try:
    db=request.state.db # 2026-09-27: engine on request.state, not global
    m=await db.query(query='select * from left_menu where manager_id=%s order by position asc', values=[R.get('manager_id')], massive=1, errors=errors, str=1) # 2026-09-27: no global db here
    return {'success':1,'login':m[1],'left_menu':m,'project_id':s.project['id']} # 2026-09-27: no global db needed
  except Exception as e:
    errors.append(str(e)); response={'errors':errors,'success':0} # 2026-09-27: no global s here

@router.get('/left-menu/tree')
async def left_menu_tree(R:dict, request: Request): # 2026-09-27: added request: Request
  errors=[]; _login=''
  m=await session_start(s=request.state.engine, login=R['login'], password=R.get('password')) # 2026-09-27: engine is on request.state, not global
  if errors and len(errors):
    return {'errors':errors,'success':0} # 2026-09-27: no global s needed
  
# 2026-09-27: removed from lib.engine import s (global), engine is on request.state directly
