from lib.core import exists_arg
from fastapi import Response
import socket # только для определения hostname
import json
from db import db,db_read,db_write
from .session import *
from config import config
import os
pwd=os.path.abspath(os.curdir)
hostname=socket.gethostname()

class Engine():
  def __init__(self,**arg):

    self.manager={}
    self.errors=[]
    
  async def reset(s,**arg):


    s.db=db
    s.db_read=db_read
    s.db_write=db_write
    s.request=request=arg['request']
    s.headers=[]
    s.request.state.cookies={}
    s.request.state.cookies_for_delete=[]
    s._end=False
    s._content_type='application/json'
    s._content=''
    s.project=None
    s.errors=[]
    s.env={}

    #print('request_url:',self.request.url.path)
    # x-real-ip

    for k in s.request['headers']:
      s.env[str(k[0].decode("utf-8"))]=str(k[1].decode("utf-8"))
      #print(str( k[0].decode("utf-8") ),'=>',str(k[1].decode("utf-8")) )
    
    #self.cookies['User-Agent']=''

    
    #print('host:',hostname)
    # Если мы не логинимся -- проверяем сессию
    s.config=config
    auth=config['auth']
    s.use_project=config['use_project']
    #print('url:',request.url.path)
    if not(request.url.path in config['login']['not_login_access']):
      host_ok=not('hosts' in config['debug']) or (('hosts' in config['debug']) and  ( hostname in config['debug']['hosts'] ))
      
      pwd_ok=not('pwd' in config['debug']) or (('pwd' in config['debug']) and  ( pwd in config['debug']['pwd'] ))
      #print('pwd:',pwd)
      #print('host_ok:',host_ok,' pwd_ok:',pwd_ok)
      if host_ok and pwd_ok:
        where='0'
        values=[]
        if 'manager_id' in config['debug']:
          where=f"{auth['manager_table_id']}={config['debug']['manager_id']}"

        if 'login' in config['debug']:
          where=f"login='{config['debug']['login']}'"
        

        manager=request.state.manager=await db.getrow(
          table=auth['manager_table'],
          where=where,
          values=values,

        )


        if manager:
          manager['id']=manager[auth['manager_table_id']]
          #self.login=self.manager['login']
        else:
          #self.login='nonelogin'
          manager={'id':0,'login':'nonelogin','name':'менеджер не найден'}
      else:
        
        await session_start(s,request=request);

      # для того, чтобы избежать путаницы в сессиях
      #s.request.state.manager=s.manager
      #print('RESET self.request.state.manager:',self.request.state.manager)
      manager=request.state.manager
      if manager['id'] and ('after_create_engine' in config):
        config['after_create_engine'](s)

      #print('MANAGER:',self.manager)

    #if not(exists_arg('login',))

  def set_cookie(self,*par,**arg):
    if len(par)==2:
      arg['name']=par[0]
      arg['value']=par[1]
    
    #print('arg',arg)
    if arg['value'] or str(arg['value'])=='0' or not(arg['value']):
      self.request.state.cookies[arg['name']]=arg['value']
    else:
      self.request.state.cookies_for_delete.append(arg['name'])
    

  def get_cookie(self,cookie_name):
    return self.request.cookies.get(cookie_name)
  def end(self):
    self._end=True

  def to_json(self,data):
      return json.dumps(data, sort_keys=False,indent=4,ensure_ascii=False,separators=(',', ': '))

s=Engine()
