from lib.core import exists_arg
from fastapi import Response
import socket # только для определения hostname
import json
from db import db,db_read,db_write
from .session import *
from config import config
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
    #print('host:',hostname)
    # Если мы не логинимся -- проверяем сессию
    s.config=config
    s.use_project=config['use_project']
    if not(self.request.url.path in config['login']['not_login_access']):

      if hostname in config['debug']['hosts']:
        self.manager=db.getrow(
          table="manager",
          select_fields="id,login",
          where="id=%s",
          values=[config['debug']['manager_id']]
        )
        if self.manager:
          self.login=self.manager['login']
        else:
          self.manager={'id':config['debug']['manager_id'],'name':'менеджер не найден'}
      else:
        #print('session start')
        session_start(self,encrypt_method=config['encrypt_method']);

            
            
      
          


    

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