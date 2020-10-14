from fastapi import APIRouter, Request, Cookie
from config import config
from lib.engine import s

from .startpage import router as router_startpage
from .testing import router as router_testing
from lib.session import session_project_create, session_create
router = APIRouter()
router.include_router(router_startpage)
router.include_router(router_testing)

@router.get("/")
async def mainpage():
  
  return {
    "this is ajax_router": True,
    "manager":s.manager
  }


# Авторизация
# curl -X 'POST' -d "{\"login\":\"admin\",\"password\":\"123\"}" http://localhost:5000/login
@router.post('/login')
async def login(R: dict):
  response={'success':0}
  if R:
    if config['use_project']:
      response=session_project_create(
        s,
        login=R['login'],
        password=R['password'],
        ip=s.env['HTTP_X_REAL_IP'],
        encrypt_method=config['encrypt_methon'],
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
        ip=s.env['HTTP_X_REAL_IP'],
        encrypt_method=config['encrypt_methon'],
        max_fails_login=3,
        max_fails_login_interval=3600,
        max_fails_ip=20,
        max_fails_ip_interval=3600
      )

  return response

@router.get('/logout')
async def logout():
  return {""}

