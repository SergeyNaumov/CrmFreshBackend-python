from fastapi import FastAPI, APIRouter, Response, Cookie
from config import config
from lib.engine import s

from .startpage import router as router_startpage
from .testing import router as router_testing

router = APIRouter()
router.include_router(router_startpage)
router.include_router(router_testing)

@router.get("/")
async def mainpage():
  
  return {
    "this is ajax_router": True,
    "manager":s.manager
  }



@router.get('/logout')
async def logout():
  return {""}

