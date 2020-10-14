from lib.core import exists_arg
from fastapi import Response
import socket # только для определения hostname

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
    

    
    
    #self.cookies['User-Agent']=''

    hostname=socket.gethostname()
    if hostname=='sv-home':
      self.manager={'id':'1','login':'admin'}
    else:
      self.manager={'id':'1','login':'admin'}

    print('hostname',hostname)

    #if not(exists_arg('login',))

  def set_cookie(self,*par,**arg):
    if len(par)==2:
      arg['name']=par[0]
      arg['value']=par[1]
    
    print('arg',arg)
    if arg['value'] or str(arg['value'])=='0' or arg['value']=='':
      self.cookies[arg['name']]=arg['value']
    else:
      self.cookies_for_delete.append(arg['name'])
    

  def get_cookie(self,cookie_name):
    return self.request.cookies.get(cookie_name)

s=Engine()