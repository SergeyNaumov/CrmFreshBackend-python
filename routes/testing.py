from fastapi import FastAPI, APIRouter
from config import config
from db import db,db_read,db_write


router = APIRouter()
@router.get('/test-headers')
async def test_headers():
  #s.headers.append(['content-type','image/png'])
  return []

@router.get('/test-cookie-write')
async def test_cookie_write():
  #print('controller:',s.response)
  #s.set_cookie(name='cookie_test',value=555)
  #s.set_cookie('cookie_test','321')
  #s.cookies_for_delete.append('User-Agent')
  #s.cookies_for_delete.append('cookie_testing')

  # response=s.response
  #s.set_cookie(
  #   name='cookie_testing',
  #   value='Z0'
  #)
  return {'setting':'ok'}




@router.get('/test-cookie-read')
async def test_cookie_read():
  print(s.get_cookie('cookie_testing'))
  print(s.get_cookie('User-Agent'))
  return {'cookie_reading':'ok'}

@router.get("/config")
async def show_config():
  print(db)
  return config

@router.get('/test-query')
async def test_query():
  manager=db.query(
    query='select * from manager where login=%s',
    values=['admin'],
    onerow=1
  )
  return manager