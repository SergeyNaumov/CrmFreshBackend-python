from lib.all_configs import read_config
from fastapi import APIRouter
import requests
import urllib
import json

router = APIRouter()

@router.post('/extend/KLADR')
async def kladr(R: dict):
  action='onestring'
  errors=[]
  if 'action' in R:
    action==R['action']
  
  list=[]
  query=R['query']
  config=R['config']
  name=R['name']

  if action == 'onestring':
    
    #request_str=f'?query=моск&oneString=1&withParent=false&limit=10'
    url='https://kladr-api.ru/api.php?'
    request={
      'query':query,
      'oneString':1,
      'withParent':'false',
      'limit':'10'
    }
    request_str=urllib.parse.urlencode(request)
    #print('request_str: ',request_str)
    response=requests.get('https://kladr-api.ru/api.php?'+request_str)

    if response.content:
      #print(response.content)
      data=json.loads(response.content)
      
      if data:
        if config and name:
            form=read_config(config=config,script='edit_form')
            
            field=form.fields_hash[name]
            
            if 'after_search' in field['kladr']:
              func_after_search=field['kladr']['after_search']
              list=func_after_search(data['result'])
            elif data['result'] and data:
              for d in data['result']:
                list.append({'header':d['fullName']})
        return {'success':1,'list':list}

  return {'success':0,'errors':errors}