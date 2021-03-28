from fastapi import FastAPI, APIRouter
from config import config
from db import db,db_read,db_write
#from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from lib.send_mes import send_mes




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



@router.get('/test/quote')
async def test_quote():
  string=db.connect.escape_string('sv " \' cms')
  return {'result':string}
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
  errors=[]
  result=db.query(
    query='desc test',
    values=[],
    errors=errors
  )
  return {
    'result':result,
    'errors':errors
  }

@router.get('/test/mailsend')
async def testmailsend():
  send_mes(
    to='svcomplex@gmail.com',
    subject='Тестовая тема (Fastapi)',
    message='<p><b>Привет!</b> Это html!</p>'
  )
  return {'ok':1}