from fastapi import FastAPI, APIRouter
from config import config
from db import db,db_read,db_write

router = APIRouter()
@router.get('/startpage')
async def view_startpage():
  errors=[]
  
  if 'use_project' in config and config['use_project']:
    print('use_project')
    # manager=db_read.query(
    #   'query':'',
    #   'values':[],
    #   'onerow':1
    # )
  else:
    print('not use_project')
    # manager=db_read.query(
    #   'query':'select *,concat("/edit_form/manager/",id) link from manager where login=?',
    #   'values':[$s->{login}],
    #   'onerow':True,
    #   'errors':errors
    # )


  return {"startpage":True}