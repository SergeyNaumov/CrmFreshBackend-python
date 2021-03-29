from lib.core import exists_arg
from fastapi import Response
import socket # только для определения hostname
import json
from db import db,db_read,db_write
from .session import *

class Engine():
  def __init__(self,**arg):
    self.manager={}
  
  def reset(self,**arg):
    self.db=db
    self.db_read=db_read
    self.db_write=db_write
    self.request=arg['request']
    self.headers=[]
    self.cookies={}
    self.cookies_for_delete=[]
    self._end=False
    self._content_type='application/json'
    self._content=''
    self.project=None
    
    self.env={}
    #print('request_url:',self.request.url.path)
    # x-real-ip

    for k in self.request['headers']:
      self.env[str(k[0].decode("utf-8"))]=str(k[1].decode("utf-8"))
      #print(str( k[0].decode("utf-8") ),'=>',str(k[1].decode("utf-8")) )
    
    #self.cookies['User-Agent']=''

    hostname=socket.gethostname()

    # Если мы не логинимся -- проверяем сессию
    if self.request.url.path not in ['/login','/test/mailsend','/register','/remember/get-access-code','/remember/check-access-code','/remember/change-password']:
      if hostname in ['sv-home','sv-digital']:
          self.manager={'id':'1','login':'admin'}
          self.login='admin'
          s.use_project=0
      else:
          session_start(self,encrypt_method='mysql_sha2');


    

    #if not(exists_arg('login',))

  def set_cookie(self,*par,**arg):
    if len(par)==2:
      arg['name']=par[0]
      arg['value']=par[1]
    
    #print('arg',arg)
    if arg['value'] or str(arg['value'])=='0' or arg['value']=='':
      self.cookies[arg['name']]=arg['value']
    else:
      self.cookies_for_delete.append(arg['name'])
    

  def get_cookie(self,cookie_name):
    return self.request.cookies.get(cookie_name)
  def end(self):
    self._end=True

  def to_json(self,data):
      return json.dumps(data, sort_keys=False,indent=4,ensure_ascii=False,separators=(',', ': '))

s=Engine()